import requests

from pia.config import LANGUAGE
from pia.nlp.tools.main import ToolResponse


def search_wikipedia(query: str) -> ToolResponse:
    headers = {
        "User-Agent": "pi-assistant (https://github.com/alexander-fischer/pi-assistant)"
    }

    search_url = f"https://{LANGUAGE}.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 1,
    }
    search_response = requests.get(search_url, params=search_params, headers=headers)
    search_response.raise_for_status()
    search_data = search_response.json()

    if not search_data["query"]["search"]:
        tool_response = ToolResponse(message="No results found.", needs_rephrasing=True)
        return tool_response

    page_title = search_data["query"]["search"][0]["title"]
    content_url = (
        f"https://{LANGUAGE}.wikipedia.org/api/rest_v1/page/summary/{page_title}"
    )
    content_response = requests.get(content_url, headers=headers)
    content_data = content_response.json()
    content_summary = content_data.get("extract", "")

    tool_response = ToolResponse(message=content_summary, needs_rephrasing=True)
    return tool_response
