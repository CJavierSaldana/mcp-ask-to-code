# MCP Ask-to-Code

An autonomous MCP server that uses the **Claude Code CLI** to solve coding problems without permission prompts.

## Quick Install (Global)

```bash
# Install from GitHub Packages (once published)
pip install mcp-ask-to-code --index-url https://ghcr.io/cjaviersaldana/mcp-ask-to-code/pypi/simple/

# Or install directly from GitHub
pip install git+https://github.com/cjaviersaldana/mcp-ask-to-code.git

# Or with pipx for isolated global install (recommended)
pipx install git+https://github.com/cjaviersaldana/mcp-ask-to-code.git
```

## Prerequisites

- **Python 3.10+**
- **Claude Code CLI** installed and authenticated:
  ```bash
  npm install -g @anthropic-ai/claude-code
  ```

## Usage

### Run the Server (stdio mode - for Claude Desktop)

```bash
mcp-ask-to-code
```

### Run on a Specific Port (SSE mode - for multiple sessions)

```bash
# Run on port 8080
mcp-ask-to-code --port 8080

# Run multiple instances on different ports
mcp-ask-to-code --port 8081 &
mcp-ask-to-code --port 8082 &
```

### Configuration Options

| Argument | Env Variable | Default | Description |
|----------|-------------|---------|-------------|
| `--name` | `MCP_NAME` | `Autonomous Code Agent` | Server name |
| `--tool-name` | `MCP_TOOL_NAME` | `ask_autonomous_agent` | Tool function name |
| `--command` | `CLAUDE_CMD` | `claude` | Claude CLI binary |
| `--port` | `MCP_PORT` | `0` (stdio) | SSE port (0=stdio) |
| `--host` | `MCP_HOST` | `127.0.0.1` | SSE host |

### Custom Personalities

```bash
# Backend Architect
MCP_NAME="Backend Architect" MCP_TOOL_NAME="consult_backend_expert" mcp-ask-to-code --port 8080

# Using npx instead of global install
mcp-ask-to-code --command "npx @anthropic-ai/claude-code"
```

## Claude Desktop Configuration

Add to `~/.config/claude-desktop/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ask-to-code": {
      "command": "mcp-ask-to-code",
      "args": [],
      "env": {}
    }
  }
}
```

**With custom environment:**

```json
{
  "mcpServers": {
    "ask-to-code": {
      "command": "mcp-ask-to-code",
      "args": [],
      "env": {
        "MCP_NAME": "Code Expert",
        "MCP_TOOL_NAME": "ask_code_expert"
      }
    }
  }
}
```

## Development

```bash
git clone https://github.com/cjaviersaldana/mcp-ask-to-code.git
cd mcp-ask-to-code
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## How It Works

1. **Single Tool**: Exposes `ask_autonomous_agent` to the LLM
2. **Delegation**: Passes the entire question to Claude Code CLI
3. **Autonomy**: Uses `--dangerously-skip-permissions` and `-p` flags
4. **Clean Output**: Strips ANSI codes for clean LLM responses

## License

MIT
