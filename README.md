# PyCursor-Agent

A powerful Python wrapper for the [Cursor Agent CLI](https://cursor.com/en-US/cli), allowing you to build general-purpose autonomous agents using Cursor's frontier models and context management capabilities.

## 🚀 Motivation

1.  **Reuse Cursor's Power**: Leverage Cursor Agent's state-of-the-art context management, tool-use capabilities, and deep codebase understanding programmatically.
2.  **Cost Effective**: Use Cursor's competitive API pricing for your own automated workflows and general agents.
3.  **General Agent Framework**: Build custom scripts, CI/CD integrations, or complex multi-step agents that interact with your filesystem and run commands autonomously.
4.  **Multi-Model Support**: Easily switch between top-tier models like `gemini-3-flash`, `gemini-3-pro`, `opus-4.5-thinking`, and `gpt-5.2`.

Check available models using:
```bash
cursor-agent --model list-models --print "hi"
```

## 🛠 Under the Hood: All is Agent
It is important to note that the underlying `cursor-agent` CLI primarily operates in **Agent Mode**. The four modes provided by this SDK (`agent`, `ask`, `planner`, `debug`) are achieved through **Prompt Engineering**.

### ⚠️ Warning: Force Mode
By default, this SDK uses Cursor's **Force Mode** (`--force`). In this mode, the Agent is automatically granted permission to execute all operations, including modifying files and running terminal commands. 
**This can be dangerous if the Agent performs unintended actions. Please use it with caution and avoid running it in sensitive environments without proper oversight.**

## 📦 Installation

### 1. Prerequisites
You **must** have the Cursor CLI installed and be logged in on your machine.
Visit [cursor.com/cli](https://cursor.com/en-US/cli) to install.

> Note: If you want to use a different supported agent (e.g. claude code), you need to install and authenticate their corresponding CLI as well. The automation mechanism relies on the agent’s official CLI being available on your system.

### 2. Create a Virtual Environment (Optional)
We highly recommend using a virtual environment:

1.  **Create environment**: `python -m venv venv`
2.  **Activate environment**:
    *   **Windows**: `.\venv\Scripts\activate`
    *   **macOS/Linux**: `source venv/bin/activate`

### 3. Install the SDK
```bash
pip install .
```

## 🛠 Usage

### Import the Package and Initialize Client
Specify a `workspace` directory to let the Agent "see" and "manage" your project files. 

Although primarily designed for Cursor, the SDK supports other agents (e.g. Claude Code) using a consistent interface.

```python
from pycursor_agent import CursorAgentClient, ClaudeCodeClient

# Initialize Cursor Agent client (Default)
client = CursorAgentClient(workspace="./my_project")

# Or initialize Claude Code client
# client = ClaudeCodeClient(workspace="./my_project")
```

### Context Management Strategies
You can manage conversation context in at least two ways:

1.  **File-based Context**: Leverage the Agent's ability to read and write files within the workspace. One Agent can write a plan or state to a file, and another (or the same one in a later call) can read it to continue the task.
2.  **Chat Session Resumption**: Use the native `chatId` (or session ID) to resume previous conversations.

```python
# Create a new chat session
chat_id = client.create_chat()

# Use the chat_id to maintain history
client.agent("My name is Alice", chat_id=chat_id)
response = client.agent("What is my name?", chat_id=chat_id)
print(response) # Should output something like "Your name is Alice"
```

### Primary Methods

1.  **Agent Mode (`.agent`)**: Default autonomous mode. Can read/write files and execute terminal commands.
2.  **Ask Mode (`.ask`)**: Pure Q&A. AI is instructed not to modify files.
3.  **Planner Mode (`.plan`)**: Generates an execution plan without performing actions.
4.  **Debug Mode (`.debug`)**: Focused on bug hunting and fixing.

## 🏗 API Reference

### `Client(agent_path="cursor-agent", workspace=None, approve_mcps=True)`
- `agent_path` (str): Path to the `cursor-agent` executable.
- `workspace` (str): The directory where the Agent will operate. Defaults to the current working directory.
- `approve_mcps` (bool): If `True`, automatically approves all configured MCP servers. **(Default: True)**

### `client.agent(prompt, model=None, mode="agent", force=True, approve_mcps=None, chat_id=None, print_output=True)`
- `prompt` (str): The instruction or question for the AI.
- `model` (str): The model name (e.g., `gemini-3-flash`, `sonnet`, `opus`).
- `mode` (str): Operation mode (`agent`, `ask`, `planner`, `debug`).
- `force` (bool): If `True`, automatically approves all file changes and terminal commands. **(Default: True)**
- `approve_mcps` (bool): Override the client's `approve_mcps` setting for this call.
- `chat_id` (str): Optional ID to resume a previous conversation history.
- `print_output` (bool): If `True`, the Agent's response will be printed to the console in real-time.

### `client.ask(prompt, model=None)`
- Shortcut for `agent()` with `mode="ask"`.

### `client.plan(prompt, model=None)`
- Shortcut for `agent()` with `mode="planner"`.

### `client.debug(prompt, model=None)`
- Shortcut for `agent()` with `mode="debug"`.

### `client.create_chat()`
- Creates a new empty chat session and returns its unique ID.

## 🧪 Testing

The project includes separate test cases for different agents under the `test_cases/` directory.

To test the **Cursor Agent**:
```bash
python3 test_cases/test_cursor.py
```

To test other agents, such as **Claude Code**:
```bash
python3 test_cases/test_claude.py
```

Test results and logs will be saved in `test_cases/test_results_cursor/` and `test_cases/test_results_claude/` respectively.

## 📦 Supporting More Agents

While this project is primarily focused on the Cursor Agent, its architecture is designed to support other CLI-based AI coding assistants effortlessly. We provide a unified interface that wraps different models to maintain consistency with Cursor's usage patterns.

As other agents may support specialized or broader features, you can extend this package to expose and leverage those specific capabilities.

| Agent | Client Class | CLI Command | Status |
|-------|--------------|-------------|--------|
| **Cursor Agent** | `CursorAgentClient` | `cursor-agent` | ✅ Supported |
| **Claude Code** | `ClaudeCodeClient` | `claude` | ✅ Supported |
| **Codex** | - | `codex` | 🚧 Coming Soon |
| **Gemini CLI** | - | `gemini` | 🚧 Coming Soon |

## 🚀 Upcoming Features

We are actively working on enhancing PyCursor-Agent with new features. Upcoming improvements include skill and user-defined prompts support, multi-agent orchestration, memory, and more.

## 📄 License
MIT License
