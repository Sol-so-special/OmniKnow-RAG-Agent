from fastapi import File, UploadFile, APIRouter
from starlette.responses import JSONResponse
from pydantic_models import QueryRequest
from pdf_data_collector import add_pdf_data, model, client
from pathlib import Path
from langchain_chroma import Chroma
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter() # Initialize router

UPLOAD_DIRECTORY = Path("uploads")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)  # Ensure the directory exists

@router.post("/add_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return JSONResponse(status_code=400, content={"error": "Only PDF allowed"})
    
    file_path = UPLOAD_DIRECTORY / file.filename
    with open(file_path, "wb") as pdf_file:
        pdf_file.write(await file.read())
    logger.info(f"File saved successfully: {file_path}")
        
    try:
        add_pdf_data(pdf_file_path=file_path)
        return JSONResponse(status_code=200, content={"message": "PDF file uploaded and processed successfully."})
    except Exception as e:
        logger.exception("Error while processing PDF")
        return JSONResponse(status_code=500, content={"error": f"Failed to process the PDF file: {str(e)}"})
    
@router.post("/search_query_in_pdf/")
async def query_messages(request: QueryRequest):
    query = request.input
    logger.info(f"Received query: {query}")
    
    try:
        db4 = Chroma(
            client=client,
            collection_name="pdf_data_collection",
            embedding_function=model,
        )
        
        results = db4.similarity_search(query=query, k=5)
        
        num_res = len(results)
        logger.info(f"PDF query '{query}' returned {num_res} result{'' if num_res < 2 else 's'}")
        
        structured_results = []
        for res in results:
            structured_results.append({
                "page_number": res.metadata.get("page_number"),
                "content": res.page_content
            })

        return JSONResponse(
            status_code=200,
            content={
                "query": query,
                "results": structured_results
            }
        )
        
    except Exception as e:
        logger.exception(f"Error during PDF query: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )