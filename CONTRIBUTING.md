# Contributing to **OmniKnow RAG Agent**

Contributions to the OmniKnow RAG Agent are welcome! This document provides guidelines for contributing to the project.

___

## 🚀 Getting Started

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/Sol-so-special/OmniKnow-RAG-Agent
   cd rag_agent
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

___

## 📋 Development Guidelines

### Code Style

- **Python**: Follow PEP 8 style guidelines
- **Imports**: Use absolute imports, group standard library, third-party, and local imports
- **Documentation**: Include docstrings for all functions and classes
- **Type Hints**: Use type hints where appropriate

### Code Organization

- **API Endpoints**: Place new API routes in appropriate files within `api_endpoints/`
- **Data Processing**: Add new collectors to separate files following the pattern of existing collectors
- **UI Components**: Keep frontend components in the `frontend/` directory
- **Tools**: Add new LangChain tools to `tools.py`

### Testing

Before submitting changes:

1. **Test the FastAPI backend**:
   ```bash
   uvicorn api:app --host 127.0.0.1 --port 8000
   # Test endpoints using the docs at http://localhost:8000/docs
   ```

2. **Test the Streamlit frontend**:
   ```bash
   streamlit run app.py
   # Verify UI functionality and styling
   ```

3. **Test with sample data**:
   - Upload test PDFs
   - Add test URLs
   - Verify search functionality

___

## 🐛 Bug Reports

When reporting bugs, please include:

- **Environment details** (Python version, OS, dependencies)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** and logs
- **Screenshots** for UI issues

___

## ✨ Feature Requests

For new features:

- **Describe the use case** and why it's valuable
- **Provide implementation details** if you have ideas
- **Consider backward compatibility**
- **Discuss performance implications**

__

## 🔧 Types of Contributions

### High Priority Areas

1. **Performance Optimization**
   - Improve embedding generation speed
   - Optimize ChromaDB queries
   - Enhance memory usage

2. **Additional Data Sources**
   - Support for more file types (DOCX, TXT, etc.)
   - Integration with cloud storage (S3, Google Drive)
   - API-based data sources

3. **Enhanced UI/UX**
   - Mobile responsiveness improvements
   - Advanced search filters
   - Better error messaging

4. **Monitoring & Analytics**
   - Usage metrics dashboard
   - Query performance analytics
   - System health monitoring

### Code Contributions

1. **Fork and clone** the repository
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the guidelines above
4. **Test thoroughly** across different scenarios
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add support for DOCX file uploads"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** with:
   - Clear description of changes
   - Link to any related issues
   - Screenshots for UI changes
   - Testing instructions

### Documentation Contributions

- **API Documentation**: Update endpoint descriptions
- **User Guides**: Improve setup and usage instructions  
- **Code Comments**: Add/improve inline documentation
- **Examples**: Provide additional usage examples

___

## 🏗️ Architecture Guidelines

### Adding New Data Sources

1. **Create a collector** (e.g., `excel_data_collector.py`):
   ```python
   def load_excel_data(file_path):
       # Implementation
       pass
   
   def process_excel_data(data):
       # Implementation  
       pass
   ```

2. **Create an API wrapper** (e.g., `excel_wrapper.py`):
   ```python
   class ExcelSearchAPIWrapper(BaseModel):
       # Implementation
       pass
   ```

3. **Add API endpoints** in `api_endpoints/excel_api.py`:
   ```python
   @router.post("/add_excel/")
   async def upload_excel(file: UploadFile = File(...)):
       # Implementation
       pass
   ```

4. **Update the tool system** in `tools.py`:
   ```python
   def excel_tool():
       # Implementation
       pass
   ```

5. **Integrate with the agent** in `app.py`

### Database Schema Considerations

When adding new data types:
- Use consistent metadata structure
- Ensure unique collection names
- Plan for efficient querying patterns
- Consider data migration strategies

___

## 🧪 Testing Guidelines

### Unit Tests
- Test individual functions in isolation
- Mock external dependencies (APIs, file systems)
- Cover edge cases and error conditions

### Integration Tests  
- Test complete workflows (upload → process → search)
- Verify API endpoint functionality
- Test agent tool selection logic

### UI Tests
- Test file upload functionality
- Verify search result display
- Test responsive design across devices

___

## 📚 Resources

### Useful Links
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

### Development Tools
- **API Testing**: Use the FastAPI docs at `/docs` endpoint
- **Database Inspection**: ChromaDB provides built-in query tools
- **Logging**: Monitor `api.log` for debugging information

___

## 🤝 Community Guidelines

- **Be respectful** and inclusive in all interactions
- **Help others** by answering questions and reviewing PRs
- **Stay focused** on constructive technical discussions
- **Follow up** on your contributions and respond to feedback

___

## 📞 Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions and ideas
- **Documentation**: Check existing docs before asking questions

Thank you for contributing to **OmniKnow RAG Agent**! 🚀