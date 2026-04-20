import ollama
from ollama import ChatResponse

response=ollama.chat(model="qwen:7b",messages=[
  {
  "role":"user",
  "content":"why sky is blue"
  },
])
print(response.message.content)