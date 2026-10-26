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

# Execute example query

```bash
curl -X POST http://127.0.0.1:8000/graphql \
-H "Content-Type: application/json" \
-d '{
  "query": "query { movies(where: {year: 2008, director: \"Christopher Nolan\"}) { title } }"
}'
```

# Open GraphQL playground

Open in browser http://127.0.0.1:8000/graphql
