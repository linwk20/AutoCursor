"""
Test script for GeminiClient.

This script tests the Gemini client with the same API as CursorAgentClient.
Results will be saved in ./test_results_gemini/
"""

from pycursor_agent import GeminiClient
import os
import shutil
from test_cursor import run_common_tests


def test_gemini():
    # Set the folder where test results will be stored
    test_file_root = os.path.dirname(os.path.abspath(__file__))
    test_results_dir = os.path.join(test_file_root, "test_results_gemini")
    
    # Clean and create the test results directory
    if os.path.exists(test_results_dir):
        if input(f"Delete test results directory {test_results_dir}? (y/n): ").lower() == "y":
            shutil.rmtree(test_results_dir)
        else:
            print("Please delete the directory manually before running the test.")
            return

    os.makedirs(test_results_dir)
    
    print(f"Testing Gemini SDK. Results will be saved in: {test_results_dir}")
    
    client = GeminiClient(workspace=test_results_dir)
    
    if not client.is_available:
        print("ERROR: Gemini CLI not found. Please install it first.")
        print("Run: npm install -g @google/gemini-cli")
        return
    
    run_common_tests(
        client=client,
        test_results_dir=test_results_dir,
        name="Gemini",
        model="gemini-3.0-flash"  # Using Cursor-style name, mapped to 'flash' internally
    )


if __name__ == "__main__":
    test_gemini()

