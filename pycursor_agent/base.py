"""
Base Agent Client - Abstract base class for all agent clients.

This module provides a consistent interface across different coding agents
like Cursor Agent, Claude Code, Codex, Gemini CLI, etc.
"""

import subprocess
import shutil
import os
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class AgentResponse:
    """Standardized response from any agent."""
    content: str
    raw_output: str
    chat_id: Optional[str] = None
    model: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseAgentClient(ABC):
    """
    Abstract base class for AI coding agent clients.
    
    This provides a unified interface for interacting with various AI coding
    assistants (Cursor Agent, Claude Code, Codex, Gemini CLI, etc.)
    """

    def __init__(
        self, 
        executable: str,
        workspace: Optional[str] = None,
        auto_approve: bool = True
    ):
        """
        Initialize the agent client.
        
        :param executable: Name or path to the agent executable.
        :param workspace: The workspace directory to use. Defaults to current directory.
        :param auto_approve: Automatically approve actions/permissions. Defaults to True.
        """
        self.executable = shutil.which(executable) or executable
        self.workspace = workspace or os.getcwd()
        self.auto_approve = auto_approve

    def _check_executable(self) -> bool:
        """Check if the executable is available."""
        return shutil.which(self.executable) is not None

    @abstractmethod
    def agent(
        self, 
        prompt: str, 
        model: Optional[str] = None, 
        mode: str = "agent",
        force: bool = True,
        chat_id: Optional[str] = None,
        print_output: bool = True
    ) -> str:
        """
        Run the agent with a prompt.
        
        :param prompt: The task or question for the agent.
        :param model: The AI model to use.
        :param mode: The operation mode ('ask', 'agent', 'planner', 'debug').
        :param force: If True, automatically approve file changes and commands.
        :param chat_id: Optional chat ID to resume a previous conversation.
        :param print_output: If True, the agent's response is printed to stdout.
        :return: The string response from the agent.
        """
        pass

    @abstractmethod
    def create_chat(self) -> str:
        """
        Create a new chat and return its ID.
        
        :return: Chat ID string.
        """
        pass

    def ask(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Ask a question without modifying files.
        
        :param prompt: The question to ask.
        :param model: Optional model to use.
        :return: The agent's response.
        """
        return self.agent(prompt, model=model, mode="ask", force=False)

    def debug(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Debug mode - focus on finding and fixing bugs.
        
        :param prompt: Description of the bug or issue.
        :param model: Optional model to use.
        :return: The agent's response.
        """
        return self.agent(prompt, model=model, mode="debug")

    def plan(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Planning mode - create a detailed plan without executing.
        
        :param prompt: The task to plan.
        :param model: Optional model to use.
        :return: The agent's response with the plan.
        """
        return self.agent(prompt, model=model, mode="planner")

    def run(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Alias for agent() with default settings.
        
        :param prompt: The task for the agent.
        :param model: Optional model to use.
        :return: The agent's response.
        """
        return self.agent(prompt, model=model)

    @property
    def is_available(self) -> bool:
        """Check if the agent executable is available on the system."""
        return self._check_executable()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(executable='{self.executable}', workspace='{self.workspace}')"

