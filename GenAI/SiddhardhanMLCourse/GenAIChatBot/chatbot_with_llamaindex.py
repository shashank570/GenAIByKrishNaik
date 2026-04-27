import os
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.groq import Groq

os.environ["GROQ_API_KEY"] = "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"

llm = Groq(
    model = "llama-3.1-8b-instant",
    temperature = 0.1
)

def chat():
    chat_history = [
        ChatMessage(role=MessageRole.SYSTEM, content="You are a helpful assistant. Be concise and accurate.")
    ]
    print("Llama index Chatbot. Type 'exit' to quit \n")
    while True:
        user_input = input("You : ").strip()
        if user_input.lower() == 'exit':
            break
        chat_history.append(ChatMessage(role=MessageRole.USER, content=user_input))

        resp = llm.chat(messages=chat_history)
        answer = resp.message.content

        print(f"Bot : {answer}\n")
        chat_history.append(ChatMessage(role=MessageRole.ASSISTANT, content=answer))
        print("="*100)

chat()