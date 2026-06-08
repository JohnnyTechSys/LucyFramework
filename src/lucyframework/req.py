import base64
import io
import os
import requests

import numpy as np
from PIL import Image as PILImage

_SESSION = requests.Session()

# Native audio / video / image input (generateContent multimodal).
_MULTIMODAL_DEFAULT_MODEL = "gemini-3.1-flash-image"
_MULTIMODAL_FALLBACK_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
]

# Text-only and light tool calls (no inline media).
_TEXT_DEFAULT_MODEL = "gemini-3.1-flash-lite"
_TEXT_FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]

_RETRYABLE_STATUS = (429, 500, 503)

try:
    from google.genai import types

    _GOOGLE_GENAI_AVAILABLE = True
except Exception:
    types = None
    _GOOGLE_GENAI_AVAILABLE = False


def process_data_part(data, default_mime):
    if data is None:
        return None

    if hasattr(data, "to_json_dict"):
        return data.to_json_dict()

    if isinstance(data, dict):
        return data

    if isinstance(data, np.ndarray):
        try:
            img = PILImage.fromarray(data)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            raw_bytes = buf.getvalue()
            if _GOOGLE_GENAI_AVAILABLE:
                try:
                    part = types.Part.from_bytes(data=raw_bytes, mime_type="image/png")
                    return part.to_json_dict()
                except Exception:
                    pass
            b64_data = base64.b64encode(raw_bytes).decode("utf-8")
            return {"inline_data": {"mime_type": "image/png", "data": b64_data}}
        except Exception:
            return None

    if isinstance(data, PILImage.Image):
        try:
            buf = io.BytesIO()
            data.save(buf, format="PNG")
            raw_bytes = buf.getvalue()
            if _GOOGLE_GENAI_AVAILABLE:
                try:
                    part = types.Part.from_bytes(data=raw_bytes, mime_type="image/png")
                    return part.to_json_dict()
                except Exception:
                    pass
            b64_data = base64.b64encode(raw_bytes).decode("utf-8")
            return {"inline_data": {"mime_type": "image/png", "data": b64_data}}
        except Exception:
            return None

    if isinstance(data, bytes):
        part = None
        if _GOOGLE_GENAI_AVAILABLE:
            try:
                part = types.Part.from_bytes(data=data, mime_type=default_mime)
            except Exception:
                part = None
        if part:
            return part.to_json_dict()
        b64_data = base64.b64encode(data).decode("utf-8")
        return {"inline_data": {"mime_type": default_mime, "data": b64_data}}

    if isinstance(data, str) and not data.startswith(("http://", "https://")):
        if not os.path.exists(data):
            return None
        try:
            with open(data, "rb") as f:
                file_bytes = f.read()
        except Exception:
            return None

        mime = default_mime
        ext = data.lower()
        if ext.endswith(".wav"):
            mime = "audio/wav"
        elif ext.endswith(".mp3"):
            mime = "audio/mp3"
        elif ext.endswith(".mp4"):
            mime = "video/mp4"
        elif ext.endswith(".png"):
            mime = "image/png"
        elif ext.endswith((".jpg", ".jpeg")):
            mime = "image/jpeg"

        part = None
        if _GOOGLE_GENAI_AVAILABLE:
            try:
                part = types.Part.from_bytes(data=file_bytes, mime_type=mime)
            except Exception:
                part = None
        if part:
            return part.to_json_dict()

        b64_data = base64.b64encode(file_bytes).decode("utf-8")
        return {"inline_data": {"mime_type": mime, "data": b64_data}}

    return None


def _payload_has_media(payload):
    for content in payload.get("contents", []):
        for part in content.get("parts", []):
            if part.get("inline_data") or part.get("inlineData"):
                return True
            if part.get("file_data") or part.get("fileData"):
                return True
    return False


def _models_for_request(payload, model_name):
    if model_name:
        return [model_name]
    if _payload_has_media(payload):
        return [_MULTIMODAL_DEFAULT_MODEL, *_MULTIMODAL_FALLBACK_MODELS]
    return [_TEXT_DEFAULT_MODEL, *_TEXT_FALLBACK_MODELS]


def req(
    toollist,
    text,
    key,
    systemprompt,
    audiodata,
    videodata,
    imagedata,
    contents=None,
    model_name=None,
):
    parts = []

    audio_part = process_data_part(audiodata, "audio/wav")
    if audio_part:
        parts.append(audio_part)

    video_part = process_data_part(videodata, "video/mp4")
    if video_part:
        parts.append(video_part)

    image_part = process_data_part(imagedata, "image/png")
    if image_part:
        parts.append(image_part)

    if text:
        parts.append({"text": text})

    if contents is not None:
        payload_contents = list(contents)
        if parts:
            payload_contents.append({"role": "user", "parts": parts})
        payload = {"contents": payload_contents}
    else:
        if not parts:
            parts.append({"text": ""})
        payload = {"contents": [{"role": "user", "parts": parts}]}

    if systemprompt:
        payload["system_instruction"] = {"parts": [{"text": systemprompt}]}

    has_media = _payload_has_media(payload)
    if toollist:
        payload["tools"] = [{"function_declarations": toollist}]
    elif has_media:
        # code_execution rejects audio/video inline parts.
        payload["tools"] = [{"google_search": {}}]
    else:
        payload["tools"] = [{"google_search": {}}, {"code_execution": {}}]

    models_to_try = _models_for_request(payload, model_name)
    timeout = 120 if has_media else 30
    response = None
    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        response = _SESSION.post(
            url, params={"key": key}, json=payload, timeout=timeout
        )

        if response.status_code == 200:
            break

        if response.status_code in _RETRYABLE_STATUS:
            reason = {
                429: "Rate limited",
                500: "Internal error (500)",
                503: "Temporarily unavailable (503)",
            }[response.status_code]
            print(f"[req] {reason} on {model}. Retrying with fallback model...")
            continue

        raise Exception(f"Gemini error {response.status_code}: {response.text}")

    if response is None or response.status_code != 200:
        raise Exception(
            f"Gemini error {response.status_code if response else 'No Response'}: {response.text if response else 'No content'}"
        )

    return response.json()
