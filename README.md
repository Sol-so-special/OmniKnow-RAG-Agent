# ✨ **OmniKnow RAG Agent** 📚🔎🌍

A powerful Retrieval-Augmented Generation (RAG) agent that combines PDF documents, web content, and real-time Google search capabilities to provide comprehensive answers to user queries. Built with FastAPI, Streamlit, and LangChain.

___

## 🌟 Features

### Multi-Source Knowledge Integration
- **📄 PDF Processing**: Upload and query PDF documents with intelligent chunking and semantic search
- **🌐 Web Content Extraction**: Scrape and index web pages for future querying
- **🔍 Real-time Google Search**: Access fresh, up-to-date information from the web
- **🤖 Intelligent Agent**: LangChain-powered agent that automatically selects the best information source

### Advanced RAG Capabilities
- **🧠 Semantic Search**: Uses HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2) for accurate similarity matching
- **💾 Vector Storage**: ChromaDB for efficient document storage and retrieval
- **🔧 Smart Tool Selection**: Automatically chooses between PDF search, web search, or Google search based on query context
- **📊 Structured Results**: Returns relevant chunks with metadata including page numbers and source URLs

### User Experience
- **🎨 Custom UI**: Beautiful Streamlit interface with animated background and custom styling
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **⚡ Real-time Processing**: Background tasks for web scraping with immediate feedback
- **🔄 Re-upload Prevention**: Intelligent duplicate detection to prevent redundant processing

___

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │   ChromaDB      │
│   Frontend      │◄──►│   Backend       │◄──►│   Vector Store  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LangChain     │    │   Tool System   │    │   Google API    │
│   Agent         │◄──►│   (PDF/Web/     │◄──►│   Search        │
│                 │    │   Google)       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

___

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key
- Google Search API key
- Google CSE ID

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sol-so-special/OmniKnow-RAG-Agent
   cd rag_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Required
   export GEMINI_API_KEY="your_gemini_api_key_here"
   export GOOGLE_API_KEY="your_google_api_key"
   export GOOGLE_CSE_ID="your_custom_search_engine_id"
   
   # optional
   export SESSION_SECRET="your_secret"  # app has session middleware commented out
   ```

4. **Start the FastAPI backend**
   ```bash
   uvicorn api:app --host 127.0.0.1 --port 8000
   ```

5. **Launch the Streamlit frontend** (in a new terminal)
   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   - Open your browser to `http://localhost:8501`
   - The FastAPI docs are available at `http://localhost:8000/docs`

___

## 📖 Usage Guide

### Adding Content Sources

**Upload PDF Documents:**
1. Use the file uploader in the sidebar
2. Select PDF files to upload
3. Wait for processing confirmation
4. Your PDFs are now searchable via chat

**Add Web Pages:**
1. Enter a URL in the sidebar text input
2. Ensure the URL starts with `http://` or `https://`
3. Click enter to start scraping
4. The web content becomes searchable once processed

### Chatting with OmniKnow

Simply type your questions in the chat interface. OmniKnow will automatically:

- Search your uploaded PDFs for relevant content
- Query indexed web pages for related information  
- Perform live Google searches for fresh data
- Combine results intelligently to provide comprehensive answers

### Example Queries

```
"What does the research paper say about machine learning?"
"Summarize the main points from the uploaded documents"
"What's the latest news about artificial intelligence?"
"Find information about the company mentioned in the web page"
```

___

## 🔧 API Endpoints

### PDF Operations
- `POST /add_pdf/` - Upload and process PDF documents
- `POST /search_query_in_pdf/` - Search within uploaded PDFs

### Web Content Operations  
- `POST /scrape_webdata/` - Extract and index web page content
- `POST /search_query_in_web/` - Search within indexed web pages

### Request/Response Examples

**Upload PDF:**
```bash
curl -X POST "http://127.0.0.1:8000/add_pdf/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

**Search PDFs:**
```bash
curl -X POST "http://127.0.0.1:8000/search_query_in_pdf/" \
  -H "Content-Type: application/json" \
  -d '{"input": "machine learning algorithms"}'
```

___

## 🏗️ Project Structure

```
rag_agent/
├── api_endpoints/         # FastAPI route handlers
│   ├── pdf_api.py         # PDF upload and search endpoints
│   └── web_api.py         # Web scraping and search endpoints
├── demo/                  # Demo videos and screenshots
├── frontend/              # UI components and styling
│   ├── background.gif     # Animated background
│   └── styling.py         # Custom CSS and UI functions
├── upload/                # Auto-created directory for PDF storage
├── api.py                 # FastAPI application setup
├── app.py                 # Streamlit main application
├── pdf_data_collector.py  # PDF processing and ChromaDB integration
├── pdf_wrapper.py         # LangChain tool wrapper for PDF search
├── prompt.py              # System prompt and agent configuration
├── pydantic_models.py     # Request/response data models
├── tools.py               # LangChain tool definitions
├── web_data_collector.py  # Web scraping and ChromaDB integration
├── web_wrapper.py         # LangChain tool wrapper for web search
└── requirements.txt       # Python dependencies
```

___

## ⚙️ Configuration

### Environment Variables

| Variable (Required) | Description |
|---------------------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key for the LLM |
| `GOOGLE_API_KEY` | Google API key for Google search |
| `GOOGLE_CSE_ID` | Custom Search Engine ID |

### Customization Options

**Adjust Chunk Sizes:**
- Modify `chunk_size` and `chunk_overlap` in `web_data_collector.py`
- Default: 800 characters with 100 character overlap

**Change Embedding Model:**
- Update the model name in data collector files
- Current: `sentence-transformers/all-MiniLM-L6-v2`

**Modify Search Results:**
- Adjust the `k` parameter in wrapper classes
- Controls number of results returned per search

___

## 🔍 Monitoring & Logging

- **API Logs**: Comprehensive logging to `api.log`
- **Prometheus Metrics**: Built-in metrics collection via `/metrics` endpoint
- **Error Handling**: Graceful error responses with detailed logging
- **Request Tracking**: Full request/response logging for debugging

___

## 🛠️ Technical Details

### Core Technologies
- **Backend**: FastAPI with async support
- **Frontend**: Streamlit with custom CSS styling
- **LLM**: Google Gemini 2.5 Flash
- **Embeddings**: HuggingFace Transformers
- **Vector DB**: ChromaDB
- **Agent Framework**: LangChain with tool calling

### Performance Features
- **Background Processing**: Web scraping runs asynchronously
- **Caching**: Streamlit caching for GIF processing
- **Connection Pooling**: Efficient HTTP request handling
- **Error Recovery**: Automatic retry mechanisms

### Security Considerations
- **CORS Configuration**: Properly configured for web deployment
- **Input Validation**: Pydantic models for request validation
- **File Type Restrictions**: Only PDF files accepted for upload
- **URL Validation**: Proper URL format checking

___

## 🆘 Troubleshooting

### Common Issues

**"GEMINI_API_KEY is not set" Error:**
- Ensure your API key is properly exported as an environment variable
- Verify the key has the correct permissions

**PDF Upload Fails:**
- Check that the file is a valid PDF
- Ensure the `upload/` directory is writable
- Verify the FastAPI server is running on port 8000

**Web Scraping Errors:**
- Confirm the URL is accessible and properly formatted
- Some websites may block automated scraping
- Check network connectivity

**Empty Search Results:**
- Ensure content has been properly uploaded/scraped first
- Try different search terms or query phrasings
- Check the logs for processing errors

### Performance Tips

- For large PDFs, processing may take several minutes
- Web scraping speed depends on the target site's response time
- Use specific queries for better search results
- Monitor memory usage with large document collections

___

## 🤝 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

___

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.