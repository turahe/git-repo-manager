#!/usr/bin/env python3
"""
Test runner script for the GitLab/GitHub Repository Management Tool
"""

import sys
import subprocess
import os


def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print("Stdout:")
            print(e.stdout)
        if e.stderr:
            print("Stderr:")
            print(e.stderr)
        return False


def main():
    """Main test runner function"""
    print("🧪 GitLab/GitHub Repository Management Tool - Test Suite")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Install test dependencies
    print("\n📦 Installing test dependencies...")
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      "Installing requirements"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run linting
    print("\n🔍 Running linting...")
    lint_success = True
    
    # Check if flake8 is available
    try:
        subprocess.run(["flake8", "--version"], capture_output=True, check=True)
        if not run_command(["flake8", "src/", "cli.py"], "Flake8 linting"):
            lint_success = False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Flake8 not available, skipping linting")
    
    # Run type checking
    print("\n🔍 Running type checking...")
    type_success = True
    
    # Check if mypy is available
    try:
        subprocess.run(["mypy", "--version"], capture_output=True, check=True)
        if not run_command(["mypy", "src/", "cli.py"], "MyPy type checking"):
            type_success = False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  MyPy not available, skipping type checking")
    
    # Run unit tests
    print("\n🧪 Running unit tests...")
    test_success = run_command([
        sys.executable, "-m", "pytest", "tests/", 
        "-v", "--tb=short", "--cov=src", "--cov-report=term-missing"
    ], "Unit tests with coverage")
    
    # Run integration tests (if any)
    print("\n🔗 Running integration tests...")
    integration_success = run_command([
        sys.executable, "-m", "pytest", "tests/", 
        "-m", "integration", "-v"
    ], "Integration tests")
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    results = [
        ("Linting", lint_success),
        ("Type Checking", type_success),
        ("Unit Tests", test_success),
        ("Integration Tests", integration_success)
    ]
    
    all_passed = True
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{name:20} {status}")
        if not success:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 