# Astra DB is a fully managed, serverless database service from DataStax built on the Apache Cassandra database. 
# It is widely used for AI applications, Retrieval-Augmented Generation (RAG), vector search, and large-scale NoSQL workloads.

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA


ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


loader = PyPDFLoader("attention.pdf")
documents = loader.load()
print(f"Total Pages Loaded: {len(documents)}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

docs = text_splitter.split_documents(documents)
print(f"Total Chunks Created: {len(docs)}")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

astra_vector_store = AstraDBVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="pdf_rag_demo",
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
)

print("Documents inserted into Astra DB")

retriever = astra_vector_store.as_retriever(search_kwargs={"k": 3})

llm = ChatGroq(groq_api_key = GROQ_API_KEY, model_name = "llama-3.1-8b-instant")

qa_chain = RetrievalQA.from_chain_type(
    llm = llm,
    retriever = retriever,
    chain_type="stuff"
)

while True:
    query = input("\nAsk Question: ")

    if query.lower() == "exit": 
        break
    
    response = qa_chain.invoke({"query": query})

    print("\nAnswer:") 
    print(response["result"])

