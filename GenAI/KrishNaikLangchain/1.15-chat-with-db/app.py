import streamlit as st
from pathlib import Path
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

# Constants
LOCALDB = "USE_LOCALDB"
POSTGRESDB = "USE_POSTGRESDB"

# Sidebar Options
radio_opt = [
    "Use SQLite3 Database - student.db",
    "Connect to your PostgreSQL Database"
]

selected_opt = st.sidebar.radio(
    label="Choose the DB which you want to chat with",
    options=radio_opt
)

# Database Selection
if radio_opt.index(selected_opt) == 1:

    db_uri = POSTGRESDB

    postgres_host = st.sidebar.text_input(
        "PostgreSQL Host",
        value="localhost"
    )

    postgres_port = st.sidebar.text_input(
        "PostgreSQL Port",
        value="5432"
    )

    postgres_user = st.sidebar.text_input(
        "PostgreSQL User",
        value="shashankshukla"
    )

    postgres_password = st.sidebar.text_input(
        "PostgreSQL Password",
        type="password"
    )

    postgres_db = st.sidebar.text_input(
        "PostgreSQL Database Name",
        value="postgres"
    )

else:
    db_uri = LOCALDB

# Groq API Key
api_key = st.sidebar.text_input(
    label="Groq API Key",
    type="password"
)

# Validation
if not api_key:
    st.info("Please add the Groq API key")
    st.stop()

# LLM
llm = ChatGroq(
    groq_api_key = api_key,
    model_name = "llama-3.3-70b-versatile",
    temperature = 0
)

# Configure DB
@st.cache_resource(ttl="2h")
def configure_db(
    db_uri,
    postgres_host=None,
    postgres_port=None,
    postgres_user=None,
    postgres_password=None,
    postgres_db=None
):

    # SQLite
    if db_uri == LOCALDB:

        dbfilepath = (Path(__file__).parent / "student.db").absolute()

        creator = lambda: sqlite3.connect(
            f"file:{dbfilepath}?mode=ro",
            uri=True
        )

        return SQLDatabase(
            create_engine(
                "sqlite:///",
                creator=creator
            )
        )

    # PostgreSQL
    elif db_uri == POSTGRESDB:

        if not (
            postgres_host and
            postgres_port and
            postgres_user and
            postgres_db
        ):
            st.error("Please provide PostgreSQL details")
            st.stop()

        # Allow blank password
        if postgres_password:
            postgres_url = (
                f"postgresql+psycopg2://"
                f"{postgres_user}:{postgres_password}"
                f"@{postgres_host}:{postgres_port}/{postgres_db}"
            )
        else:
            postgres_url = (
                f"postgresql+psycopg2://"
                f"{postgres_user}"
                f"@{postgres_host}:{postgres_port}/{postgres_db}"
            )

        return SQLDatabase(create_engine(postgres_url))


# Create DB connection
if db_uri == POSTGRESDB:

    db = configure_db(
        db_uri,
        postgres_host,
        postgres_port,
        postgres_user,
        postgres_password,
        postgres_db
    )

else:

    db = configure_db(db_uri)

# Toolkit
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=llm
)

# Agent
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="tool-calling",
    handle_parsing_errors=True,
    max_iterations=3
)

# Chat History
if (
    "messages" not in st.session_state
    or st.sidebar.button("Clear Message History")
):

    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "How can I help you?"
        }
    ]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User Input
user_query = st.chat_input(
    placeholder="Ask anything from the database"
)

# Handle Query
if user_query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):

        streamlit_callback = StreamlitCallbackHandler(
            st.container()
        )

        try:

            response = agent.invoke(
                {"input": user_query},
                config={
                    "callbacks": [streamlit_callback]
                }
            )

            output = response["output"]

            st.write(output)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": output
                }
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")