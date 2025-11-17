from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import BaseTool

class GoogleSearchTool(BaseTool):
    name: str = "google_search"
    description: str = (
        "Perform a live Google search and return recent snippets or metadata relevant to the query. "
        "Use this for fresh information, news, or fact-checking. "
        "Input should be a search query string."
    )
    
    def _run(self, query: str) -> str:
        """Execute Google search."""
        search_wrapper = GoogleSearchAPIWrapper()
        return search_wrapper.run(query)