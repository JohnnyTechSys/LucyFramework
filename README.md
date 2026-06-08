<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>LucyAI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #0b0f17;
      color: #e8eefc;
      line-height: 1.5;
    }

    .container {
      max-width: 900px;
      margin: auto;
      padding: 40px 20px;
    }

    h1 {
      font-size: 48px;
      margin-bottom: 10px;
    }

    .tagline {
      font-size: 18px;
      color: #aab6d6;
      margin-bottom: 30px;
    }

    .hero {
      background: #121a2a;
      padding: 25px;
      border-radius: 12px;
      margin-bottom: 30px;
    }

    .code {
      background: #0a0f1d;
      padding: 15px;
      border-radius: 10px;
      overflow-x: auto;
      font-family: monospace;
      color: #9ef0ff;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 15px;
      margin-top: 20px;
    }

    .card {
      background: #121a2a;
      padding: 15px;
      border-radius: 10px;
    }

    .card h3 {
      margin-top: 0;
      color: #7ab8ff;
    }

    .section {
      margin-top: 40px;
    }

    .highlight {
      color: #7df9ff;
    }

    .footer {
      margin-top: 50px;
      font-size: 12px;
      color: #6b7896;
      text-align: center;
    }

    pre {
      margin: 0;
    }
  </style>
</head>

<body>

<div class="container">

  <!-- HERO -->
  <h1>🚀 LucyAI</h1>
  <div class="tagline">
    Turn Python functions into multimodal AI agents.
  </div>

  <div class="hero">
    <p>
      LucyAI is a lightweight framework for building AI agents with
      <span class="highlight">tool calling</span>,
      <span class="highlight">memory</span>, and
      <span class="highlight">multimodal inputs</span>.
    </p>

    <p>No graphs. No config files. No boilerplate.</p>

    <div class="code">
<pre>
from lucyai import Lucy

agent = Lucy()

@agent.tool
def search(query: str):
    return f"results for {query}"

print(agent.run("Search for pizza recipes"))
</pre>
    </div>
  </div>

  <!-- FEATURES -->
  <div class="section">
    <h2>⚡ Features</h2>

    <div class="grid">
      <div class="card">
        <h3>Simple API</h3>
        <p>Just Python functions → AI agents</p>
      </div>

      <div class="card">
        <h3>Tool Calling</h3>
        <p>Automatic function execution via LLM reasoning</p>
      </div>

      <div class="card">
        <h3>Multimodal</h3>
        <p>Images, audio, video, numpy, PIL support</p>
      </div>

      <div class="card">
        <h3>Memory</h3>
        <p>Built-in conversation history system</p>
      </div>

      <div class="card">
        <h3>Gemini Ready</h3>
        <p>Automatic fallback model chain</p>
      </div>

      <div class="card">
        <h3>Minimal</h3>
        <p>No heavy framework dependencies</p>
      </div>
    </div>
  </div>

  <!-- INSTALL -->
  <div class="section">
    <h2>📦 Installation</h2>

    <div class="code">
<pre>
uv add lucyai
# or
pip install lucyai
</pre>
    </div>
  </div>

  <!-- EXAMPLE -->
  <div class="section">
    <h2>🧠 Example</h2>

    <div class="code">
<pre>
from lucyai import Lucy

agent = Lucy()

response = agent.run("Hello!")
print(response)
</pre>
    </div>
  </div>

  <!-- WHY -->
  <div class="section">
    <h2>🤖 Why LucyAI?</h2>

    <p>
      Most AI frameworks require config files, graphs, and heavy abstractions.
    </p>

    <p>
      <span class="highlight">LucyAI removes all of that.</span>
    </p>

    <div class="grid">
      <div class="card">⚡ Fast setup</div>
      <div class="card">🧠 Multimodal by default</div>
      <div class="card">🔧 Real tool calling</div>
      <div class="card">🪶 Minimal boilerplate</div>
      <div class="card">🐍 Pure Python</div>
    </div>
  </div>

  <!-- PITCH -->
  <div class="section">
    <h2>💡 One-line pitch</h2>
    <div class="hero">
      Build multimodal AI agents in Python with just functions.
    </div>
  </div>

  <div class="footer">
    AGPL-3.0-only • LucyAI
  </div>

</div>

</body>
</html>
