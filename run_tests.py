#!/usr/bin/env python3
"""
Test runner script for the data provider system.

This script can be used to run all tests for the new abstract data layer.
"""

import sys
import subprocess
import os


def run_tests():
    """Run all tests for the data provider system."""
    
    # Change to the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    print("Running data provider system tests...")
    print("=" * 50)
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short"
        ], check=True)
        
        print("\n" + "=" * 50)
        print("All tests passed successfully! ✅")
        return 0
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print(f"Some tests failed! ❌ (exit code: {e.returncode})")
        return e.returncode
    
    except FileNotFoundError:
        print("Error: pytest not found. Please install it with:")
        print("pip install pytest")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())