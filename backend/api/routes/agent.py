from fastapi import APIRouter, HTTPException
from models.schemas import QueryRequest
from agent.executor import get_agent_executor
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/chat")
async def chat(request: QueryRequest):
    """Chat with the RAG agent."""
    try:
        agent_executor = get_agent_executor()
        
        result = agent_executor.invoke({
            "input": request.input,
            "chat_history": []  # Simplified for now
        })
        
        return {"output": result["output"]}
    except Exception as e:
        logger.exception("Agent chat failed")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")