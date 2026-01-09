# MCP Ask-to-Code

An autonomous MCP server that uses the **Claude Code CLI** to solve coding problems without permission prompts.

## Quick Install

```bash
# Global install with pipx (recommended)
pipx install git+https://github.com/cjaviersaldana/mcp-ask-to-code.git

# Or with pip
pip install git+https://github.com/cjaviersaldana/mcp-ask-to-code.git
```

## Prerequisites

**Claude Code CLI** installed and authenticated:
```bash
npm install -g @anthropic-ai/claude-code
```

## Usage

```bash
# Run (stdio mode for Claude Desktop)
mcp-ask-to-code

# Run with a specific model
mcp-ask-to-code --model claude-sonnet-4-20250514

# Run on a port (SSE mode for multiple sessions)
mcp-ask-to-code --port 8080
```

### Options

| Argument | Env Variable | Default | Description |
|----------|-------------|---------|-------------|
| `--model` | `CLAUDE_MODEL` | (CLI default) | Model to use (e.g. `claude-sonnet-4-20250514`, `opus`) |
| `--name` | `MCP_NAME` | `Autonomous Code Agent` | Server name |
| `--tool-name` | `MCP_TOOL_NAME` | `ask_autonomous_agent` | Tool function name |
| `--command` | `CLAUDE_CMD` | `claude` | Claude CLI binary path |
| `--port` | `MCP_PORT` | `0` (stdio) | Port for SSE mode |
| `--host` | `MCP_HOST` | `127.0.0.1` | Host for SSE mode |

## Claude Desktop Configuration

Add to your config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/claude-desktop/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Basic Setup

```json
{
  "mcpServers": {
    "ask-to-code": {
      "command": "mcp-ask-to-code",
      "args": []
    }
  }
}
```

### With Specific Model

```json
{
  "mcpServers": {
    "ask-to-code": {
      "command": "mcp-ask-to-code",
      "args": ["--model", "claude-sonnet-4-20250514"]
    }
  }
}
```

### Custom "Expert" Personality

```json
{
  "mcpServers": {
    "backend-expert": {
      "command": "mcp-ask-to-code",
      "args": ["--model", "opus", "--name", "Backend Architect"],
      "env": {
        "MCP_TOOL_NAME": "consult_backend_expert"
      }
    }
  }
}
```

### Multiple Agents

```json
{
  "mcpServers": {
    "code-agent": {
      "command": "mcp-ask-to-code",
      "args": ["--model", "claude-sonnet-4-20250514"]
    },
    "code-reviewer": {
      "command": "mcp-ask-to-code",
      "args": ["--model", "opus"],
      "env": {
        "MCP_NAME": "Code Reviewer",
        "MCP_TOOL_NAME": "review_code"
      }
    }
  }
}
```

## How It Works

1. Exposes a single tool (`ask_autonomous_agent`) to the LLM
2. Delegates questions to Claude Code CLI with `--dangerously-skip-permissions -p`
3. Returns clean output (ANSI codes stripped)

## License

MIT
