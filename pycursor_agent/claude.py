"""
Claude Code Client - Implementation for Anthropic's Claude Code CLI.

This module provides a Python wrapper for the Claude Code command-line tool,
with an API consistent with CursorAgentClient.

Internal mappings from Cursor-style args to Claude CLI args:
- --force → --dangerously-skip-permissions
- --approve-mcps → --tools "default" (or "" to disable)
- --print → --print
- --model → --model (with alias conversion)
- chat_id → --resume <id>
- --workspace → cwd (working directory)
"""

import subprocess
import json
import os
from typing import Optional

from .base import BaseAgentClient


class ClaudeCodeClient(BaseAgentClient):
    """
    A Python wrapper for the Claude Code CLI.
    
    This client provides an API consistent with CursorAgentClient,
    internally converting parameters to Claude CLI format.
    
    Example:
        >>> from pycursor_agent import ClaudeCodeClient
        >>> client = ClaudeCodeClient()
        >>> response = client.agent("Create a hello world script")
    """

    # Model alias mapping: Cursor-style → Claude-style
    MODEL_ALIASES = {
        # Common aliases
        "sonnet": "sonnet",
        "opus": "opus",
        "claude-sonnet": "sonnet",
        "claude-opus": "opus",
        # Map some cursor model names if needed
        "claude-3-sonnet": "sonnet",
        "claude-3-opus": "opus",
    }

    def __init__(
        self, 
        agent_path: str = "claude", 
        workspace: Optional[str] = None, 
        approve_mcps: bool = True
    ):
        """
        Initialize the Claude Code client.
        
        :param agent_path: Path to the claude executable. Defaults to 'claude'.
        :param workspace: The workspace directory to use. Defaults to current directory.
        :param approve_mcps: Automatically approve all MCP servers. Defaults to True.
        """
        super().__init__(
            executable=agent_path,
            workspace=workspace,
            auto_approve=approve_mcps
        )
        # Keep approve_mcps as an alias for API consistency with Cursor
        self.approve_mcps = approve_mcps

    @property
    def agent_path(self) -> str:
        """Alias for executable for API consistency with Cursor."""
        return self.executable

    def _convert_model(self, model: str) -> str:
        """Convert Cursor-style model names to Claude CLI format."""
        if not model:
            return model
        return self.MODEL_ALIASES.get(model.lower(), model)

    def agent(
        self, 
        prompt: str, 
        model: Optional[str] = None, 
        mode: str = "agent", 
        force: bool = True,
        approve_mcps: Optional[bool] = None,
        chat_id: Optional[str] = None,
        print_output: bool = True
    ) -> str:
        """
        Run Claude Code with a prompt.
        
        API is consistent with CursorAgentClient.agent().
        
        :param prompt: The task or question for the agent.
        :param model: The AI model to use ('sonnet', 'opus', or full model name).
        :param mode: The operation mode ('ask', 'agent', 'planner', 'debug').
        :param force: If True, bypass permission checks (--dangerously-skip-permissions).
        :param approve_mcps: If True, enable all tools (--tools "default"); if False, disable all (--tools "").
        :param chat_id: Optional chat ID to resume a previous conversation.
        :param print_output: If True, use print mode (non-interactive).
        :return: The string response from Claude.
        """
        cmd = [self.executable]
        
        # --print for non-interactive mode (required for programmatic use)
        if print_output:
            cmd.append("--print")
        
        # --force in Cursor → --dangerously-skip-permissions in Claude
        if force:
            cmd.append("--dangerously-skip-permissions")
        
        # --tools controls available tools (only works with --print mode)
        # approve_mcps=True means use all tools ("default")
        should_approve_mcps = approve_mcps if approve_mcps is not None else self.approve_mcps
        if should_approve_mcps:
            cmd.extend(["--tools", "default"])
        else:
            cmd.extend(["--tools", ""])
        
        # Model selection (with alias conversion)
        if model:
            converted_model = self._convert_model(model)
            cmd.extend(["--model", converted_model])
        
        # Resume existing session if chat_id is provided
        if chat_id:
            cmd.extend(["--resume", chat_id])

        # Handle modes by modifying the prompt (same as Cursor)
        final_prompt = prompt
        if mode == "ask":
            final_prompt = f"[MODE: ASK - Please answer the question without modifying any files] {prompt}"
        elif mode == "debug":
            final_prompt = f"[MODE: DEBUG - Focus on finding and fixing bugs in the code] {prompt}"
        elif mode == "planner":
            final_prompt = f"[MODE: PLANNER - Create a detailed plan for the following task but do not execute yet] {prompt}"
        
        # Add -- to separate options from prompt
        cmd.append("--")
        # Add prompt at the end (Claude CLI takes prompt as positional arg)
        cmd.append(final_prompt)
        
        try:
            # Run from workspace directory if specified
            env = os.environ.copy()
            cwd = self.workspace if self.workspace else None

            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd,
                env=env
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout
            raise RuntimeError(f"Claude Code execution failed: {error_msg}")

    def create_chat(self) -> str:
        """
        Create a new chat session and return its ID.
        
        This runs a minimal Claude command to create a real session,
        then extracts and returns the session_id from the JSON output.
        
        :return: The session ID (UUID).
        """
        cmd = [
            self.executable,
            "--print",
            "--output-format", "json",
            "--dangerously-skip-permissions",
            "--",
            "Say OK"  # Minimal prompt to create session
        ]
        
        try:
            cwd = self.workspace if self.workspace else None
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
            
            # Parse JSON output to extract session_id
            output = json.loads(result.stdout.strip())
            session_id = output.get("session_id")
            
            if not session_id:
                raise RuntimeError("No session_id found in Claude output")
            
            return session_id
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout
            raise RuntimeError(f"Failed to create chat: {error_msg}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse Claude output: {e}")
