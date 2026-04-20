import ollama
from ollama import ChatResponse
from ollama import chat


response=ollama.chat(model="qwen:7b",messages=[
  {
  "role":"user",
  "content":"why sky is blue",
  }
],
 stream=True
 )
for chunk in response:
 print(chunk["message"]["content"],end="",flush=True)

