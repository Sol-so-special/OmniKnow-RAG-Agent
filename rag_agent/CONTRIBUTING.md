# Contributing to **OmniKnow** 🤝

First off — **thank you for considering contributing to OmniKnow!** 🎉
This project thrives on community input. Whether you’re fixing bugs, improving docs, or building new features, your contributions make a difference.

---

## 🛠️ How you can contribute

* **Report bugs**: Open a GitHub issue with clear reproduction steps.
* **Suggest enhancements**: Share ideas for improvements, whether UX, performance, or new features.
* **Improve documentation**: Even fixing a typo helps future users.
* **Add tests**: Strengthen reliability by expanding coverage.
* **Submit code**: Tackle open issues or propose new features.

---

## 🔄 Development workflow

1. **Fork** this repository.
2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/Solomon Ayo/rag_ai_agent
   cd chatbot
   ```
3. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Install dependencies** into a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   # .venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```
5. **Make your changes** (code, docs, tests).
6. **Run tests** before pushing (see Testing below).
7. **Commit** your changes with a clear message (see Commit Guidelines below).
8. **Push** to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```
9. **Open a Pull Request (PR)** against `main`.

---

## 🎨 Code style

* Follow **PEP8** (Python style guide).
* Keep functions small and focused.
* Write clear docstrings (Google or NumPy style).
* Use type hints where possible.
* Avoid duplicating code — refactor instead.

---

## 📝 Commit guidelines

* Use clear, descriptive commit messages.
* Format:

  ```
  <type>(<scope>): <short summary>
  ```

  Examples:

  * `fix(api): handle missing file extension in PDF upload`
  * `feat(frontend): add toggle for re-uploading PDFs`
  * `docs: expand README with API usage examples`

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

---

## ✅ Testing

* Ensure all changes pass existing tests.
* Add new tests for new functionality.
* Run tests locally before pushing (using `pytest` or your chosen framework).
* Check that both FastAPI endpoints and Streamlit UI still run without errors.

---

## 📂 Project structure recap

See [README.md](README.md#project-structure--important-files-) for a full breakdown. Key areas for contributors:

* `api_endpoints/` — add new routes or extend PDF/web APIs.
* `frontend/` — improve Streamlit UI & styling.
* `tools.py` — register new LangChain tools.
* `requirements.txt` — pin new dependencies responsibly.

---

## 💡 Tips for good contributions

* Small, focused PRs are easier to review than giant ones.
* Link your PR to related issues (`Closes #123`).
* Document new features in README if user-facing.
* Run `pip freeze > requirements.txt` if dependencies change.

---

## 📬 Questions?

* Open an [issue](../../issues).
* Or start a discussion in your PR.

We value your input, no matter the size.
Let’s build something powerful together 🚀