from pydantic import BaseModel

class QueryRequest(BaseModel):
    input: str
    
class WebDataRequest(BaseModel):
    url: str