import requests
import sys
from typing import List, Dict, Any, Optional
from .config import GitLabConfig


class GitLabClient:
    """Client for interacting with GitLab API"""
    
    def __init__(self, config: GitLabConfig):
        self.config = config
        self.headers = {
            "Private-Token": config.private_token,
            "Content-Type": "application/json"
        }
    
    def get_current_user_id(self) -> int:
        """Fetches the ID of the authenticated user."""
        user_api_url = f"{self.config.url}/api/v4/user"
        
        try:
            response = requests.get(user_api_url, headers=self.headers)
            response.raise_for_status()
            user_data = response.json()
            return user_data['id']
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                print(f"Error: Authentication failed when getting user ID. Check your GitLab Token and URL. {e}")
            else:
                print(f"HTTP Error fetching user ID: {e}")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred during user ID API request: {e}")
            sys.exit(1)
    
    def get_user_owned_projects(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Fetches a list of projects directly owned by the specified user ID.
        Includes both public and private personal projects.
        """
        projects = []
        page = 1
        per_page = 100  # Max per_page for GitLab API
        
        api_url = f"{self.config.url}/api/v4/users/{user_id}/projects?per_page={per_page}"
        
        print(f"Fetching personal project list for user ID {user_id} from {self.config.url}...")
        
        while True:
            paged_url = f"{api_url}&page={page}"
            try:
                response = requests.get(paged_url, headers=self.headers)
                response.raise_for_status()
                current_page_projects = response.json()
                
                if not current_page_projects:
                    break  # No more projects
                
                for project_data in current_page_projects:
                    projects.append(project_data)
                
                # Check if 'X-Next-Page' header exists to determine if there are more pages
                if 'X-Next-Page' in response.headers and response.headers['X-Next-Page']:
                    page += 1
                else:
                    break  # No more pages
                    
            except requests.exceptions.HTTPError as e:
                if response.status_code == 401:
                    print(f"Error: Authentication failed. Check your GitLab Token and URL. {e}")
                elif response.status_code == 403:
                    print(f"Error: API rate limit exceeded or forbidden. {e}")
                else:
                    print(f"HTTP Error fetching projects: {e}")
                sys.exit(1)
            except requests.exceptions.RequestException as e:
                print(f"An unexpected error occurred during API request: {e}")
                sys.exit(1)
        
        print(f"Found {len(projects)} personal projects.")
        return projects
    
    def get_group_projects(self, group_id: int) -> List[Dict[str, Any]]:
        """
        Fetches a list of all projects within a specified GitLab group.
        Includes both public and private projects accessible via the token.
        """
        projects = []
        page = 1
        per_page = 100  # Max per_page for GitLab API
        
        api_url = f"{self.config.url}/api/v4/groups/{group_id}/projects?per_page={per_page}"
        
        print(f"  Fetching projects for group ID {group_id}...")
        
        while True:
            paged_url = f"{api_url}&page={page}"
            try:
                response = requests.get(paged_url, headers=self.headers)
                response.raise_for_status()
                current_page_projects = response.json()
                
                if not current_page_projects:
                    break  # No more projects
                
                for project_data in current_page_projects:
                    projects.append(project_data)
                
                if 'X-Next-Page' in response.headers and response.headers['X-Next-Page']:
                    page += 1
                else:
                    break
                    
            except requests.exceptions.HTTPError as e:
                if response.status_code == 401:
                    print(f"  Error for group {group_id}: Authentication failed. Check token. {e}")
                elif response.status_code == 403:
                    print(f"  Error for group {group_id}: API rate limit exceeded or forbidden. {e}")
                elif response.status_code == 404:
                    print(f"  Error: Group with ID {group_id} not found or you don't have access. {e}")
                else:
                    print(f"  HTTP Error fetching projects for group {group_id}: {e}")
                break
            except requests.exceptions.RequestException as e:
                print(f"  An unexpected error for group {group_id} occurred during API request: {e}")
                break
        
        return projects 