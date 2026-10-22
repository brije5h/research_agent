import os

from dotenv import load_dotenv
from tavily import TavilyClient

from langchain_core.tools import tool

from research_agent.contracts.search_contracts import (
    SearchResponse,
    SearchResult,
)

load_dotenv()


class WebSearch:

    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY is not set in the environment."
            )

        self.client = TavilyClient(api_key=api_key)

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> SearchResponse:

        response = self.client.search(
            query=query,
            max_results=max_results,
        )
        
        #confusing
        results = [
            SearchResult(
                title=result["title"],
                url=result["url"],
                snippet=result.get("content", ""),
            )
            for result in response["results"]
        ]

        return SearchResponse(
            query=query,
            results=results,
        )


web_search_client = WebSearch()


@tool
def search_web(query: str) -> SearchResponse:
    """Search the web for information relevant to a research question.

    Use this tool when you need external information, supporting evidence,
    recent developments, or sources for a research task.
    """
    respone = web_search_client.search(
        query=query,
        max_results=5,
    )
    return respone.model_dump()


# if __name__ == "__main__":
#     print(search_web.name)
#     print(search_web.description)
#     print(search_web.args_schema.model_json_schema())