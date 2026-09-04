import requests
from bs4 import BeautifulSoup


def fetch_job_posting(url: str) -> dict:

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; JobPilotBot/1.0)"},
            timeout=10,
        )
        response.raise_for_status()
    except response.RequestException as e:

        return {"error": f"Could not fetch URL: {str(e)}"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    text = "\n".join(line for line in text.splitlines() if line.strip())

    max_chars = 8000
    if len(text) > max_chars:
        text = text[:max_chars]

    return {"text": text, "source_url": url}