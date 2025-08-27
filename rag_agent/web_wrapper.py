import requests
from typing import Optional
from langchain_core.callbacks import CallbackManagerForToolRun
from pydantic import BaseModel, ConfigDict
from langchain_core.tools import BaseTool

class WebSearchAPIWrapper(BaseModel):
    """Wrapper for Web Search API."""
    api_url: str = "http://127.0.0.1:8000"  # The API URL for searching stored web pages
    k: int = 10  # The number of results to return
    model_config = ConfigDict(extra="forbid")
    
    def _web_search_results(self, search_term: str) -> str:
        response = requests.post(f"{self.api_url}/search_query_in_web/", json={"input": search_term})
        if response.status_code == 200:
            return response.json()
        else:
            return "❌ Failed to fetch results!"

    def run(self, query: str) -> str:
        """Run query through Web Data Search and parse the result."""
        return self._web_search_results(query)

class WebSearchRun(BaseTool):
    """Tool for searching stored web page content."""
    name: str = "web_data_search"
    description: str = (
        "A wrapper around the Web Search API. "
        "Useful for retrieving relevant information from web pages that were previously ingested into the knowledge base. "
        "Input should be a search query."
    )
    api_wrapper: WebSearchAPIWrapper

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)