"""
Test script for ClaudeCodeClient.

This script tests the Claude Code client with the same API as CursorAgentClient.
Results will be saved in ./test_results_claude/
"""

from pycursor_agent import ClaudeCodeClient
import os
import shutil
from test_cursor import run_common_tests


def test_claude():
    # Set the folder where test results will be stored
    test_file_root = os.path.dirname(os.path.abspath(__file__))
    test_results_dir = os.path.join(test_file_root, "test_results_claude")
    
    # Clean and create the test results directory
    if os.path.exists(test_results_dir):
        if input(f"Delete test results directory {test_results_dir}? (y/n): ").lower() == "y":
            shutil.rmtree(test_results_dir)
        else:
            print("Please delete the directory manually before running the test.")
            return

    os.makedirs(test_results_dir)
    
    print(f"Testing Claude Code SDK. Results will be saved in: {test_results_dir}")
    
    client = ClaudeCodeClient(workspace=test_results_dir)
    
    if not client.is_available:
        print("ERROR: Claude CLI not found. Please install it first.")
        print("Run: npm install -g @anthropic-ai/claude-code")
        return
    
    run_common_tests(
        client=client,
        test_results_dir=test_results_dir,
        name="Claude Code"
    )


if __name__ == "__main__":
    test_claude()
