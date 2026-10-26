# Setup

This lab uses [uv](https://docs.astral.sh/uv/) to manage the Python environment and dependencies.

Install uv if it is not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create the virtual environment and install dependencies:

```bash
uv sync
```

# Environment Variables
## Review 01_environment_variables.py
```bash
cat 01_environment_variables.py
```

## Run with provided environment variables
```bash
NICKNAME=Bobby uv run python 01_environment_variables.py
```

# Configuration file
## Review 02_config_file.py and 02_config_file.json
```bash
cat 02_config_file.py
cat 02_config_file.json
```

## Run 02_config_file.py
```bash
uv run python 02_config_file.py
```

# Simple Web App
## Run web app
```bash
uv run streamlit run 03_simple_web_app.py
```

# Simple Web App with DB
## Run web app
```bash
uv run streamlit run 04_simple_web_app_with_db.py
```

# Simple Pub/Sub app
## Run simple queue subscriber
```bash
uv run python 05_simple_queue_subscriber.py
```

## Run simple queue publisher
**Note:** Open another terminal first
```bash
uv run streamlit run 05_simple_queue_publisher.py
```

# Show threads on OS level
## Run
```bash
uv run python 06_threads.py
```

## Copy the command from the initial log message
Show threads on OS level: `ps -T -p XXXXXX`

## Execute the command in another terminal
```bash
ps -T -p XXXXXX
```

# Async
## Run
```bash
uv run python 07_async.py
```

## Compare threads with async
In another terminal, run the same `ps -T -p XXXXXX` command using the PID printed at startup and compare with the threads demo.
