from llama_index.llms.ollama import Ollama
from config.settings import Settings

settings = Settings()
OLLAMA_URL = settings.OLLAMA_URL

# Module-level cache for model and instance
# manual in-memory caching (also called a singleton-style cache for one object at a time).
# These are module-level global variables
# they are stored in global name space
# so every time it checks into global name space and if there are any values
# the same is used initialized as None for the first time

_current_model_name = None
_current_llm_instance = None

def get_ollama_llm(model_name: str):
    global _current_model_name, _current_llm_instance # this mean i am refering to global variables so do not create loacl variable
    if _current_model_name == model_name and _current_llm_instance is not None:
        return _current_llm_instance
    llm = Ollama(base_url=OLLAMA_URL, model=model_name)
    _current_model_name = model_name
    _current_llm_instance = llm
    return llm


# Example usage -> (convo_pro_chat_gpt_clone) shashankshukla@Shashanks-MacBook-Pro convo_pro_chat_gpt_clone % python -m llm_factory.get_llm

# check_llm = get_ollama_llm(model_name="llama3:latest")
# print(f"check_llm -> {check_llm}")
# print(f"type -> {type(check_llm)}")