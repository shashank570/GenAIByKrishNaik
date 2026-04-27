import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    temperature = 0.1
)

parser = StrOutputParser()

def chat():
    chat_history = [
        ("system", "You are a helpful chatbot. Be concise and accurate.")
    ]
    print("Langchain Chatbot. Type 'exit' to quit\n")
    while True:
        user_input = input("You : ").strip()
        if user_input.lower() == "exit":
            break
        chat_history.append(("user", user_input))
        prompt = ChatPromptTemplate.from_messages(chat_history)
        chain = prompt| llm | parser
        response = chain.invoke({})
        print(f"Bot: {response}\n")
        chat_history.append(("assistant", response))
        print("="*100)

chat()