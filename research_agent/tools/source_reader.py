from langchain_core.tools import tool
import httpx
from bs4 import BeautifulSoup

from research_agent.contracts.research_contracts import (
    SourceReadResponse,
)

def _read_source(url: str) -> SourceReadResponse:

    response = httpx.get(
        url,
        timeout=15,
        follow_redirects=True,
        headers={
            "User-Agent": "ResearchEngineerAgent/0.1"
        },
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    # Remove elements that aren't useful research content.
    for element in soup(
        ["script", "style", "nav", "footer"]
    ):
        element.decompose()

    content = soup.get_text(
        separator="\n",
        strip=True,
    )

    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else url
    )

    return SourceReadResponse(
        url=url,
        title=title,
        content=content,
        source_type="other",
    )


@tool
def read_source(url: str) -> dict:
    """Reads and extracts the full text content from a given web URL. 

    Use this tool after finding relevant URLs via search_web to get detailed evidence.
    
    Args:
        url: The web URL to read.
    """
    return _read_source(url).model_dump()

    