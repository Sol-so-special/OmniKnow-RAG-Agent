from pydantic import BaseModel, HttpUrl, Field

class QueryRequest(BaseModel):
    input: str = Field(..., min_length=1, max_length=50000)
    conversation_id: str | None = None

class WebDataRequest(BaseModel):
    url: HttpUrl

class PDFUploadResponse(BaseModel):
    message: str
    filename: str
    chunks_stored: int

class SearchResponse(BaseModel):
    query: str
    results: list[dict]
    num_results: int

class HealthResponse(BaseModel):
    status: str
    environment: str
    vector_store: str