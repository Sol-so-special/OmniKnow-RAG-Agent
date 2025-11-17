from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from agent.prompt import get_agent_prompt
from tools.pdf_tool import PDFSearchTool
from tools.web_tool import WebSearchTool
from tools.google_tool import GoogleSearchTool
from core.config import get_settings
from functools import lru_cache

@lru_cache()
def get_agent_executor() -> AgentExecutor:
    """Singleton agent executor."""
    settings = get_settings()
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        max_retries=2,
        google_api_key=settings.gemini_api_key
    )
    
    # Initialize tools
    tools = [
        GoogleSearchTool(),
        PDFSearchTool(),
        WebSearchTool()
    ]
    
    # Create agent
    prompt = get_agent_prompt()
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
        max_execution_time=120  # 2 minutes
    )