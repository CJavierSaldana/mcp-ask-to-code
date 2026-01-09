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

# Run on a port (SSE mode for multiple sessions)
mcp-ask-to-code --port 8080
```

### Options

| Argument | Env Variable | Default | Description |
|----------|-------------|---------|-------------|
| `--name` | `MCP_NAME` | `Autonomous Code Agent` | Server name |
| `--tool-name` | `MCP_TOOL_NAME` | `ask_autonomous_agent` | Tool name |
| `--command` | `CLAUDE_CMD` | `claude` | Claude CLI binary |
| `--model` | `CLAUDE_MODEL` | (default) | Model to use |
| `--port` | `MCP_PORT` | `0` (stdio) | SSE port |
| `--host` | `MCP_HOST` | `127.0.0.1` | SSE host |

## Claude Desktop Config

Add to `~/.config/claude-desktop/claude_desktop_config.json`:

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

## License

MIT
