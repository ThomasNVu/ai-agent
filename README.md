# AI Agent

A command-line coding agent that uses OpenRouter to inspect, edit, and run Python code inside the included `calculator/` workspace.

## Features

- List and read project files
- Create or overwrite files
- Run Python files and inspect their output
- Use multiple tool calls to complete a coding task
- Keep file operations inside `calculator/`

## Setup

Requires Python 3.13+, [`uv`](https://docs.astral.sh/uv/), and an [OpenRouter API key](https://openrouter.ai/keys).

```bash
git clone https://github.com/ThomasNVu/ai-agent.git
cd ai-agent
uv sync
```

Create a `.env` file:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Usage

```bash
uv run python main.py "Explain how the calculator works"
```

Use `--verbose` to show tool calls and token usage:

```bash
uv run python main.py "Add exponentiation support and run the tests" --verbose
```

## Tools

- `get_files_info` — list files and directories
- `get_file_content` — read a file
- `write_file` — create or overwrite a file
- `run_python_file` — execute a Python file

## Tests

```bash
uv run python calculator/tests.py
```

## Security

The agent can overwrite files and execute Python code. Its file paths are restricted to `calculator/`, but it is not a complete sandbox. Use it only in a trusted development environment.
