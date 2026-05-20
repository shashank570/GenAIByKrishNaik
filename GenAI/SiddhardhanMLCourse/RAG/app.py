import os
import streamlit as st
from rag_utility import answer_question, process_documents_to_chroma_db

working_dir = os.path.dirname(os.path.abspath((__file__)))

st.title("🦙 Llama-3.1-8B - Document RAG")

uploaded_file = st.file_uploader("Upload a PDF File", type=["pdf"])

if uploaded_file is not None:
    save_path = os.path.join(working_dir, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    process_document = process_documents_to_chroma_db(uploaded_file.name)
    st.info("Document Processed Successfully")

user_question = st.text_area("Ask your question about the document")

if st.button("Answer"):
    answer = answer_question(user_question)

    st.markdown("### Llama-3.1-8B Response")
    st.markdown(answer)