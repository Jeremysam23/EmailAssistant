import subprocess

MODEL = "llama3.2"

previous_email = "My package arrived damaged."
previous_reply = (
    "We apologize for the inconvenience. "
    "We will arrange a replacement after verification."
)

def ask_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", MODEL, prompt],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return "Error: Make sure Ollama is running and llama3.2 is installed."
    return result.stdout.strip()

def analyze_email(email):
    prompt = f"""
    Analyze this customer email:
    {email}

    Identify its intent in one short phrase, such as delivery issue,
    refund request, damaged product, or general inquiry.
    Return only the intent.
    """
    return ask_ollama(prompt)

def generate_reply(email, intent):
    prompt = f"""
    You are a professional customer support email assistant.

    Previous email: {previous_email}
    Previous reply: {previous_reply}

    Current customer email: {email}
    Detected intent: {intent}

    Write a concise, polite, professional email reply.
    Use the previous interaction only if relevant.
    Do not claim an action has been completed unless confirmed.
    Include a greeting and an appropriate closing.
    """
    return ask_ollama(prompt)

def main():
    print("\\n=== INTELLIGENT EMAIL ASSISTANT ===")

    while True:
        email = input("\\nEnter customer email (or 'exit'): ").strip()
        if email.lower() == "exit":
            print("Goodbye!")
            break
        if not email:
            continue

        print("\\nAnalyzing email...")
        intent = analyze_email(email)
        print("\\nDetected Intent:", intent)

        print("\\nGenerating reply...")
        reply = generate_reply(email, intent)
        print("\\nSuggested Reply:\\n")
        print(reply)

        with open("outputs/email_replies.txt", "a", encoding="utf-8") as f:
            f.write(
                f"Customer Email: {email}\\n"
                f"Intent: {intent}\\n"
                f"Suggested Reply: {reply}\\n"
                + "-" * 50 + "\\n"
            )
        print("\\nReply saved to outputs/email_replies.txt")

if __name__ == "__main__":
    main()
