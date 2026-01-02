import subprocess
import shutil
import os
from typing import Optional, List

class CursorAgentClient:
    """
    A Python wrapper for the Cursor Agent CLI.
    
    This client allows you to programmatically interact with Cursor's AI Agent
    to perform coding tasks, ask questions, or debug code.
    """

    def __init__(self, agent_path: str = "cursor-agent", workspace: Optional[str] = None):
        """
        Initialize the Cursor Agent client.
        
        :param agent_path: Path to the cursor-agent executable. Defaults to 'cursor-agent'.
        :param workspace: The workspace directory to use. Defaults to current directory.
        """
        self.agent_path = shutil.which(agent_path) or agent_path
        self.workspace = workspace or os.getcwd()

    def agent(self, 
             prompt: str, 
             model: Optional[str] = None, 
             mode: str = "agent", 
             force: bool = True,
             print_output: bool = True) -> str:
        """
        Run the Cursor Agent with a prompt.
        
        :param prompt: The task or question for the agent.
        :param model: The AI model to use (e.g., 'gemini-3-flash', 'gpt-5.2').
        :param mode: The operation mode ('ask', 'agent', 'planner', 'debug').
        :param force: If True, automatically approve file changes and commands.
        :param print_output: If True, the agent's response is printed to stdout.
        :return: The string response from the agent.
        """
        
        # Prepare the base command
        # Although 'ask', 'planner', 'debug' are not direct subcommands of cursor-agent CLI,
        # we can influence behavior via the prompt or future-proof the API.
        # Currently, we use the 'agent' command as the primary interface.
        
        cmd = [self.agent_path]
        
        if print_output:
            cmd.append("--print")
            
        if force:
            cmd.append("--force")
            
        if model:
            cmd.extend(["--model", model])
            
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
        
        # Use the 'agent' subcommand as it's the most versatile
        cmd.extend(["agent", final_prompt])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout
            raise RuntimeError(f"Cursor Agent execution failed: {error_msg}")

    def ask(self, prompt: str, model: Optional[str] = None) -> str:
        """Helper for 'ask' mode."""
        return self.agent(prompt, model=model, mode="ask", force=False)

    def debug(self, prompt: str, model: Optional[str] = None) -> str:
        """Helper for 'debug' mode."""
        return self.agent(prompt, model=model, mode="debug")

    def plan(self, prompt: str, model: Optional[str] = None) -> str:
        """Helper for 'planner' mode."""
        return self.agent(prompt, model=model, mode="planner")

