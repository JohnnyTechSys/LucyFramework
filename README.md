# 🚀 LucyAI

Turn Python functions into multimodal AI agents.

LucyAI is a lightweight framework for building AI agents with tool calling, memory, and multimodal inputs in pure Python.

No graphs. No config files. No boilerplate.

Just Python → agents.

---

## ⚡ Features

- Simple Python-first API
- Automatic tool calling
- Tool schemas generated from type hints
- Conversation history built-in
- Image, audio, and video inputs
- NumPy + Pillow support
- Gemini integration (with fallback chain)
- Minimal dependencies
- Python 3.11+

---

## 📦 Installation
```
uv add lucyai #UV is recomended
```
or
```
pip install lucyai #pip is fine
```
<br>

## 🧠 Quick Start
```
from lucyai import Lucy

agent = Lucy()

response = agent.run("Hello!")
print(response)
```
<br>

## 🔧 Tool Calling
```
from lucyai import Lucy

agent = Lucy()

@agent.tool
def get_time() -> str:
    return "3:00 PM"

@agent.tool
def add(a: int, b: int) -> int:
    return a + b
```
<br>

## 🖼️ Image Input
```
agent.run("What is in this image?", imagedata="image.png")
```
Supported:
- PNG
- JPEG
- Pillow Images
- NumPy Arrays
- Raw bytes

<br>

## 🎧 Audio Input
```
agent.run("Transcribe this audio", audiodata="audio.wav")
```
Supported:
- WAV
- MP3
- Raw bytes

<br>

## 🎥 Video Input
```
agent.run("Describe this video", videodata="video.mp4")
```
Supported:
- MP4
- Raw bytes

<br>

## 💭 Memory
```
agent = Lucy(history_limit=10)

agent.run("My name is Johnny")
agent.run("What is my name?")

agent.clear_history()
```
<br>
## 🔑 API Keys

Environment variables:
- GEMINI_API_KEY
- HZAPIKEY
```
export GEMINI_API_KEY="your-key"
```
Or:
```
Lucy(api_key="your-key")
```
<br>

## 🧪 Example

from lucyai import Lucy

agent = Lucy()

@agent.tool
def search(q: str) -> str:
    return f"Searching: {q}"

print(agent.run("Find cauliflower recipes"))

<br>

## 🤖 Why LucyAI?

- Fast setup
- Multimodal by default
- Real tool calling
- Minimal boilerplate
- Pure Python

"If you can write a function, you can build an agent."

<br>

## 📋 Requirements

- Python 3.11+
- Gemini API key

<br>
## 📜 License

AGPL-3.0-only
