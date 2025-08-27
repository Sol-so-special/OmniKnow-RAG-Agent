from pdf_wrapper import PDFSearchAPIWrapper
from web_wrapper import WebSearchAPIWrapper
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.tools import StructuredTool

# Configure Google Search tool
def google_tool():
    google_search = GoogleSearchAPIWrapper()
    google_tool = StructuredTool.from_function(
        func=google_search.run,
        name="google_search",
        description="Perform a live Google search and return recent snippets or metadata relevant to the user query."
    )
    return google_tool

# Configure Web URL Search tool
def web_tool():
    web_data_search = WebSearchAPIWrapper()
    web_tool = StructuredTool.from_function(
        func=web_data_search.run,
        name="web_data_search",
        description="Search stored web page content that was previously added to the knowledge base and return relevant text chunks."
    )
    return web_tool

# Configure PDF Search tool
def pdf_tool():
    pdf_search = PDFSearchAPIWrapper()
    pdf_tool = StructuredTool.from_function(
        func=pdf_search.run,
        name="pdf_search",
        description="Search stored PDF documents that were previously uploaded into the knowledge base and return relevant text segments."
    )
    return pdf_tool