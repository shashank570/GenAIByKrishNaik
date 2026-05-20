import re
from llama_index.core import PromptTemplate

from llm_factory.get_llm import get_ollama_llm


def get_chat_title(model, user_query):
    llm = get_ollama_llm(model)
    title_prompt_template = ("You are a helpful assistant that generates short, clear, and catchy titles.\n\n"
                       "Task:\n- Read the given user query.\n- Create a concise title (max 7 words).\n"
                       "- The title should summarize the intent of the query.\n"
                       "- Avoid unnecessary words, punctuation, or filler.\n"
                       "- Keep it professional and easy to understand.\n\n"
                       "User Query:\n{user_query}\n\n"
                       "Output:\nTitle:")
    title_prompt = PromptTemplate(title_prompt_template).format(user_query=user_query)
    title = llm.complete(prompt=title_prompt).text
    return title

def clean_title(title: str) -> str:
    """
    Cleans model-generated titles.
    """
    if not title:
        return "New Chat"

    # Remove markdown
    title = title.replace("*", "").replace('"', "").strip()

    # Remove common assistant phrases
    patterns = [
        r"^sure[,!: ]*",
        r"^here\s+is\s+the\s+title.*?:",
        r"^title\s*:",
        r"^suggested\s+title\s*:",
    ]

    for pattern in patterns:
        title = re.sub(pattern, "", title, flags=re.IGNORECASE).strip()

    # Keep only first line
    title = title.split("\n")[0].strip()

    # Limit length
    return title[:60] if title else "New Chat"


# Example usage
# model = "llama3:latest"
# user_query = "Can you explain the concept of reinforcement learning and its applications in modern AI"
# title = get_chat_title(model, user_query)
# print(title)

# NOTE: Smaller models (like gemma 2b) may not give you accurate and short title.