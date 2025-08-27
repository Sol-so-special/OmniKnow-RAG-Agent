import streamlit as st
import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import pdf_tool, web_tool, google_tool
from prompt import prompt
from frontend.styling import apply_styling, render_user_message, render_ai_message

# Streamlit configuration
st.set_page_config(page_title="OmniKnow RAG Assistant")
apply_styling()   # Apply background gif and CSS styling for the sidebar

# Setup API Key with validation
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY is not set. Please set it in environment variables.")
    st.stop()
    
# Initialize tools/prompt in session state
if "pdf_tool" not in st.session_state:
    st.session_state.pdf_tool = pdf_tool()

if "web_tool" not in st.session_state:
    st.session_state.web_tool = web_tool()

if "google_tool" not in st.session_state:
    st.session_state.google_tool = google_tool()

if "prompt" not in st.session_state:
    st.session_state.prompt = prompt()

if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Initialize tracking of uploaded PDFs and accessed URLs
if "pdfs" not in st.session_state:
    st.session_state.pdfs = []
    
if "urls" not in st.session_state:
    st.session_state.urls = []
    
# Streamlit setup
st.title("📚🔎🌍 OmniKnow  ✨ RAG  🤖 Assistant")
st.markdown("<br><br>", unsafe_allow_html=True)

st.subheader("👋 Hi! I'm your RAG-powered assistant. Ask me about your PDFs, web pages, the latest from Google, or any other query on your mind! 😊")
st.markdown("___")

with st.sidebar:
    allow_reupload = st.checkbox("Allow re-upload", value=False)
    if not allow_reupload:
        st.warning('INFO: Re-uploading the same PDF or re-processing the same URL is disabled by default. Tick the checkbox "Allow re_upload" to enable both')
    else:
        st.warning('STATUS: ✅ PDF Re-upload and URL re-processing enabled')

    file_uploader = st.file_uploader("Upload your file:", type=["pdf"], key="file_input")
    if file_uploader is not None:
        file_str = str(file_uploader.name)
        if file_str not in st.session_state.pdfs or allow_reupload:
            response = requests.post(f"http://127.0.0.1:8000/add_pdf/", files={"file": file_uploader})
            if response.status_code == 200:
                st.success("✅ PDF document uploaded successfully")
                st.session_state.pdfs.append(file_str)
            else:
                st.error(f"Error: Failed to upload PDF. Status code: {response.status_code}")
                st.error("Response content: " + response.text)
                
    url = st.text_input("Enter URL", key="url_input").strip()
    if url:
        url_str = str(url.strip())
        if url_str not in st.session_state.urls or allow_reupload:
            if not url.startswith(('http://', 'https://')):
                st.error("Invalid URL format. Please ensure the URL starts with 'http://' or 'https://'.")
            else:
                response = requests.post(f"http://127.0.0.1:8000/scrape_webdata/", json={"url": url})
                if response.status_code in (200, 202):
                    st.success("✅ Web Data Extracted")
                    st.session_state.urls.append(url_str)
                else:
                    st.error(f"Error: Failed to extract web data. Status code: {response.status_code}")
                    st.error("Response content: " + response.text)
                                            
# Create the LangChain agent
if "agent_executor" not in st.session_state:
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", max_retries=2)
        
        # Setup tools
        tools = [
            st.session_state.google_tool,
            st.session_state.pdf_tool,
            st.session_state.web_tool
        ]
        
        agent = create_tool_calling_agent(llm, tools, st.session_state.prompt)
        st.session_state.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        st.stop()
    
# Show existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        render_user_message(message["content"])
    else:
        render_ai_message(message["content"])

# Handle query input and AI output
if query := st.chat_input("Enter your query:"):
    st.session_state.messages.append({"role": "user", "content": query})
    render_user_message(query)
    
    with st.spinner("Generating response..."):
        try:
            result = st.session_state.agent_executor.invoke({
                "input": query,
                "chat_history": st.session_state.messages[-1000:]
            })
            output = result["output"]
        except Exception as e:
            output = f"Sorry, I ran into an error: {e}"
        
    render_ai_message(output)
    st.session_state.messages.append({"role": "assistant", "content": output})