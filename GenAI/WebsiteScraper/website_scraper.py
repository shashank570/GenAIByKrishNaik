import os
from dotenv import load_dotenv
load_dotenv()
import httpx
import trafilatura
from playwright.sync_api import sync_playwright
from openai import OpenAI

# =========================
# CONFIG
# =========================
TIMEOUT = 15
MAX_INPUT_CHARS = 12000  # prevent token overflow

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ Please set GROQ_API_KEY as environment variable")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# =========================
# FETCH (HTTP)
# =========================
def fetch_url(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}

    with httpx.Client(timeout=TIMEOUT, follow_redirects=True) as client_http:
        response = client_http.get(url, headers=headers)
        response.raise_for_status()
        return response.text, str(response.url)


# =========================
# FETCH (BROWSER FALLBACK)
# =========================
def fetch_with_browser(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")

        content = page.content()
        browser.close()
        return content


# =========================
# PRIVATE PAGE DETECTION
# =========================
def is_private_page(html: str, url: str) -> bool:
    html_lower = html.lower()
    url_lower = url.lower()

    strong_indicators = [
        "access denied",
        "403 forbidden",
        "not authorized",
        "unauthorized",
        "please log in",
        "please sign in"
    ]

    # URL-based detection (strict)
    if any(x in url_lower for x in ["/login", "/signin", "/auth"]):
        return True

    # HTML-based detection (strict phrases only)
    if any(ind in html_lower for ind in strong_indicators):
        return True

    return False


# =========================
# EXTRACT CLEAN TEXT
# =========================
def extract_text(html: str) -> str:
    return trafilatura.extract(html) or ""


# =========================
# LLM SUMMARIZATION
# =========================
def summarize(text: str) -> str:
    text = text[:MAX_INPUT_CHARS]

    prompt = f"""
You are an expert content summarizer.

Summarize the following webpage content into a clear explanation of at least 200 words.

Guidelines:
- Focus on main topic and key ideas
- Ignore navigation, ads, login prompts
- Keep it professional and concise
- Single paragraph output
- Do not hallucinate

Content:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


# =========================
# MAIN PIPELINE
# =========================
def process_url(url: str) -> dict:
    try:
        print(f"\n🌐 Processing: {url}")

        # Step 1: Try HTTP fetch
        try:
            html, final_url = fetch_url(url)
        except Exception:
            print("⚠️ HTTP failed, using browser...")
            html = fetch_with_browser(url)
            final_url = url

        # Step 2: Detect private/login page
        if is_private_page(html, final_url):
            return {"url": url, "error": "private url"}

        # Step 3: Extract main content
        text = extract_text(html)

        if len(text.strip()) < 200:
            return {"url": url, "error": "unable to extract content"}

        # Step 4: Summarize
        summary = summarize(text)

        return {"url": url, "summary": summary}

    except Exception as e:
        return {"url": url, "error": str(e)}


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://blogs.mulesoft.com/author/astonwhiteling/",
        "https://basecamp.salesforce.com/content/sales-revops-salesforce-only-sending-docusign-and-pdf-quote"
    ]

    for url in urls:
        result = process_url(url)

        print("\n===== RESULT =====")
        print(result)