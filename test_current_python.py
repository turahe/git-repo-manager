#!/usr/bin/env python3
"""
Simple test script to verify codebase compatibility with the current Python version.
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")
    
    # List of modules to test
    modules_to_test = [
        'src.config',
        'src.gitlab_client',
        'src.github_client', 
        'src.repository_manager',
        'src.composer_manager',
        'src.services',
        'cli'
    ]
    
    failed_imports = []
    
    for module_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            failed_imports.append((module_name, e))
        except Exception as e:
            print(f"⚠️  {module_name}: {e}")
            failed_imports.append((module_name, e))
    
    return failed_imports

def test_basic_functionality():
    """Test basic functionality without external dependencies."""
    print("\nTesting basic functionality...")
    
    try:
        # Test config loading
        from src.config import config_manager
        config = config_manager.load_config()
        print("✅ Config loading")
        
        # Test dataclass imports
        from src.config import GitLabConfig, GitHubConfig, ComposerConfig
        print("✅ Dataclass imports")
        
        # Test client imports
        from src.gitlab_client import GitLabClient
        from src.github_client import GitHubClient
        print("✅ Client class imports")
        
        # Test manager imports
        from src.repository_manager import RepositoryManager
        from src.composer_manager import ComposerManager
        print("✅ Manager class imports")
        
        # Test services import
        from src.services import UserRepositoryService, GroupRepositoryService, ComposerService, GitHubUserService, GitHubOrganizationService
        print("✅ Service class imports")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_cli_help():
    """Test that CLI help works."""
    print("\nTesting CLI help...")
    
    try:
        result = subprocess.run(
            [sys.executable, 'cli.py', '--help'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ CLI help command works")
            return True
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ CLI help timed out")
        return False
    except Exception as e:
        print(f"❌ CLI help error: {e}")
        return False

def test_syntax():
    """Test Python syntax for all Python files."""
    print("\nTesting Python syntax...")
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        if 'venv' in root or '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    syntax_errors = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                compile(f.read(), file_path, 'exec')
            print(f"✅ {file_path}")
        except SyntaxError as e:
            print(f"❌ {file_path}: {e}")
            syntax_errors.append((file_path, e))
        except Exception as e:
            print(f"⚠️  {file_path}: {e}")
            syntax_errors.append((file_path, e))
    
    return syntax_errors

def test_dependencies():
    """Test that all required dependencies can be imported."""
    print("\nTesting dependencies...")
    
    dependencies = [
        'click',
        'requests', 
        'yaml',
        'concurrent.futures',
        'pathlib',
        'typing'
    ]
    
    failed_deps = []
    
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError as e:
            print(f"❌ {dep}: {e}")
            failed_deps.append((dep, e))
        except Exception as e:
            print(f"⚠️  {dep}: {e}")
            failed_deps.append((dep, e))
    
    return failed_deps

def main():
    """Run all tests."""
    print(f"Testing with Python {sys.version}")
    print("=" * 50)
    
    # Test syntax first
    syntax_errors = test_syntax()
    
    # Test dependencies
    dep_errors = test_dependencies()
    
    # Test imports
    import_errors = test_imports()
    
    # Test basic functionality
    basic_ok = test_basic_functionality()
    
    # Test CLI
    cli_ok = test_cli_help()
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Python version: {sys.version}")
    print(f"Syntax errors: {len(syntax_errors)}")
    print(f"Dependency errors: {len(dep_errors)}")
    print(f"Import errors: {len(import_errors)}")
    print(f"Basic functionality: {'✅ PASS' if basic_ok else '❌ FAIL'}")
    print(f"CLI help: {'✅ PASS' if cli_ok else '❌ FAIL'}")
    
    if syntax_errors or dep_errors or import_errors or not basic_ok or not cli_ok:
        print("\n❌ Some tests failed!")
        return 1
    else:
        print("\n✅ All tests passed!")
        return 0

if __name__ == '__main__':
    sys.exit(main()) 