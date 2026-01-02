from pycursor_agent import Client
import os
import shutil

def test_sdk():
    # Set the folder where test results will be stored
    sdk_root = os.path.dirname(os.path.abspath(__file__))
    test_results_dir = os.path.join(sdk_root, "test_results")
    
    # Clean and create the test results directory
    if os.path.exists(test_results_dir):
        shutil.rmtree(test_results_dir)
    os.makedirs(test_results_dir)
    
    print(f"Testing SDK. Results will be saved in: {test_results_dir}")
    
    # Set workspace to test_results so generated files stay within that folder
    client = Client(workspace=test_results_dir)
    model = "gemini-3-flash"
    
    # Log file path
    log_path = os.path.join(test_results_dir, "test_log.txt")
    
    def log(msg):
        print(msg)
        with open(log_path, "a") as f:
            f.write(msg + "\n")

    log("=== Cursor Agent SDK Test Report ===\n")

    # 1. Testing 'ask' mode
    log("--- 1. Testing 'ask' mode ---")
    try:
        res = client.ask("What is 1 + 1?", model=model)
        log(f"Prompt: What is 1 + 1?\nResult: {res}\n")
    except Exception as e:
        log(f"Error in 'ask': {e}\n")

    # 2. Testing 'agent' mode
    log("--- 2. Testing 'agent' mode ---")
    try:
        # Ask it to write the result to a file
        res = client.call("Write the result of '1 + 1' into a file named agent_result.txt", model=model)
        log(f"Prompt: Write result of '1 + 1' to file\nResult: {res}\n")
    except Exception as e:
        log(f"Error in 'agent': {e}\n")

    # 3. Testing 'planner' mode
    log("--- 3. Testing 'planner' mode ---")
    try:
        res = client.plan("I want to write a simple calculator program, please help me plan the steps", model=model)
        log(f"Prompt: Plan a calculator program\nResult: {res}\n")
    except Exception as e:
        log(f"Error in 'planner': {e}\n")

    # 4. Testing 'debug' mode
    log("--- 4. Testing 'debug' mode ---")
    try:
        # Create a buggy file in the test_results directory for debugging
        buggy_file = os.path.join(test_results_dir, "buggy_code.py")
        with open(buggy_file, "w") as f:
            f.write("def add(a, b):\n    return a - b  # Intentional bug")
        
        res = client.debug("The logic of the add function in buggy_code.py seems wrong, please check and fix it", model=model)
        log(f"Prompt: Fix buggy_code.py\nResult: {res}\n")
    except Exception as e:
        log(f"Error in 'debug': {e}\n")

    log("=== Test Complete ===")

if __name__ == "__main__":
    test_sdk()
