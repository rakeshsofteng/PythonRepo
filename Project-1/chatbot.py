import openai

# Replace with your OpenAI API key
OPENAI_API_KEY = "your-api-key-here"

openai.api_key = OPENAI_API_KEY

def ask_chatgpt(question, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def main():
    print("ChatGPT Chatbot. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        answer = ask_chatgpt(user_input)
        print("Bot:", answer)

if __name__ == "__main__":
    main()