"""
MCP Ask-to-Code Server

An autonomous MCP server that uses the Claude Code CLI to solve coding problems
without asking for permission. Hackable via CLI args and environment variables.
"""

import os
import sys
import subprocess
import argparse
import re
from mcp.server.fastmcp import FastMCP


# --- 1. HACKABLE CONFIGURATION (Via Arguments or Env Vars) ---
def get_config():
    """Parse configuration from CLI arguments and environment variables."""
    parser = argparse.ArgumentParser(description="Hackable Claude Code MCP Server")
    parser.add_argument(
        "--name",
        default=os.environ.get("MCP_NAME", "Autonomous Code Agent"),
        help="Name of the MCP Server",
    )
    parser.add_argument(
        "--tool-name",
        default=os.environ.get("MCP_TOOL_NAME", "ask_autonomous_agent"),
        help="Name of the function tool exposed to the LLM",
    )
    parser.add_argument(
        "--tool-description",
        default=os.environ.get(
            "MCP_TOOL_DESCRIPTION",
            "AUTONOMOUS AGENT: Solves a coding task or answers a question by running an internal agent.\n"
            "This tool has full access to the filesystem, can run tests, read files, and analyze logic.",
        ),
        help="Description of the function tool exposed to the LLM",
    )
    parser.add_argument(
        "--command",
        default=os.environ.get("CLAUDE_CMD", "claude"),
        help="The binary to run (e.g., 'claude' or 'npx @anthropic-ai/claude-code')",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("MCP_PORT", "0")),
        help="Port for SSE transport (0 = stdio mode, default)",
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("MCP_HOST", "0.0.0.0"),
        help="Host for SSE transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("CLAUDE_MODEL", ""),
        help="Claude model to use (e.g. claude-sonnet-4-20250514, opus)",
    )

    # Parse known args only, so fastmcp can handle the rest if needed
    args, _ = parser.parse_known_args()
    return args


config = get_config()

# Initialize Server with the custom name
mcp = FastMCP(config.name)


# --- 2. HELPERS ---
def strip_ansi(text: str) -> str:
    """Removes terminal colors so the output is clean for the LLM."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


# --- 3. THE DYNAMIC TOOL ---
# We register the tool dynamically to allow the name/description to be changed
@mcp.tool(name=config.tool_name, description=config.tool_description)
def execute_request(question: str) -> str:
    """
    Execute a request using the autonomous agent.
    """
    print(f"[{config.name}] Received Request: {question}")

    # The Magic Flags for Autonomy:
    # -p: Print output to stdout (Headless mode)
    # --dangerously-skip-permissions: BYPASSES ALL CONFIRMATION PROMPTS
    cmd = [config.command, "-p", question, "--dangerously-skip-permissions"]
    
    # Add model flag if specified
    if config.model:
        cmd.extend(["--model", config.model])

    try:
        # Run the command in the current folder where the server was started
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
            timeout=300,  # 5 minute timeout for complex tasks
        )

        # Combine stdout and stderr (sometimes the CLI prints info to stderr)
        full_output = result.stdout + "\n" + result.stderr
        clean_output = strip_ansi(full_output)

        if result.returncode != 0:
            return f"Agent encountered an error (Code {result.returncode}):\n{clean_output}"

        return f"Agent Analysis & Result:\n{clean_output}"

    except subprocess.TimeoutExpired:
        return "The agent timed out while trying to solve the problem."
    except FileNotFoundError:
        return f"Executable '{config.command}' not found. Is it installed?"
    except Exception as e:
        return f"System Error: {str(e)}"


def main():
    """Entry point for the MCP server."""
    # Remove our custom args from sys.argv so fastmcp doesn't get confused
    sys.argv = [sys.argv[0]] + [
        arg
        for arg in sys.argv[1:]
        if not arg.startswith(("--name", "--tool", "--command", "--port", "--host", "--model"))
    ]
    
    if config.port > 0:
        # SSE transport mode - use uvicorn directly for custom host/port
        import uvicorn
        print(f"[{config.name}] Starting SSE server on http://{config.host}:{config.port}")
        uvicorn.run(
            mcp.sse_app(),
            host=config.host,
            port=config.port,
            log_level="info"
        )
    else:
        # Default stdio transport mode
        mcp.run()


if __name__ == "__main__":
    main()

