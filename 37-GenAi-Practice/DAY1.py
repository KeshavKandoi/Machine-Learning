import ollama
from ollama import ChatResponse
from ollama import chat

prompt=input("Enter your text ")

response=ollama.chat(model="qwen:7b",messages=[
  {
  "role":"user",
  "content":prompt,
  }
],
 stream=True
 )
for chunk in response:
 print(chunk["message"]["content"],end="",flush=True)

