from langchain_core.tools import tool
import httpx
from bs4 import BeautifulSoup

from research_agent.contracts.source_read_contracts import (
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
        source_type="web",
    )


@tool
def read_source(url: str) -> SourceReadResponse:
    """Read the contents of a web source.

    Use this when a search result looks relevant and you need
    to inspect the actual source before using its claims as evidence.
    """
    return _read_source(url)
    