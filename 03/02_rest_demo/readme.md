# Setup

This demo uses [uv](https://docs.astral.sh/uv/) to manage the Python environment and dependencies.

Install uv if it is not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create the virtual environment and install dependencies:

```bash
uv sync
```

# Run application

```bash
uv run uvicorn main:app --reload
```

# Open OpenAPI Docs

Open in browser http://127.0.0.1:8000/docs
