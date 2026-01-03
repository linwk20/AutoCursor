"""
Gemini Client - Implementation for Google's Gemini CLI.

This module provides a Python wrapper for the Gemini command-line tool,
with an API consistent with CursorAgentClient and ClaudeCodeClient.

Internal mappings from Cursor-style args to Gemini CLI args:
- force / approve_mcps → --yolo
- model → --model
- chat_id → --resume
- workspace → cwd
"""

import subprocess
import json
import os
from typing import Optional

from .base import BaseAgentClient


class GeminiClient(BaseAgentClient):
    """
    A Python wrapper for the Gemini CLI.
    
    This client provides an API consistent with CursorAgentClient and ClaudeCodeClient,
    internally converting parameters to Gemini CLI format.
    
    Example:
        >>> from pycursor_agent import GeminiClient
        >>> client = GeminiClient()
        >>> response = client.agent("Create a hello world script")
    """

    # Model alias mapping: Cursor-style -> Gemini CLI style
    MODEL_ALIASES = {
        "gemini-3-flash": "flash",
        "gemini-3.0-flash": "flash",
        "gemini-3-pro": "pro",
        "gemini-3.0-pro": "pro",
        "gemini-2.0-flash": "flash",
        "gemini-2.0-pro": "pro",
        "gemini-1.5-flash": "flash",
        "gemini-1.5-pro": "pro",
    }

    def __init__(
        self, 
        agent_path: str = "gemini", 
        workspace: Optional[str] = None, 
        approve_mcps: bool = True
    ):
        """
        Initialize the Gemini client.
        
        :param agent_path: Path to the gemini executable. Defaults to 'gemini'.
        :param workspace: The workspace directory to use. Defaults to current directory.
        :param approve_mcps: Automatically approve all tools/MCP servers. Defaults to True.
        """
        super().__init__(
            executable=agent_path,
            workspace=workspace,
            auto_approve=approve_mcps
        )
        # Keep approve_mcps for API consistency
        self.approve_mcps = approve_mcps
        print("[pycursor_agent][GeminiClient] WARNING: GeminiClient always enable Force mode if 'force' is True OR 'approve_mcps' is True.", flush=True)

    @property
    def agent_path(self) -> str:
        """Alias for executable for API consistency."""
        return self.executable

    def _convert_model(self, model: str) -> str:
        """Convert Cursor-style model names to Gemini CLI format."""
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
        Run Gemini with a prompt.
        
        API is consistent with CursorAgentClient.agent().
        
        :param prompt: The task or question for the agent.
        :param model: The AI model to use (e.g., 'gemini-2.0-flash').
        :param mode: The operation mode ('ask', 'agent', 'planner', 'debug').
        :param force: If True, use YOLO mode (--yolo).
        :param approve_mcps: If True, use YOLO mode (--yolo).
        :param chat_id: Optional chat ID to resume a previous conversation.
        :param print_output: If True, non-interactive mode is used.
        :return: The string response from Gemini.
        """
        cmd = [self.executable]
        
        # force=True or approve_mcps=True → --yolo
        should_yolo = force or (approve_mcps if approve_mcps is not None else self.approve_mcps)
        # Note: Gemini CLI requires --yolo mode (force mode) to use tools or when force/tool-use is specified.
        # Always enable YOLO mode if 'force' is True or 'approve_mcps' is True.
        # INSERT_YOUR_CODE
        if should_yolo:
            cmd.append("--yolo")
        
        # Model selection (with alias conversion)
        if model:
            converted_model = self._convert_model(model)
            cmd.extend(["--model", converted_model])
        
        # Resume existing session if chat_id is provided
        if chat_id:
            cmd.extend(["--resume", chat_id])

        # Handle modes by modifying the prompt
        final_prompt = prompt
        if mode == "ask":
            final_prompt = f"[MODE: ASK - Please answer the question without modifying any files] {prompt}"
        elif mode == "debug":
            final_prompt = f"[MODE: DEBUG - Focus on finding and fixing bugs in the code] {prompt}"
        elif mode == "planner":
            final_prompt = f"[MODE: PLANNER - Create a detailed plan for the following task but do not execute yet] {prompt}"
        
        # Positional prompt for one-shot (non-interactive) mode
        cmd.append(final_prompt)
        
        try:
            cwd = self.workspace if self.workspace else None
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout
            if "SyntaxError: Invalid regular expression flags" in error_msg and "Node.js" in error_msg:
                raise RuntimeError(
                    f"Gemini CLI requires Node.js 20 or higher. Current version: {error_msg.split('Node.js ')[-1].strip()}\n"
                    "Please upgrade Node.js to use GeminiClient."
                ) from e
            raise RuntimeError(f"Gemini execution failed: {error_msg}")

    def create_chat(self) -> str:
        """
        Create a new chat session and return its ID.
        
        This runs a minimal Gemini command to create a session,
        then extracts and returns the session_id from the JSON output.
        
        :return: The session ID.
        """
        cmd = [
            self.executable,
            "--output-format", "json",
            "--yolo",
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
                raise RuntimeError("No session_id found in Gemini output")
            
            return session_id
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout
            if "SyntaxError: Invalid regular expression flags" in error_msg and "Node.js" in error_msg:
                raise RuntimeError(
                    f"Gemini CLI requires Node.js 20 or higher. Current version: {error_msg.split('Node.js ')[-1].strip()}\n"
                    "Please upgrade Node.js to use GeminiClient."
                ) from e
            raise RuntimeError(f"Failed to create chat: {error_msg}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse Gemini output: {e}")

