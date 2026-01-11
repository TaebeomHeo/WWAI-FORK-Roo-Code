import sys
import os
import json
import shutil

# Add the project root to sys.path to allow importing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import the MCP server tools
# Note: We are importing the functions directly to test the logic, bypassing the FastMCP server wrapper for this script.
# This assumes the functions are decorated but still callable, or we might need to inspect the 'mcp' object if FastMCP wraps them heavily.
# Looking at server.py, they are decorated with @mcp.tool(). FastMCP tools are usually callable directly.

try:
    from ww_custom.mcp.test_manager.server import check_tc_config, setup_tc_repo, save_new_tc, search_past_tcs, _load_config
except ImportError:
    # Try alternate import if package structure is different
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../mcp/test-manager')))
    try:
        from server import check_tc_config, setup_tc_repo, save_new_tc, search_past_tcs, _load_config
    except ImportError as e:
        print(f"Error importing MCP server: {e}")
        sys.exit(1)

def print_result(test_name, result):
    print(f"[{test_name}]")
    print(f"Result: {result}")
    print("-" * 30)

def main():
    print("=== Starting MCP Test Manager Verification ===\n")

    # 1. Backup existing config
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/qa_config.json'))
    backup_path = config_path + ".bak"
    if os.path.exists(config_path):
        shutil.copy(config_path, backup_path)
        print(f"Backed up config to {backup_path}")
    
    # Ensure starting with a clean slate for the test
    if os.path.exists(config_path):
        os.remove(config_path)

    try:
        # Test 1: Check Config (Should fail/missing)
        res = check_tc_config()
        print_result("Test 1: Check Initial Config", res)
        assert "MISSING_CONFIG" in res or "not configured" in res

        # Test 2: Setup Repo
        test_repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../temp_test_repo'))
        res = setup_tc_repo(test_repo_path)
        print_result("Test 2: Setup Repo", res)
        assert "SUCCESS" in res
        assert os.path.exists(test_repo_path)

        # Test 3: Check Config again (Should pass)
        res = check_tc_config()
        print_result("Test 3: Check Config After Setup", res)
        assert "OK" in res

        # Test 4: Save New TC
        tc_content = """# TC_LOGIN_001
## Title: Verify Login Success
## Steps:
1. Go to login page
2. Enter valid creds
3. Click login
## Expected:
Redirect to dashboard.
"""
        res = save_new_tc("TC_LOGIN_001.md", tc_content)
        print_result("Test 4: Save New TC", res)
        assert "SUCCESS" in res
        assert os.path.exists(os.path.join(test_repo_path, "TC_LOGIN_001.md"))

        # Test 5: Search Past TCs
        res = search_past_tcs("Login")
        print_result("Test 5: Search 'Login'", res)
        assert "TC_LOGIN_001.md" in res

    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"❌ ERROR DURING EXECUTION: {e}")
    finally:
        # Cleanup
        print("\n=== Cleanup ===")
        # Restore config
        if os.path.exists(backup_path):
            shutil.move(backup_path, config_path)
            print("Restored original config.")
        elif os.path.exists(config_path):
            os.remove(config_path) # If no backup existed, remove the one we created
            
        # Remove temp repo
        # if os.path.exists(test_repo_path):
        #     shutil.rmtree(test_repo_path)
        #     print("Removed temp test repo.")
        # Commented out repo removal to allow manual inspection if needed, 
        # or you can uncomment to clean up fully. For now, let's keep it for verification.
        print(f"Note: Temp test repo at {test_repo_path} was NOT removed for manual inspection.")

if __name__ == "__main__":
    main()
