from lucyai import Lucy
import time

agent = Lucy()

print("\n🚀 LucyAI Demo Starting...\n")
time.sleep(0.5)

# --- TOOL 1 ---
@agent.tool
def web_search(query: str) -> str:
    return f"[search results] Found results for: {query}"

# --- TOOL 2 ---
@agent.tool
def add(a: int, b: int) -> int:
    return a + b

print("🧠 Running agent...\n")
time.sleep(0.5)

# --- TEST 1: tool calling ---
response1 = agent.run("Search for pizza recipes")
print("💬 Prompt: Search for pizza recipes")
print("🤖 Response:", response1)

time.sleep(1)

# --- TEST 2: math tool ---
response2 = agent.run("What is 12 + 30?")
print("\n💬 Prompt: What is 12 + 30?")
print("🤖 Response:", response2)

time.sleep(1)

# --- TEST 3: memory ---
agent.run("My name is Johnny")
response3 = agent.run("What is my name?")

print("\n💬 Prompt: What is my name?")
print("🤖 Response:", response3)

print("\n✨ Demo complete.\n")