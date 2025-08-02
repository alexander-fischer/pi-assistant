import requests

from pia.config import LANGUAGE, MAX_WIKIPEDIA_CONTENT_LENGTH
from pia.nlp.tools.main import ToolResponse


def search_wikipedia(query: str) -> ToolResponse:
    search_url = f"https://{LANGUAGE}.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 1,
    }
    search_response = requests.get(search_url, params=search_params)
    search_data = search_response.json()

    if not search_data["query"]["search"]:
        tool_response = ToolResponse(message="No results found.", needs_rephrasing=True)
        return tool_response

    page_title = search_data["query"]["search"][0]["title"]
    content_url = f"https://{LANGUAGE}.wikipedia.org/w/api.php"
    content_params = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "extracts",
        "explaintext": True,
    }
    content_response = requests.get(content_url, params=content_params)
    content_data = content_response.json()

    page_id = next(iter(content_data["query"]["pages"]))
    page_content: str = content_data["query"]["pages"][page_id]["extract"]

    # limit to max content length to improve speed and quality
    page_content_words = page_content.split()
    capped_page_content = " ".join(page_content_words[:MAX_WIKIPEDIA_CONTENT_LENGTH])

    tool_response = ToolResponse(message=capped_page_content, needs_rephrasing=True)
    return tool_response
