# Contributing to Context-Aware Research Brief Generator

We welcome contributions to the **Context-Aware Research Brief Generator** project! Whether it's fixing bugs, improving documentation, adding features, or enhancing testing, your help is appreciated.

## How to Contribute

### 1. Fork the Repository

* Click the **Fork** button at the top-right of the repository.
* Clone your fork locally:

```bash
git clone https://github.com/<your-username>/context-aware-research-brief.git
cd context-aware-research-brief
```

### 2. Set Up Development Environment

* Create a virtual environment:

```bash
python -m venv env
# Activate
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

* Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Create a Branch

* Use a descriptive branch name:

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes

* Follow **PEP8** standards for Python code.
* Ensure all **LLM outputs** continue to conform to Pydantic schemas.
* Add **unit tests** for any new functionality or bug fixes.
* Include docstrings and update documentation where necessary.

### 5. Testing

* Run unit tests:

```bash
pytest -v
```

* Ensure all tests pass before submitting a pull request.

### 6. Commit and Push

```bash
git add .
git commit -m "Add description of changes"
git push origin feature/your-feature-name
```

### 7. Open a Pull Request

* Navigate to your fork on GitHub.
* Click **Compare & Pull Request**.
* Fill in the description with details about your changes.
* Reference any related issues, if applicable.

### 8. Code Review

* One of the maintainers will review your pull request.
* Make requested changes promptly to ensure a smooth merge.

### 9. Merging

* Once approved, a maintainer will merge your PR into the main branch.

## Guidelines

* Be respectful and professional.
* Keep pull requests focused and concise.
* Ensure reproducibility; tests must pass on a fresh environment.
* Document new features and update README if necessary.

## Reporting Issues

* Use GitHub Issues to report bugs or request enhancements.
* Provide steps to reproduce, expected behavior, and observed behavior.
* Include relevant screenshots or error logs if applicable.

## License

All contributions must comply with the project’s [LICENSE](LICENSE).

---

Thank you for helping improve the **Context-Aware Research Brief Generator**!
