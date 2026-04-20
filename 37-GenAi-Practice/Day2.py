
import ollama
from ollama import ChatResponse
from ollama import chat


message=[]

print("write quit for exit")


while True:
  prompt=input("Enter your text:\n")

  if prompt.lower()=="quit":
    print("BYEE")
    break

  message.append(
    {
      "role":'user',
      "content":prompt
    }
  )

  response=ollama.chat(model="qwen:7b",messages=message,stream=True)
  
  full_response=""
  print("Bot: ", end="")

  for chunk in response:

    content=chunk["message"]["content"]
    print(content, end="", flush=True)
    full_response+=content

  message.append(
  {
  "role":'assistant',
  "content":full_response
  }
  )

