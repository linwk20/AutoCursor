"""
Cursor Agent Client - Implementation for Cursor's AI Agent CLI.

This module provides a Python wrapper for the Cursor Agent command-line tool,
allowing programmatic interaction with Cursor's AI capabilities.
"""

import subprocess
from typing import Optional

from .base import BaseAgentClient


class CursorAgentClient(BaseAgentClient):
    """
    A Python wrapper for the Cursor Agent CLI.
    
    This client allows you to programmatically interact with Cursor's AI Agent
    to perform coding tasks, ask questions, or debug code.
    
    Example:
        >>> from pycursor_agent import CursorAgentClient
        >>> client = CursorAgentClient()
        >>> response = client.agent("Create a hello world script")
    """

    def __init__(
        self, 
        agent_path: str = "cursor-agent", 
        workspace: Optional[str] = None, 
        approve_mcps: bool = True
    ):
        """
        Initialize the Cursor Agent client.
        
        :param agent_path: Path to the cursor-agent executable. Defaults to 'cursor-agent'.
        :param workspace: The workspace directory to use. Defaults to current directory.
        :param approve_mcps: Automatically approve all MCP servers. Defaults to True.
        """
        super().__init__(
            executable=agent_path,
            workspace=workspace,
            auto_approve=approve_mcps
        )
        # Keep approve_mcps as an alias for backwards compatibility
        self.approve_mcps = approve_mcps

    @property
    def agent_path(self) -> str:
        """Alias for executable for backwards compatibility."""
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
        Run the Cursor Agent with a prompt.
        
        :param prompt: The task or question for the agent.
        :param model: The AI model to use (e.g., 'gemini-3-flash', 'gpt-5.2').
        :param mode: The operation mode ('ask', 'agent', 'planner', 'debug').
        :param force: If True, automatically approve file changes and commands.
        :param approve_mcps: If True, automatically approve all MCP servers. Defaults to self.approve_mcps.
        :param chat_id: Optional chat ID to resume a previous conversation.
        :param print_output: If True, the agent's response is printed to stdout.
        :return: The string response from the agent.
        """
        cmd = [self.executable]
        
        if print_output:
            cmd.append("--print")
            
        if force:
            cmd.append("--force")

        should_approve_mcps = approve_mcps if approve_mcps is not None else self.approve_mcps
        if should_approve_mcps:
            cmd.append("--approve-mcps")
            
        if model:
            cmd.extend(["--model", model])
        
        if chat_id:
            cmd.extend(["--resume", chat_id])
            
        if self.workspace:
            cmd.extend(["--workspace", self.workspace])

        # Handle modes by modifying the prompt if necessary
        final_prompt = prompt
        if mode == "ask":
            final_prompt = f"[MODE: ASK - Please answer the question without modifying any files] {prompt}"
        elif mode == "debug":
            final_prompt = f"[MODE: DEBUG - Focus on finding and fixing bugs in the code] {prompt}"
        elif mode == "planner":
            final_prompt = f"[MODE: PLANNER - Create a detailed plan for the following task but do not execute yet] {prompt}"
        
        cmd.extend(["agent", final_prompt])
        
        try:
            result = self._run_command(cmd)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout
            raise RuntimeError(f"Cursor Agent execution failed: {error_msg}")

    def create_chat(self) -> str:
        """
        Create a new empty chat and return its ID.
        
        :return: The chat ID.
        """
        try:
            result = self._run_command([self.executable, "create-chat"])
            # Assuming output format like "Created chat: <chatId>" or just the ID
            return result.stdout.strip().split()[-1]
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create chat: {e.stderr}")

