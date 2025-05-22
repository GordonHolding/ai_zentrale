def generate_text(prompt: str, model="gpt-3.5-turbo") -> str:
    from openai import OpenAI
    import os
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        {"role": "system", "content": "Du bist eine professionelle Text-KI für die Gordon Holding."},
        {"role": "user", "content": prompt}
    ]
    completion = client.chat.completions.create(model=model, messages=messages)
    return completion.choices[0].message.content
