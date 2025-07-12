#!/usr/bin/env python3
"""
Test script for output directory feature
"""

import os
import tempfile
import shutil
from src.config import RepositoryConfig
from src.repository_manager import RepositoryManager


def test_output_directory():
    """Test the output directory feature"""
    print("🧪 Testing Output Directory Feature")
    print("=" * 40)
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as temp_dir:
        default_dir = os.path.join(temp_dir, "default")
        custom_dir = os.path.join(temp_dir, "custom")
        
        # Create directories
        os.makedirs(default_dir, exist_ok=True)
        os.makedirs(custom_dir, exist_ok=True)
        
        print(f"Default directory: {default_dir}")
        print(f"Custom directory: {custom_dir}")
        
        # Test configuration
        config = RepositoryConfig(repo_dir=default_dir, max_concurrent_downloads=5)
        repo_manager = RepositoryManager(config)
        
        # Test with default directory
        print("\n📁 Testing with default directory...")
        repo_name = "test/repo1"
        repo_url = "https://github.com/test/repo1.git"
        
        result_name, result_message = repo_manager.clone_or_pull_repo(repo_url, repo_name)
        print(f"Result: {result_message}")
        
        # Test with custom output directory
        print("\n📁 Testing with custom output directory...")
        result_name, result_message = repo_manager.clone_or_pull_repo(repo_url, repo_name, output_dir=custom_dir)
        print(f"Result: {result_message}")
        
        # List directories to see what was created
        print(f"\n📋 Default directory contents:")
        if os.path.exists(default_dir):
            for item in os.listdir(default_dir):
                print(f"  - {item}")
        
        print(f"\n📋 Custom directory contents:")
        if os.path.exists(custom_dir):
            for item in os.listdir(custom_dir):
                print(f"  - {item}")
        
        print("\n✅ Output directory feature test completed!")


if __name__ == "__main__":
    test_output_directory() 