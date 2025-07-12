#!/usr/bin/env python3
"""
Comprehensive test script to verify codebase compatibility across Python versions 3.10, 3.11, 3.12, and 3.13.
This script can be run locally to test imports and basic functionality across multiple Python versions.
"""

import sys
import subprocess
import importlib
import os
import platform
from pathlib import Path

def get_python_versions():
    """Get available Python versions to test."""
    versions = ['3.10', '3.11', '3.12', '3.13']
    available_versions = []
    
    for version in versions:
        try:
            # Try to find Python executable
            if platform.system() == "Windows":
                # On Windows, try python3.x or py -3.x
                cmd = f'py -{version} --version'
            else:
                # On Unix-like systems, try python3.x
                cmd = f'python{version} --version'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                available_versions.append(version)
                print(f"✅ Found Python {version}")
            else:
                print(f"❌ Python {version} not found")
        except Exception as e:
            print(f"❌ Error checking Python {version}: {e}")
    
    return available_versions

def test_python_version(version):
    """Test a specific Python version."""
    print(f"\n{'='*60}")
    print(f"Testing Python {version}")
    print(f"{'='*60}")
    
    # Determine the Python command
    if platform.system() == "Windows":
        python_cmd = f'py -{version}'
    else:
        python_cmd = f'python{version}'
    
    # Test 1: Syntax check
    print(f"\n1. Testing syntax with {python_cmd}...")
    syntax_ok = test_syntax_with_python(python_cmd)
    
    # Test 2: Import test
    print(f"\n2. Testing imports with {python_cmd}...")
    import_ok = test_imports_with_python(python_cmd)
    
    # Test 3: Basic functionality
    print(f"\n3. Testing basic functionality with {python_cmd}...")
    basic_ok = test_basic_functionality_with_python(python_cmd)
    
    # Test 4: CLI help
    print(f"\n4. Testing CLI help with {python_cmd}...")
    cli_ok = test_cli_help_with_python(python_cmd)
    
    # Summary for this version
    print(f"\n{'='*40}")
    print(f"Python {version} Results:")
    print(f"Syntax: {'✅ PASS' if syntax_ok else '❌ FAIL'}")
    print(f"Imports: {'✅ PASS' if import_ok else '❌ FAIL'}")
    print(f"Basic functionality: {'✅ PASS' if basic_ok else '❌ FAIL'}")
    print(f"CLI help: {'✅ PASS' if cli_ok else '❌ FAIL'}")
    
    return {
        'version': version,
        'syntax': syntax_ok,
        'imports': import_ok,
        'basic': basic_ok,
        'cli': cli_ok
    }

def test_syntax_with_python(python_cmd):
    """Test Python syntax using the specified Python command."""
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
            cmd = f'{python_cmd} -m py_compile "{file_path}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path}: {result.stderr.strip()}")
                syntax_errors.append(file_path)
        except Exception as e:
            print(f"  ⚠️  {file_path}: {e}")
            syntax_errors.append(file_path)
    
    return len(syntax_errors) == 0

def test_imports_with_python(python_cmd):
    """Test module imports using the specified Python command."""
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
            cmd = f'{python_cmd} -c "import {module_name}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✅ {module_name}")
            else:
                print(f"  ❌ {module_name}: {result.stderr.strip()}")
                failed_imports.append(module_name)
        except Exception as e:
            print(f"  ⚠️  {module_name}: {e}")
            failed_imports.append(module_name)
    
    return len(failed_imports) == 0

def test_basic_functionality_with_python(python_cmd):
    """Test basic functionality using the specified Python command."""
    test_code = '''
import sys
try:
    # Test config loading
    from src.config import config_manager
    config = config_manager.load_config()
    print("  ✅ Config loading")
    
    # Test dataclass imports
    from src.config import GitLabConfig, GitHubConfig, ComposerConfig
    print("  ✅ Dataclass imports")
    
    # Test client imports
    from src.gitlab_client import GitLabClient
    from src.github_client import GitHubClient
    print("  ✅ Client class imports")
    
    # Test manager imports
    from src.repository_manager import RepositoryManager
    from src.composer_manager import ComposerManager
    print("  ✅ Manager class imports")
    
    # Test services import
    from src.services import UserRepositoryService, GroupRepositoryService, ComposerService, GitHubUserService, GitHubOrganizationService
    print("  ✅ Service class imports")
    
    print("  ✅ All basic functionality tests passed")
    sys.exit(0)
except Exception as e:
    print(f"  ❌ Basic functionality test failed: {e}")
    sys.exit(1)
'''
    
    try:
        result = subprocess.run(
            f'{python_cmd} -c "{test_code}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print(result.stderr.strip())
            return False
    except subprocess.TimeoutExpired:
        print("  ❌ Basic functionality test timed out")
        return False
    except Exception as e:
        print(f"  ❌ Basic functionality test error: {e}")
        return False

def test_cli_help_with_python(python_cmd):
    """Test CLI help using the specified Python command."""
    try:
        result = subprocess.run(
            f'{python_cmd} cli.py --help',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("  ✅ CLI help command works")
            return True
        else:
            print(f"  ❌ CLI help failed: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("  ❌ CLI help timed out")
        return False
    except Exception as e:
        print(f"  ❌ CLI help error: {e}")
        return False

def main():
    """Run tests across all available Python versions."""
    print("Python Version Compatibility Test")
    print("=" * 60)
    print(f"Current Python: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    
    # Get available Python versions
    print("\nChecking available Python versions...")
    available_versions = get_python_versions()
    
    if not available_versions:
        print("\n❌ No Python versions found to test!")
        return 1
    
    print(f"\nFound {len(available_versions)} Python version(s) to test: {', '.join(available_versions)}")
    
    # Test each version
    results = []
    for version in available_versions:
        result = test_python_version(version)
        results.append(result)
    
    # Final summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    
    all_passed = True
    for result in results:
        version = result['version']
        passed = result['syntax'] and result['imports'] and result['basic'] and result['cli']
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"Python {version}: {status}")
        
        if not passed:
            all_passed = False
            print(f"  - Syntax: {'✅' if result['syntax'] else '❌'}")
            print(f"  - Imports: {'✅' if result['imports'] else '❌'}")
            print(f"  - Basic: {'✅' if result['basic'] else '❌'}")
            print(f"  - CLI: {'✅' if result['cli'] else '❌'}")
    
    if all_passed:
        print(f"\n🎉 All Python versions passed all tests!")
        return 0
    else:
        print(f"\n⚠️  Some Python versions failed some tests.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 