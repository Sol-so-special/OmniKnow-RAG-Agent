from langchain_core.tools import BaseTool
from pydantic import Field
import json

class WebSearchTool(BaseTool):
    name: str = "web_data_search"
    description: str = (
        "Search stored web page content that was previously added to the knowledge base. "
        "Returns relevant text chunks with source URLs. "
        "Input should be a search query string."
    )
    
    def _run(self, query: str) -> str:
        """Execute web search."""
        from services.web_service import WebService
        web_service = WebService()
        results = web_service.search(query, k=10)
        return json.dumps(results, indent=2)