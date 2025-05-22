def summarize_text(text):
    from openai import OpenAI
    import os
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Fasse diesen Text so präzise wie möglich zusammen."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content
