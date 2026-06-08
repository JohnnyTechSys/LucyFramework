# Lucy Framework

A lightweight multimodal AI agent framework for Python.

Lucy makes it easy to build AI agents with automatic tool calling, conversation history, and multimodal input support using a simple Python API.

## Features

* Simple API
* Automatic tool calling
* Automatic tool schema generation from Python type hints
* Conversation history management
* Image input support
* Audio input support
* Video input support
* NumPy image support
* Pillow image support
* Built-in Gemini integration
* Automatic model fallback chain
* Minimal dependencies
* Python 3.11+

---

## Installation

```bash
uv add lucyframework
```

or

```bash
pip install lucyframework
```

---

## Quick Start

```python
from lucyframework import Lucy

agent = Lucy()

response = agent.run("Hello!")

print(response)
```

---

## Tool Calling

Register tools using a simple decorator.

```python
from lucyframework import Lucy

agent = Lucy()

@agent.tool
def get_time() -> str:
    """Returns the current time."""
    return "3:00 PM"

result = agent.run("What time is it?")

print(result)
```

Tools are automatically converted into Gemini function declarations using Python type hints.

```python
@agent.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

---

## Image Input

```python
from lucyframework import Lucy

agent = Lucy()

result = agent.run(
    "What is in this image?",
    imagedata="image.png"
)

print(result)
```

Supported image formats:

* PNG
* JPEG
* Pillow Images
* NumPy Arrays
* Raw Bytes

---

## Audio Input

```python
result = agent.run(
    "Transcribe this audio.",
    audiodata="audio.wav"
)
```

Supported formats:

* WAV
* MP3
* Raw Bytes

---

## Video Input

```python
result = agent.run(
    "Describe this video.",
    videodata="video.mp4"
)
```

Supported formats:

* MP4
* Raw Bytes

---

## Conversation History

Lucy automatically maintains conversation history.

```python
agent = Lucy(history_limit=10)

agent.run("My name is Johnny.")
agent.run("What is my name?")
```

Clear history:

```python
agent.clear_history()
```

---

## API Key

Lucy automatically searches for:

```bash
GEMINI_API_KEY
```

or

```bash
HZAPIKEY
```

Example:

```bash
export GEMINI_API_KEY="your-api-key"
```

You can also provide the key directly:

```python
agent = Lucy(api_key="your-api-key")
```

---

## Example

```python
from lucyframework import Lucy

agent = Lucy()

@agent.tool
def search(query: str) -> str:
    return f"Searching for: {query}"

response = agent.run(
    "Search for cauliflower recipes."
)

print(response)
```

---

## Why Lucy?

Many AI frameworks require large configuration files, complex setup, and multiple abstractions before you can build an agent.

Lucy focuses on:

* Simplicity
* Fast setup
* Multimodal support
* Practical tool calling
* Minimal boilerplate

If you can write a Python function, you can build a Lucy tool.

---

## Requirements

* Python 3.11+
* Gemini API key

---

## License

AGPL 3.0