from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
from models.schemas import QueryRequest, PDFUploadResponse, SearchResponse
from services.pdf_service import PDFService
from services.storage import StorageService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/pdf", tags=["PDF"])

# Initialize pdf service
def get_pdf_service():
    return PDFService()

# Storage management
def get_storage_service():
    return StorageService()

@router.post("/upload", response_model=PDFUploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    force_reprocess: bool = False
):
    """Upload and process PDF."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    # Instantiate services when needed
    storage_service = get_storage_service()
    pdf_service = get_pdf_service()
    
    # Read file content
    content = await file.read()
    
    # Save to storage
    storage_path = storage_service.save_file(file.filename, content)
    logger.info(f"Saved PDF: {storage_path}")
    
    try:
        # Get path for processing
        processing_path = storage_service.get_file_path(file.filename)
        
        # Process PDF
        chunks_stored = pdf_service.process_pdf(Path(processing_path), force_reprocess=force_reprocess)
        
        return PDFUploadResponse(
            message="PDF uploaded and processed successfully",
            filename=file.filename,
            chunks_stored=chunks_stored
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        logger.exception("PDF processing failed")
        raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")

@router.post("/search", response_model=SearchResponse)
async def search_pdf(request: QueryRequest):
    """Search PDF knowledge base."""
    pdf_service = get_pdf_service()
    
    try:
        results = pdf_service.search(request.input, k=5)
        
        return SearchResponse(
            query=request.input,
            results=results,
            num_results=len(results)
        )
    except Exception as e:
        logger.exception("PDF search failed")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")