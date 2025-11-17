from functools import lru_cache
from agent.executor import get_agent_executor
from services.pdf_service import PDFService
from services.web_service import WebService

@lru_cache()
def get_pdf_service() -> PDFService:
    return PDFService()

@lru_cache()
def get_web_service() -> WebService:
    return WebService()

@lru_cache()
def get_agent():
    return get_agent_executor()