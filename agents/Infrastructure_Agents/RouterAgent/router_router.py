import openai
from agents.Infrastructure_Agents.RouterAgent.router_prompt_loader import load_identity_prompt, load_dynamic_router_prompt

def determine_agent(user_input):
    prompt = load_identity_prompt() + "\n\n" + load_dynamic_router_prompt()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message["content"].strip()
        return reply
    except Exception as e:
        return f"Routing-Fehler: {e}"
