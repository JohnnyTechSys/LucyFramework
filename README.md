 LucyAI README

🚀 LucyAI
=========

**Turn Python functions into multimodal AI agents in seconds.**

No graphs. No config files. No boilerplate.  
Just Python → intelligent agents.

* * *

⚡ Why LucyAI?
-------------

Most AI frameworks force complexity:

*   Graphs
*   Pipeline systems
*   Config files
*   Extra abstraction layers

**LucyAI removes all of it.**

*   ✔ Function = Tool
*   ✔ Instant execution
*   ✔ Multimodal by default
*   ✔ Built-in memory
*   ✔ Zero boilerplate

_If you can write Python, you can build AI agents._

* * *

🎬 Live Demo
------------

Real tool calling + memory + no setup:

[![demo](https://asciinema.org/a/vUi5VWSTxZK2dyps.svg)](https://asciinema.org/a/vUi5VWSTxZK2dyps)

* * *

📦 Installation
---------------

    uv add lucyai

or

    pip install lucyai

* * *

🧠 Quick Start
--------------

    from lucyai import Lucy
    
    agent = Lucy()
    
    response = agent.run("Hello!")
    print(response)

* * *

🔧 Tool Calling
---------------

Turn Python functions into AI tools automatically:

    from lucyai import Lucy
    
    agent = Lucy()
    
    @agent.tool
    def get_time() -> str:
        return "3:00 PM"
    
    @agent.tool
    def add(a: int, b: int) -> int:
        return a + b

* * *

🖼️ Image Input
---------------

    agent.run("What is in this image?", imagedata="image.png")

Supported:

*   PNG
*   JPEG
*   Pillow Images
*   NumPy arrays
*   Raw bytes

* * *

🎧 Audio Input
--------------

    agent.run("Transcribe this audio", audiodata="audio.wav")

Supported:

*   WAV
*   MP3
*   Raw bytes

* * *

🎥 Video Input
--------------

    agent.run("Describe this video", videodata="video.mp4")

Supported:

*   MP4
*   Raw bytes

* * *

💭 Memory
---------

    agent = Lucy(history_limit=10)
    
    agent.run("My name is Johnny")
    agent.run("What is my name?")
    
    agent.clear_history()

* * *

🔑 API Keys
-----------

Environment variables:

*   GEMINI\_API\_KEY
*   HZAPIKEY

    export GEMINI_API_KEY="your-key"

Or:

    Lucy(api_key="your-key")

* * *

🧪 Example
----------

    from lucyai import Lucy
    
    agent = Lucy()
    
    @agent.tool
    def search(q: str) -> str:
        return f"Searching: {q}"
    
    print(agent.run("Find cauliflower recipes"))

* * *

🤖 Why LucyAI?
--------------

*   Fast setup
*   Multimodal by default
*   Real tool calling
*   Minimal boilerplate
*   Pure Python

**If you can write a function, you can build an AI agent.**

* * *

📋 Requirements
---------------

*   Python 3.11+
*   Gemini API key

* * *

📜 License
----------

AGPL-3.0-only
