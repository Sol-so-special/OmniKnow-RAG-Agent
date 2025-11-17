from langchain_core.tools import BaseTool
from pydantic import Field
import json

class PDFSearchTool(BaseTool):
    name: str = "pdf_search"
    description: str = (
        "Search stored PDF documents that were previously uploaded into the knowledge base. "
        "Returns relevant text segments with page numbers and source filenames. "
        "Input should be a search query string."
    )
    
    def _run(self, query: str) -> str:
        """Execute PDF search."""
        from services.pdf_service import PDFService
        pdf_service = PDFService()
        results = pdf_service.search(query, k=5)
        return json.dumps(results, indent=2)