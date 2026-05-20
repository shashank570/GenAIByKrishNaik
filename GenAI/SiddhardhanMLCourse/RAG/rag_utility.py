import os
from dotenv import load_dotenv


from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA

load_dotenv()

working_dir = os.path.dirname(os.path.abspath((__file__)))

embedding = HuggingFaceEmbeddings()

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    temperature = 0
)


def process_documents_to_chroma_db(file_name):
    loader = UnstructuredPDFLoader(f"{working_dir}/{file_name}")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 200
    )
    chunks = text_splitter.split_documents(documents)
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory = f"{working_dir}/doc_vectorstore"
    )
    return 0

def answer_question(user_question):
    vector_db = Chroma(
        persist_directory = f"{working_dir}/doc_vectorstore",
        embedding_function = embedding
    )

    retriever = vector_db.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = "stuff",
        retriever = retriever
    )

    response = qa_chain.invoke({"query" : user_question})
    answer = response["result"]
    return answer