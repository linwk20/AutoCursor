"""
pycursor_agent - A unified Python SDK for AI coding assistants.

This package provides a consistent interface for interacting with various
AI coding agents including Cursor Agent, Claude Code, and more.

Quick Start:
    >>> from pycursor_agent import CursorAgentClient, ClaudeCodeClient
    >>> 
    >>> # Using Cursor Agent
    >>> cursor = CursorAgentClient()
    >>> cursor.agent("Create a hello world script")
    >>> 
    >>> # Using Claude Code
    >>> claude = ClaudeCodeClient()
    >>> claude.agent("Explain this code")
"""

# Base class
from .base import BaseAgentClient, AgentResponse

# Cursor Agent
from .cursor import CursorAgentClient

# Claude Code
from .claude import ClaudeCodeClient

# Gemini Client
from .gemini import GeminiClient

# Codex Client
from .codex import CodexClient


__all__ = [
    # Base
    "BaseAgentClient",
    "AgentResponse",
    # Implementations
    "CursorAgentClient",
    "ClaudeCodeClient",
    "GeminiClient",
    "CodexClient",
]

__version__ = "0.2.0"
