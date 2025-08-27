import requests
from typing import Optional
from langchain_core.callbacks import CallbackManagerForToolRun
from pydantic import BaseModel, ConfigDict
from langchain_core.tools import BaseTool

class PDFSearchAPIWrapper(BaseModel):
    """Wrapper for PDF Search API."""
    api_url: str = "http://127.0.0.1:8000"  # The API URL for searching stored PDFs
    k: int = 10  # The number of results to return
    model_config = ConfigDict(extra="forbid")

    def _pdf_search_results(self, search_term: str) -> str:
        import requests
        response = requests.post(f"{self.api_url}/search_query_in_pdf/", json={"input": search_term})
        if response.status_code == 200:
            return response.json()
        else:
            return "❌ Failed to fetch results!"

    def run(self, query: str) -> str:
        """Run query through PDF Search and parse the result."""
        return self._pdf_search_results(query)

class PDFSearchRun(BaseTool):
    """Tool for searching stored PDF documents."""
    name: str = "pdf_search"
    description: str = (
        "A wrapper around the PDF Search API. "
        "Useful for retrieving relevant information from PDF documents that were previously uploaded into the knowledge base. "
        "Input should be a search query."
    )
    api_wrapper: PDFSearchAPIWrapper

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)