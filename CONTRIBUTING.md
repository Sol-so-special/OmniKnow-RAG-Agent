# Contributing to **OmniKnow RAG Agent**

Thank you for your interest in contributing to **OmniKnow**! This document provides guidelines and instructions for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [Development Workflow](#-development-workflow)
- [Coding Standards](#-coding-standards)
- [Testing Guidelines](#-testing-guidelines)
- [Commit Message Guidelines](#-commit-message-guidelines)
- [Pull Request Process](#-pull-request-process)
- [Project Structure](#-project-structure)
- [Reporting Issues](#-reporting-issues)

---

## 🤝 Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- **Be respectful** and inclusive of all contributors
- **Be constructive** in feedback and discussions
- **Be professional** in all interactions
- **Focus on what is best** for the community and project

Violations may result in being banned from contributing.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- **Git**
- **Code editor** (VS Code recommended)

### Fork and Clone

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/Sol-so-special/OmniKnow-RAG-Agent
cd OmniKnow-RAG-Agent

# 3. Add upstream remote
git remote add upstream https://github.com/Sol-so-special/OmniKnow-RAG-Agent
```

### Setup Development Environment

```bash
# 1. Create .env file
cp .env.example .env
# Add your API keys

# 2. Start development environment
docker-compose up --build

# 3. Verify everything works
python tests/test_api.py
```

---

## 🔄 Development Workflow

### 1. Create Feature Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

Branch naming conventions:

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

### 2. Make Changes

- Write clean, documented code
- Follow existing code structure and patterns
- Add tests for new features
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run local tests
python tests/test_api.py

# Test with Docker Compose
docker-compose up --build
# Verify at http://localhost:8000/docs

# Test Kubernetes manifests (optional but recommended for K8s changes)
# AWS EKS
kubectl apply -f kubernetes/ --dry-run=client
kubectl apply -f kubernetes/ --dry-run=server

# GCP GKE
kubectl apply -f kubernetes-gcp/ --dry-run=client
kubectl apply -f kubernetes-gcp/ --dry-run=server

# Run linting
cd backend
pip install flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
# Then create Pull Request on GitHub
```

---

## 📝 Coding Standards

### Python Code Style

- **PEP 8**: Follow [PEP 8](https://pep8.org/) style guide
- **Type Hints**: Use type hints for function parameters and returns
- **Docstrings**: Use Google-style docstrings

```python
def process_document(file_path: Path, force_reprocess: bool = False) -> int:
    """
    Process and index a document.
    
    Args:
        file_path: Path to the document file
        force_reprocess: Whether to reprocess if already exists
        
    Returns:
        Number of chunks stored
        
    Raises:
        ValueError: If document already processed and force_reprocess=False
    """
    # Implementation
```

### Code Organization

- **Single Responsibility**: Each function/class should have one clear purpose
- **DRY Principle**: Don’t repeat yourself - extract common logic
- **Separation of Concerns**: Keep API logic, business logic, and infrastructure separate

### Naming Conventions

- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private Methods**: `_leading_underscore`

---

## 🧪 Testing Guidelines

### Test Requirements

All new features MUST include tests:

```python
# Example test structure
def test_pdf_upload():
    """Test PDF upload functionality."""
    with open("test.pdf", "rb") as f:
        response = requests.post(
            f"{API_BASE}/pdf/upload",
            files={"file": f}
        )
    assert response.status_code == 200
    assert "chunks_stored" in response.json()
```

### Test Categories

1. **Unit Tests**: Test individual functions/methods
2. **Integration Tests**: Test API endpoints
3. **E2E Tests**: Test complete workflows

### Running Tests

```bash
# Run all tests
python tests/test_api.py
```

---

## 💬 Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(agent): add conversation memory persistence

- Implement Redis-based conversation storage
- Add session management
- Update agent executor to use memory

Closes #123
```

```bash
fix(pdf): handle PDFs without page metadata

Added default value for page number extraction to prevent crashes
when processing PDFs without page metadata.
```

---

## 🔀 Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] Branch is up-to-date with `main`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
```

### Review Process

1. **Automated Checks**: GitHub Actions runs tests
2. **Code Review**: Maintainer reviews code
3. **Feedback**: Address requested changes
4. **Approval**: Maintainer approves PR
5. **Merge**: PR is merged to `main`

---

## 🗂️ Project Structure

Understanding the project structure helps you contribute effectively:

```
Omniknow-RAG-Agent/
├── .env                          # Local environment variables
├── .env.cloud                    # AWS cloud environment template
├── .env.gcp                      # GCP cloud environment template
├── .gitignore
├── LICENSE
├── README.md                     # Project Documentation
├── CONTRIBUTING.md               # Contributing guidelines
├── docker-compose.yml            # Local development stack
├── docker-compose.cloud.yml      # Cloud simulation (API-only)
│
├── .github/
│   └── workflows/
│       ├── deploy-aws.yml        # AWS EKS CI/CD pipeline
│       ├── deploy-gcp.yml        # GCP Cloud Run CI/CD pipeline
│       ├── deploy-gke.yml        # GCP GKE CI/CD pipeline
│       └── test.yml              # Automated testing
│
├── backend/                      # FastAPI backend application
│   ├── __init__.py
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   │
│   ├── api/                      # REST API layer
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── dependencies.py       # Dependency injection
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py         # Health check endpoint
│   │       ├── pdf.py            # PDF upload/search endpoints
│   │       ├── web.py            # Web scraping endpoints
│   │       └── agent.py          # Agent chat endpoint
│   │
│   ├── agent/                    # LangChain agent logic
│   │   ├── __init__.py
│   │   ├── executor.py           # Agent executor setup
│   │   └── prompt.py             # System prompts
│   │
│   ├── core/                     # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py             # Pydantic settings
│   │   └── logging.py            # Logging configuration
│   │
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   └── schemas.py            # Pydantic request/response schemas
│   │
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── embeddings.py         # Embedding model singleton
│   │   ├── vector_store.py       # Vector DB abstraction (Chroma/Pinecone)
│   │   ├── storage.py            # File storage abstraction (local/S3)
│   │   ├── pdf_service.py        # PDF processing
│   │   └── web_service.py        # Web scraping
│   │
│   └── tools/                    # LangChain tools
│       ├── __init__.py
│       ├── pdf_tool.py           # PDF search tool
│       ├── web_tool.py           # Web search tool
│       └── google_tool.py        # Google search tool
│
├── local_frontend/               # Streamlit UI (local-only)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── streamlit_app.py          # Main Streamlit app
│   └── assets/
│       ├── background.gif
│       └── styling.py            # Custom CSS/styling
│
├── kubernetes/                   # AWS EKS manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml.example      # Template
│   ├── hpa.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   └── ingress.yaml              # NGINX ingress with TLS
│
├── kubernetes-gcp/               # GCP GKE manifests
│   ├── configmap.yaml
│   ├── secrets.yaml.example
│   ├── hpa.yaml
│   ├── backend-deployment.yaml
│   └── backend-service.yaml
│
├── scripts/                      # Utility scripts
│   ├── generate_test_pdf.py      # Creates test PDF (test_document.pdf) for API integration tests (tests/test_api.py)
│   └── deploy-gcp.sh             # GCP deployment helper
│
├── tests/                        # Test suite
│   ├── test_api.py               # API integration tests
│   └── fixtures/                 # Test data for sample files
│       └── test_document.pdf     # Sample PDF for testing
│
├── docs/                         # Documentation
│   ├── deployment-guide.md       # Documentation for deployment with detailed steps
│   └── architecture.png          # System architecture diagram
│
└── demo/                         # Demo materials
    ├── screenshots/
    │   ├── streamlit_ui.png
    │   └── kubernetes_dashboard.png
    └── videos/
        └── local_demo_video.mp4
```

### Key Files

- **`backend/api/main.py`**: FastAPI application entry point
- **`backend/core/config.py`**: Configuration management
- **`backend/services/vector_store.py`**: Vector store abstraction
- **`backend/agent/executor.py`**: LangChain agent setup

---

## 🐛 Reporting Issues

### Before Creating an Issue

- Search existing issues to avoid duplicates
- Verify the issue exists in the latest version
- Collect relevant information (logs, screenshots, etc.)

### Issue Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11.5]
- Docker: [e.g., 24.0.6]

## Logs
```

Paste relevant logs here

```

```

### Feature Requests

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should this work?

## Alternatives Considered
Other approaches you've thought about
```

---

## 🎯 Areas for Contribution

Looking for where to contribute? Consider these areas:

### High Priority

- [ ] Improve test coverage
- [ ] Add support for more document formats (DOCX, TXT)
- [ ] Implement user authentication
- [ ] Add conversation memory persistence

### Medium Priority

- [ ] Improve error handling and logging
- [ ] Add more LangChain tools
- [ ] Implement rate limiting
- [ ] Add Helm charts for Kubernetes deployments
- [ ] Add caching layer (Redis)

### Documentation

- [ ] Add more code examples
- [ ] Create video tutorials
- [ ] Improve API documentation
- [ ] Add architecture decision records (ADRs)

---

## 📚 Resources

### Helpful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

### Learning Resources

- [RAG Tutorial](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)
- [MLOps Principles](https://ml-ops.org/)

---

## ❓ Questions?

If you have questions about contributing:

1. Check existing documentation
2. Search closed issues
3. Ask in GitHub Discussions
4. Email: solsosospecial@gmail.com

---

## 🌟 Recognition

Contributors will be recognized in:

- Project [README](README.md)
- This section
- GitHub contributors list

Thank you for contributing to OmniKnow! 🎉

---

**Happy Contributing!** 🚀​​​​​​​​​​​​​​​​