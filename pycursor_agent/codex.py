"""
Codex Client - Implementation for Codex CLI.

This module provides a Python wrapper for the Codex command-line tool,
with an API consistent with CursorAgentClient and ClaudeCodeClient.
"""

import subprocess
import json
import os
from typing import Optional

from .base import BaseAgentClient


class CodexClient(BaseAgentClient):
    """
    A Python wrapper for the Codex CLI.
    
    This client provides an API consistent with CursorAgentClient,
    internally converting parameters to Codex CLI format.
    
    Example:
        >>> from pycursor_agent import CodexClient
        >>> client = CodexClient()
        >>> response = client.agent("Create a hello world script")
    """

    def __init__(
        self, 
        agent_path: str = "codex", 
        workspace: Optional[str] = None, 
        approve_mcps: bool = True
    ):
        """
        Initialize the Codex client.
        
        :param agent_path: Path to the codex executable. Defaults to 'codex'.
        :param workspace: The workspace directory to use. Defaults to current directory.
        :param approve_mcps: Automatically approve all MCP servers. Defaults to True.
        """
        super().__init__(
            executable=agent_path,
            workspace=workspace,
            auto_approve=approve_mcps
        )
        self.approve_mcps = approve_mcps
        print("[pycursor_agent][CodexClient] WARNING: CodexClient always enable Force mode if 'force' is True OR 'approve_mcps' is True.", flush=True)


    @property
    def agent_path(self) -> str:
        """Alias for executable for API consistency."""
        return self.executable

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
        Run Codex with a prompt.
        
        API is consistent with CursorAgentClient.agent().
        
        :param prompt: The task or question for the agent.
        :param model: The AI model to use.
        :param mode: The operation mode ('ask', 'agent', 'planner', 'debug').
        :param force: If True, bypass permission checks (--dangerously-bypass-approvals-and-sandbox).
        :param approve_mcps: Included for API consistency, ignored by Codex CLI directly (controlled by force/sandbox).
        :param chat_id: Optional chat ID to resume a previous conversation.
        :param print_output: If True, uses exec mode (non-interactive).
        :return: The string response from Codex.
        """
        cmd = [self.executable, "exec"]
        
        # Add global/exec flags FIRST (before subcommand/prompt)
        cmd.append("--json")
        
        # Force/Auto-approve
        # --dangerously-bypass-approvals-and-sandbox skips confirmations
        should_force = force or (approve_mcps if approve_mcps is not None else self.approve_mcps)
        if should_force:
            cmd.append("--dangerously-bypass-approvals-and-sandbox")
            
        # Model selection
        if model:
            cmd.extend(["--model", model])
        
        # Workspace
        if self.workspace:
            cmd.extend(["-C", self.workspace])

        # Handle modes by modifying the prompt
        final_prompt = prompt
        if mode == "ask":
            final_prompt = f"[MODE: ASK - Please answer the question without modifying any files] {prompt}"
        elif mode == "debug":
            final_prompt = f"[MODE: DEBUG - Focus on finding and fixing bugs in the code] {prompt}"
        elif mode == "planner":
            final_prompt = f"[MODE: PLANNER - Create a detailed plan for the following task but do not execute yet] {prompt}"
        
        # If chat_id is present, use 'resume' subcommand
        if chat_id:
            cmd.extend(["resume", chat_id, final_prompt])
        else:
            # No chat_id, just prompt
            cmd.append(final_prompt)
        
        try:
            # Run from workspace directory if specified (though -C handles it for Codex)
            cwd = self.workspace if self.workspace else None
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
            
            # Parse JSONL output to extract response text
            output_lines = result.stdout.strip().split('\n')
            response_text = []
            
            for line in output_lines:
                try:
                    data = json.loads(line)
                    if data.get("type") == "item.completed":
                        item = data.get("item", {})
                        # Collect agent messages
                        if item.get("type") == "agent_message":
                            text = item.get("text", "")
                            if text:
                                response_text.append(text)
                except json.JSONDecodeError:
                    continue
            
            return "\n".join(response_text).strip()

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout
            raise RuntimeError(f"Codex execution failed: {error_msg}")

    def create_chat(self) -> str:
        """
        Create a new chat session and return its ID.
        
        This runs a minimal Codex command to create a session,
        then extracts and returns the thread_id from the JSON output.
        
        :return: The session ID (thread_id).
        """
        cmd = [
            self.executable, "exec",
            "--json",
            "--dangerously-bypass-approvals-and-sandbox",
            "Say OK"
        ]
        
        if self.workspace:
            cmd.extend(["-C", self.workspace])
            
        try:
            cwd = self.workspace if self.workspace else None
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
            
            # Parse JSONL output to extract thread_id
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines:
                try:
                    data = json.loads(line)
                    if data.get("type") == "thread.started":
                        thread_id = data.get("thread_id")
                        if thread_id:
                            return thread_id
                except json.JSONDecodeError:
                    continue
            
            raise RuntimeError("Could not find thread_id in Codex output")
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout
            raise RuntimeError(f"Failed to create chat: {error_msg}")
