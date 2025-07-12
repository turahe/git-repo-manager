import requests
import sys
from typing import List, Dict, Any, Optional
from .config import GitHubConfig


class GitHubClient:
    """Client for interacting with GitHub API"""
    
    def __init__(self, config: GitHubConfig):
        self.config = config
        self.headers = {
            "Authorization": f"token {config.access_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "git-repo-manager/1.0"
        }
    
    def get_current_user(self) -> Dict[str, Any]:
        """Fetches the authenticated user information."""
        user_api_url = "https://api.github.com/user"
        
        try:
            response = requests.get(user_api_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                print(f"Error: Authentication failed when getting user info. Check your GitHub Token. {e}")
            else:
                print(f"HTTP Error fetching user info: {e}")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred during user info API request: {e}")
            sys.exit(1)
    
    def get_user_repositories(self, username: str) -> List[Dict[str, Any]]:
        """
        Fetches a list of repositories for a specific GitHub user.
        Includes both public and private repositories accessible via the token.
        """
        repositories = []
        page = 1
        per_page = 100  # Max per_page for GitHub API
        
        api_url = f"https://api.github.com/users/{username}/repos?per_page={per_page}"
        
        print(f"Fetching repositories for GitHub user '{username}'...")
        
        while True:
            paged_url = f"{api_url}&page={page}"
            try:
                response = requests.get(paged_url, headers=self.headers)
                response.raise_for_status()
                current_page_repos = response.json()
                
                if not current_page_repos:
                    break  # No more repositories
                
                for repo_data in current_page_repos:
                    repositories.append(repo_data)
                
                # Check if there are more pages
                if 'next' in response.links:
                    page += 1
                else:
                    break
                    
            except requests.exceptions.HTTPError as e:
                if response.status_code == 401:
                    print(f"Error: Authentication failed. Check your GitHub Token. {e}")
                elif response.status_code == 403:
                    print(f"Error: API rate limit exceeded or forbidden. {e}")
                elif response.status_code == 404:
                    print(f"Error: User '{username}' not found. {e}")
                else:
                    print(f"HTTP Error fetching repositories: {e}")
                break
            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred during API request: {e}")
                break
        
        print(f"Found {len(repositories)} repositories for user '{username}'.")
        return repositories
    
    def get_organization_repositories(self, org_name: str) -> List[Dict[str, Any]]:
        """
        Fetches a list of repositories for a specific GitHub organization.
        Includes both public and private repositories accessible via the token.
        """
        repositories = []
        page = 1
        per_page = 100  # Max per_page for GitHub API
        
        api_url = f"https://api.github.com/orgs/{org_name}/repos?per_page={per_page}"
        
        print(f"Fetching repositories for GitHub organization '{org_name}'...")
        
        while True:
            paged_url = f"{api_url}&page={page}"
            try:
                response = requests.get(paged_url, headers=self.headers)
                response.raise_for_status()
                current_page_repos = response.json()
                
                if not current_page_repos:
                    break  # No more repositories
                
                for repo_data in current_page_repos:
                    repositories.append(repo_data)
                
                # Check if there are more pages
                if 'next' in response.links:
                    page += 1
                else:
                    break
                    
            except requests.exceptions.HTTPError as e:
                if response.status_code == 401:
                    print(f"Error: Authentication failed. Check your GitHub Token. {e}")
                elif response.status_code == 403:
                    print(f"Error: API rate limit exceeded or forbidden. {e}")
                elif response.status_code == 404:
                    print(f"Error: Organization '{org_name}' not found. {e}")
                else:
                    print(f"HTTP Error fetching repositories: {e}")
                break
            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred during API request: {e}")
                break
        
        print(f"Found {len(repositories)} repositories for organization '{org_name}'.")
        return repositories
    
    def get_authenticated_user_repositories(self) -> List[Dict[str, Any]]:
        """
        Fetches a list of repositories owned by the authenticated user.
        Includes both public and private repositories.
        """
        repositories = []
        page = 1
        per_page = 100  # Max per_page for GitHub API
        
        api_url = f"https://api.github.com/user/repos?per_page={per_page}"
        
        print("Fetching repositories for authenticated GitHub user...")
        
        while True:
            paged_url = f"{api_url}&page={page}"
            try:
                response = requests.get(paged_url, headers=self.headers)
                response.raise_for_status()
                current_page_repos = response.json()
                
                if not current_page_repos:
                    break  # No more repositories
                
                for repo_data in current_page_repos:
                    repositories.append(repo_data)
                
                # Check if there are more pages
                if 'next' in response.links:
                    page += 1
                else:
                    break
                    
            except requests.exceptions.HTTPError as e:
                if response.status_code == 401:
                    print(f"Error: Authentication failed. Check your GitHub Token. {e}")
                elif response.status_code == 403:
                    print(f"Error: API rate limit exceeded or forbidden. {e}")
                else:
                    print(f"HTTP Error fetching repositories: {e}")
                break
            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred during API request: {e}")
                break
        
        print(f"Found {len(repositories)} repositories for authenticated user.")
        return repositories 