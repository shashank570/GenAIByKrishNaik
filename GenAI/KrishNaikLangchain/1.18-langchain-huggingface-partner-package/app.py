import validators
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser # LCEL (LangChain Expression Language) instead of load_summarize_chain
from langchain_community.document_loaders import (
    YoutubeLoader,
    UnstructuredURLLoader
)
from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace
)

st.set_page_config(
    page_title = "LangChain: Summarize Text From YT or Website",
    page_icon="🦜"
)

st.title("🦜 LangChain: Summarize Text From YT or Website using huggingface endpoint")
st.subheader("Summarize URL")

# Sidebar
with st.sidebar:
    hf_api_key = st.text_input("Huggingface API Token", value="", type="password")

generic_url = st.text_input("URL", label_visibility = "collapsed")

repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

prompt = ChatPromptTemplate.from_template("""
Provide a concise summary of the following content in around 300 words.

Content:
{text}
""")

# Output Parser 
output_parser = StrOutputParser()

# Button
if st.button("Summarize the Content from YT or Website"):
    if not hf_api_key.strip() or not generic_url.strip():
        st.error("Please provide the required information.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL.")
    else:
        try:
            with st.spinner("Loading content..."):

                llm = HuggingFaceEndpoint(
                    repo_id=repo_id,
                    task="conversational",
                    max_new_tokens=150,
                    temperature=0.7,
                    huggingfacehub_api_token=hf_api_key
                )

                chat_model = ChatHuggingFace(llm=llm)

                chain = prompt | chat_model | output_parser

                # Load documents
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(
                        generic_url,
                        add_video_info=False
                    )
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={ 
                            "User-Agent": ( 
                                "Mozilla/5.0 " 
                                "(Macintosh; Intel Mac OS X 13_5_1) " 
                                "AppleWebKit/537.36 " 
                                "(KHTML, like Gecko) " 
                                "Chrome/116.0.0.0 Safari/537.36" 
                                ) 
                            }
                    )
                docs = loader.load()

                # Combine document text
                final_text = "\n\n".join(doc.page_content for doc in docs)
                final_text = final_text[:12000]

                summary = chain.invoke({
                    "text": final_text
                })
                st.success(summary)

        except Exception as e:
            import traceback 
            st.error(f"Error: {str(e)}") 
            st.code(traceback.format_exc())