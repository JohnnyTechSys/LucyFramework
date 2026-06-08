from functools import wraps
import inspect
import os
from .req import req, process_data_part

# Load .env at module import time
try:
    import dotenv

    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(package_dir, ".env")
    if os.path.exists(dotenv_path):
        dotenv.load_dotenv(dotenv_path)
    else:
        dotenv.load_dotenv()
except Exception:
    pass


class Lucy:
    def __init__(self, api_key=None, history_limit=10):
        self.toollist = []
        self.tools_map = {}
        self.history = []
        self.history_limit = history_limit
        self.api_key = api_key or os.getenv("HZAPIKEY") or os.getenv("GEMINI_API_KEY")

    def tool(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        hints = inspect.signature(func).parameters
        properties = {}
        required = []

        type_map = {
            str: "string",
            float: "number",
            int: "integer",
            bool: "boolean",
            list: "array",
            dict: "object",
        }

        for name, param in hints.items():
            if name in ("self", "cls"):
                continue
            annotation = param.annotation
            properties[name] = {
                "type": type_map.get(annotation, "string"),
                "description": f"Parameter {name}",
            }
            if param.default is inspect.Parameter.empty:
                required.append(name)

        self.tools_map[func.__name__] = func

        self.toollist.append(
            {
                "name": func.__name__,
                "description": func.__doc__ or "",
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            }
        )

        return wrapper

    def clear_history(self):
        self.history = []

    def _get_history_contents(self):
        # Filter history to remove completed tool call cycles
        # This maintains proper turn structure for Gemini API
        filtered_history = []
        i = 0
        while i < len(self.history):
            turn = self.history[i]
            filtered_history.append(turn)
            
            # If this is a model turn with tool calls, skip the function response and final model response
            if turn.get("role") == "model":
                parts = turn.get("parts", [])
                has_tool_call = any(
                    part.get("functionCall") or part.get("function_call") 
                    for part in parts
                )
                if has_tool_call and i + 2 < len(self.history):
                    # Skip the function response (user with functionResponse)
                    # and the final model response
                    i += 2
            i += 1
        
        if self.history_limit and len(filtered_history) > self.history_limit:
            return filtered_history[-self.history_limit :]
        return filtered_history

    def run(
        self,
        text=None,
        audiodata=None,
        videodata=None,
        imagedata=None,
        systemprompt=None,
        max_turns=10,
    ):
        if not self.api_key:
            import dotenv

            package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dotenv_path = os.path.join(package_dir, ".env")
            if os.path.exists(dotenv_path):
                dotenv.load_dotenv(dotenv_path)
            else:
                dotenv.load_dotenv()
            self.api_key = os.getenv("HZAPIKEY") or os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "HZAPIKEY or GEMINI_API_KEY is not set. Please provide it or set it in your environment."
                )

        user_parts = []

        audio_part = process_data_part(audiodata, "audio/wav")
        if audio_part:
            user_parts.append(audio_part)

        video_part = process_data_part(videodata, "video/mp4")
        if video_part:
            user_parts.append(video_part)

        image_part = process_data_part(imagedata, "image/png")
        if image_part:
            user_parts.append(image_part)

        if text:
            user_parts.append({"text": text})

        if user_parts:
            self.history.append({"role": "user", "parts": user_parts})
        elif not self.history:
            self.history.append({"role": "user", "parts": [{"text": ""}]})

        response = req(
            toollist=self.toollist,
            text=None,
            key=self.api_key,
            systemprompt=systemprompt,
            audiodata=None,
            videodata=None,
            imagedata=None,
            contents=self._get_history_contents(),
        )

        # Accumulate executed tool calls across turns
        executed_tool_calls = []

        for turn in range(max_turns):
            if "error" in response:
                return f"Error: {response['error'].get('message', 'Unknown API Error')}"

            candidates = response.get("candidates", [])
            if not candidates:
                return response.get("promptFeedback", "No response generated by model.")

            candidate = candidates[0]
            content = candidate.get("content")
            if not content:
                return "No content returned by model."

            if "role" not in content:
                content["role"] = "model"
            self.history.append(content)

            parts = content.get("parts", [])
            tool_calls = []
            for part in parts:
                call = part.get("functionCall") or part.get("function_call")
                if call:
                    tool_calls.append(call)

            if not tool_calls:
                output_text = "".join(part.get("text", "") for part in parts)
                return {"tool_calls": executed_tool_calls, "output": output_text}

            function_response_parts = []
            for call in tool_calls:
                name = call.get("name")
                args = call.get("args", {})

                func = self.tools_map.get(name)
                if func:
                    try:
                        result = func(**args)
                    except Exception as e:
                        result = f"Error executing tool {name}: {str(e)}"
                else:
                    result = f"Error: Tool '{name}' not found."

                response_dict = (
                    result if isinstance(result, dict) else {"output": result}
                )

                function_response_parts.append(
                    {"functionResponse": {"name": name, "response": response_dict}}
                )

            self.history.append({"role": "user", "parts": function_response_parts})
            # Record executed tool calls
            for p in function_response_parts:
                executed_tool_calls.append(p["functionResponse"])

            # Request model again to get its follow-up output (or further tool calls)
            response = req(
                toollist=self.toollist,
                text=None,
                key=self.api_key,
                systemprompt=systemprompt,
                audiodata=None,
                videodata=None,
                imagedata=None,
                contents=self._get_history_contents(),
            )

        return "Error: Maximum tool execution turns exceeded."
