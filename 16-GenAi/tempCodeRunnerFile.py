
response = client.models.generate_content(

    model='gemini-2.5-flash', contents='I bought 5 pens at 3 rupees each and sold 2 pens at 4 rupees each. Did I make a profit or loss?',
    config=types.GenerateContentConfig(
        system_instruction= system_prompt,
         response_mime_type="application/json"
    )
)
print(response.text)