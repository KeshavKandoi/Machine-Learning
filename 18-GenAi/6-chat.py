import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

system_prompt="""
  You are an helpful AI Assistant who is specialized in resolving user query.
  you work on start,plan,action,observe mode.
  For the given user query and available tools,plan the step by step execution based on the planning.
  select the relevant tool from the available tools and based on the tool selection you perform an action to call the tool.
  wait for the observation and based on the observation from the tool call resolve the user query.

  Rules:
  Follow the Output JSON Format.
  Always perform one step at a time and wait for next input.
  Carefully analyse the user query.
  Only use tools from the Available Tools list below. Do not invent tool names.
  The "input" field must always be a plain string, never a JSON object or dict.

  Available Tools:
  - get_weather(city: str): Returns the current weather for the given city.
    Example input: "delhi" or "new york" — pass only the city name as a plain string.

  Output JSON Format:
  {{
  "step":"string",
  "content":"string",
  "function":"The name of function if the step is action",
  "input":"The input parameter for the function as a plain string"
  }}

  Example:
  User Query: What is the weather of new york?
  output:{{"step":"plan","content":"The user is interested in weather data of new york"}}
  output:{{"step":"plan","content":"From the available tools I should call get_weather"}}
  output:{{"step":"action","function":"get_weather","input":"new york"}}
  output:{{"step":"observe","content":"new york: 12°C, clear sky, humidity 60%"}}
  output:{{"step":"output","content":"The weather for new york is 12°C with clear sky and humidity of 60%."}}
"""

API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "f668351e5606b81d754b29f3fe0bdce3"

def get_weather(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }
    res = requests.get(API_URL, params=params)
    data = res.json()

    if res.status_code != 200:
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    city_name   = data["name"]
    country     = data["sys"]["country"]
    temp        = data["main"]["temp"]
    feels_like  = data["main"]["feels_like"]
    humidity    = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    wind_speed  = data["wind"]["speed"]

    return (
        f"{city_name}, {country}: {temp}°C (feels like {feels_like}°C), "
        f"{description}, humidity {humidity}%, wind {wind_speed} m/s"
    )

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name and returns current weather from OpenWeatherMap"
    }
}

while True:
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    user_query = input("> ")

    if user_query.lower() in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=messages,
            response_format={"type": "json_object"}
        )

        reply = response.choices[0].message.content
        print(reply)

        try:
            parsed_output = json.loads(reply)
        except json.JSONDecodeError:
            messages.append({"role": "assistant", "content": reply})
            continue

        if not isinstance(parsed_output, dict):
            messages.append({"role": "assistant", "content": reply})
            continue

        messages.append({"role": "assistant", "content": reply})

        if parsed_output.get("step") == "action":
            tool_name  = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if tool_name in available_tools:
                observation = available_tools[tool_name]["fn"](tool_input)
            else:
                observation = f"Tool '{tool_name}' not found."

            observe_msg = json.dumps({"step": "observe", "content": str(observation)})
            print(observe_msg)
            messages.append({"role": "user", "content": observe_msg})
            continue

        if parsed_output.get("step") == "output":
            print("\nFinal Answer:", parsed_output.get("content"))
            break