from fastapi import APIRouter, BackgroundTasks, HTTPException
from models.schemas import WebDataRequest, QueryRequest, SearchResponse
from services.web_service import WebService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/web", tags=["Web"])

# Initialize web service
def get_web_service():
    return WebService()

@router.post("/scrape")
async def scrape_url(
    request: WebDataRequest,
    background_tasks: BackgroundTasks,
    force_reprocess: bool = False
):
    """Scrape and store web page."""
    web_service = get_web_service()
    
    try:
        # Queue scraping task with force flag
        background_tasks.add_task(
            web_service.process_url,
            str(request.url),
            force_reprocess
        )
        
        logger.info(f"Scraping queued for: {request.url}")
        return {"message": f"Scraping started for {request.url}"}
    except ValueError as e:
        # Duplicate detected
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        logger.exception("URL scraping failed")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@router.post("/search", response_model=SearchResponse)
async def search_web(request: QueryRequest):
    """Search web knowledge base."""
    web_service = get_web_service()
    
    try:
        results = web_service.search(request.input, k=10)
        
        return SearchResponse(
            query=request.input,
            results=results,
            num_results=len(results)
        )
    except Exception as e:
        logger.exception("Web search failed")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")