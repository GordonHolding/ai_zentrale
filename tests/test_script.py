from agents.General_Agents.TextAgent.text_agent import generate_text

def main():
    prompt = "Was ist die Vision von DRESSCODE?"
    print("🧪 Test-Prompt:", prompt)
    output = generate_text(prompt)
    print("✅ Antwort vom TextAgent:")
    print(output)

if __name__ == "__main__":
    main()
