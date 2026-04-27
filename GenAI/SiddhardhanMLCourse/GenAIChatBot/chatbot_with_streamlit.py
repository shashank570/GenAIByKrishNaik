from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

load_dotenv()

# streamlit page setup this will apprear at top of the tab of webpage
st.set_page_config(
    page_title = "Chatbot",
    page_icon = "🤖",
    layout = "centered"
)

st.title("💬 Generative AI Chatbot")

# initiate chat history -> this is require because with every user interaction (click to submit buttom in user input) 
# the stremlit app reruns again and read the whole script
# we will first check if chat_history already exist in session state -> 
# if not present -> create it as an empty list
# if present -> keep existing data
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# show chat history
for message in st.session_state.chat_history:
    # message["role"] decides styling: Streamlit automatically formats it nicely :
    # if it is a user role then it will create a user chat bubble 
    # if it is assitant role then it will create a assistant bubble
    with st.chat_message(message["role"]):
        # Renders the message text: supports bold, italics, code block, links
        st.markdown(message["content"])

# llm initiate
llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    temperature = 0
)

# input box
# flow -> User types → show user message → save → send full history → get response → save → display
user_prompt = st.chat_input("Ask Chatbot....")
if user_prompt:
    # Displays user message in chat bubble
    st.chat_message("user").markdown(user_prompt)
    # Adds user message to persistent chat_history
    st.session_state.chat_history.append({"role" : "user", "content" : user_prompt})

    # *st.session_state.chat_history -> unpacks the entire chat history
    # llm will receive below
    # [
    #     {"role": "system", "content": "..."},
    #     {"role": "user", "content": "..."},
    #     {"role": "assistant", "content": "..."},
    #     {"role": "user", "content": "..."}
    # ]
    response = llm.invoke(
        input = [{"role" : "system", "content" : "You are a helpful assistant"}, *st.session_state.chat_history]
    )

    assistant_response  = response.content
    # Adds assistant message to persistent chat_history
    st.session_state.chat_history.append({"role" : "assistant", "content" : assistant_response})
    # Displays assistant message in chat bubble
    st.chat_message("assistant").markdown(assistant_response)