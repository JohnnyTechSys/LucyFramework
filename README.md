//==============================//
// LUCYAI::DOC v1.0 (pseudo-lang)
// renderer: markdown-compatible
// license: AGPL-3.0-only
//==============================//

#> 🚀 LucyAI

##::meta
title = "LucyAI"
tagline = "Turn Python functions into multimodal AI agents"
mode = "agent-framework"
language = "python + gemini-tools"
::end

##::intro
LucyAI is a lightweight framework for building AI agents with tool calling,
memory, and multimodal inputs in pure Python.

No graphs. No config files. No boilerplate.

Just Python → agents.
::end

##::example.block python
from lucyai import Lucy

agent = Lucy()

@agent.tool
def search(query: str):
    return f"results for {query}"

print(agent.run("Search for pizza recipes"))
::end

##::features.block
- Simple Python-first API
- Automatic tool calling
- Type-hint → tool schema generation
- Conversation memory
- Image / Audio / Video inputs
- NumPy + Pillow support
- Gemini integration w/ fallback chain
- Minimal dependencies
- Python 3.11+
::end

##::install.block bash
uv add lucyai
# or
pip install lucyai
::end

##::quickstart.block python
from lucyai import Lucy

agent = Lucy()

print(agent.run("Hello!"))
::end

##::tools.block python
@agent.tool
def get_time() -> str:
    return "3:00 PM"

@agent.tool
def add(a: int, b: int) -> int:
    return a + b
::end

##::media.support
image: PNG, JPEG, PIL, NumPy
audio: WAV, MP3, raw bytes
video: MP4, raw bytes
::end

##::memory.block
agent = Lucy(history_limit=10)

agent.run("My name is Johnny")
agent.run("What is my name?")

agent.clear_history()
::end

##::env.block
GEMINI_API_KEY or HZAPIKEY

export GEMINI_API_KEY="your-api-key"
::end

##::example.full python
from lucyai import Lucy

agent = Lucy()

@agent.tool
def search(query: str) -> str:
    return f"Searching for: {query}"

print(agent.run("Search cauliflower recipes"))
::end

##::why
LucyAI removes complexity:

- fast setup
- multimodal by default
- real tool calling
- minimal boilerplate
- pure Python

"If you can write a function, you can build an agent."
::end

##::requirements
Python >= 3.11
Gemini API key
::end

##::license
AGPL-3.0-only
::end

//==============================//
// END LUCYAI::DOC
//==============================//
