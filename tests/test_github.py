#!/usr/bin/env python3
"""
Simple test script for GitHub functionality
"""

import os
import sys
from src.config import GitHubConfig, RepositoryConfig
from src.github_client import GitHubClient
from src.services import GitHubUserService, GitHubOrganizationService


def test_github_config():
    """Test GitHub configuration loading"""
    print("Testing GitHub configuration...")
    
    # Test from environment
    config = GitHubConfig.from_env()
    print(f"GitHub URL: {config.url}")
    print(f"Token configured: {'Yes' if config.access_token else 'No'}")
    
    # Test from config file
    try:
        config = GitHubConfig.from_config()
        print(f"Config file - GitHub URL: {config.url}")
        print(f"Config file - Token configured: {'Yes' if config.access_token else 'No'}")
    except Exception as e:
        print(f"Config file error: {e}")


def test_github_client():
    """Test GitHub client functionality"""
    print("\nTesting GitHub client...")
    
    config = GitHubConfig.from_env()
    if not config.access_token:
        print("No GitHub token found. Skipping client tests.")
        return
    
    client = GitHubClient(config)
    
    try:
        # Test current user
        user = client.get_current_user()
        print(f"Authenticated as: {user.get('login', 'Unknown')}")
        
        # Test user repositories (limit to first few)
        repos = client.get_user_repositories(user['login'])
        print(f"Found {len(repos)} repositories for user {user['login']}")
        
        if repos:
            print("Sample repositories:")
            for repo in repos[:3]:
                print(f"  - {repo['full_name']}: {repo['clone_url']}")
                
    except Exception as e:
        print(f"GitHub client test failed: {e}")


def test_github_services():
    """Test GitHub services"""
    print("\nTesting GitHub services...")
    
    github_config = GitHubConfig.from_env()
    repo_config = RepositoryConfig.from_env()
    
    if not github_config.access_token:
        print("No GitHub token found. Skipping service tests.")
        return
    
    try:
        # Test user service
        user_service = GitHubUserService(github_config, repo_config)
        print("GitHubUserService created successfully")
        
        # Test organization service
        org_service = GitHubOrganizationService(github_config, repo_config)
        print("GitHubOrganizationService created successfully")
        
    except Exception as e:
        print(f"Service test failed: {e}")


if __name__ == "__main__":
    print("GitHub Functionality Test")
    print("=" * 30)
    
    test_github_config()
    test_github_client()
    test_github_services()
    
    print("\nTest completed!") 