"""
Test script for CodexClient.

This script tests the Codex client to verify all modes and features work correctly.
Results will be saved in ./test_results_codex/
"""

from pycursor_agent import CodexClient
from test_cursor import run_common_tests
import os
import shutil


def test_sdk():
    # Set the folder where test results will be stored
    test_file_root = os.path.dirname(os.path.abspath(__file__))
    test_results_dir = os.path.join(test_file_root, "test_results_codex")
    
    # Clean and create the test results directory
    if os.path.exists(test_results_dir):
        # Auto-confirm for automation purposes, or use input if interactive
        # For this agent run, we'll just delete it to ensure clean state
        shutil.rmtree(test_results_dir)

    os.makedirs(test_results_dir)
    
    print(f"Testing Codex SDK. Results will be saved in: {test_results_dir}")
    
    # Initialize client with the test workspace
    client = CodexClient(workspace=test_results_dir)
    
    if not client.is_available:
        print("ERROR: codex CLI not found. Please install it first.")
        return
    
    # Run common tests
    # Using a model known to work with Codex, or default
    run_common_tests(
        client=client,
        test_results_dir=test_results_dir,
        name="Codex",
        model="gpt-5.1-codex-max"
    )


if __name__ == "__main__":
    test_sdk()

