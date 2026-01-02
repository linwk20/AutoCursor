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
It is important to note that the underlying `cursor-agent` CLI primarily operates in **Agent Mode**. The four modes provided by this SDK (`ask`, `agent`, `planner`, `debug`) are achieved through **Prompt Engineering**. We wrap your prompts with specific instructions to guide the AI's behavior, ensuring it performs exactly as intended.

## 📦 Installation

### 1. Prerequisites
You **must** have the Cursor CLI installed and be logged in on your machine.
Visit [cursor.com/cli](https://cursor.com/en-US/cli) to install.

### 2. Create a Virtual Environment (Optional)
We highly recommend using a virtual environment to manage your dependencies:

1.  **Create environment**:
    ```bash
    python -m venv venv
    ```
2.  **Activate environment**:
    *   **Windows**: `.\venv\Scripts\activate`
    *   **macOS/Linux**: `source venv/bin/activate`

### 3. Install the SDK
```bash
pip install pycursor-agent
```

## 🛠 Usage

The SDK provides four primary methods to interact with the AI:

### Import the Package
```python
from pycursor_agent import Client
```

### 1. Agent Mode (`.agent`)
The default autonomous mode. AI can read/write files and execute terminal commands.
```python
client = Client()
client.agent("Write the result of '1 + 1' into result.txt", model="gemini-3-flash")
```

### 2. Ask Mode (`.ask`)
Pure Q&A mode. The AI is instructed to answer questions without making any changes to your files.
```python
answer = client.ask("What is 1 + 1?")
```

### 3. Planner Mode (`.plan`)
Asks the AI to create a detailed execution plan for a complex task without actually performing the actions.
```python
plan = client.plan("Plan the development steps for a weather forecast app")
```

### 4. Debug Mode (`.debug`)
Focused on bug hunting. AI will analyze the code and attempt to fix the issues.
```python
fix = client.debug("Fix the connection timeout bug in main.py")
```

## 🧪 Testing
The project includes a `test_sdk.py` script that demonstrates and verifies all four modes. You can run it to see the SDK in action:
```bash
python3 test_sdk.py
```
Test results (including generated files) will be stored in the `test_results/` folder.

## 🏗 API Reference

### `Client`
- `agent(prompt, model, mode, force, print_output)`: The primary method to interact with the agent.
- `ask(prompt, model)`: Shortcut for non-modifying Q&A.
- `debug(prompt, model)`: Shortcut for debugging tasks.
- `plan(prompt, model)`: Shortcut for planning tasks.

## 📄 License
MIT License
