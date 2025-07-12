import concurrent.futures
from typing import List, Dict, Any, Optional
from .config import GitLabConfig, RepositoryConfig, GroupConfig, GitHubConfig
from .gitlab_client import GitLabClient
from .github_client import GitHubClient
from .repository_manager import RepositoryManager
from .composer_manager import ComposerManager


class UserRepositoryService:
    """Service for managing user-owned repositories"""
    
    def __init__(self, gitlab_config: GitLabConfig, repo_config: RepositoryConfig):
        self.gitlab_client = GitLabClient(gitlab_config)
        self.repo_manager = RepositoryManager(repo_config)
    
    def clone_user_repositories(self, output_dir: Optional[str] = None) -> None:
        """Clone all user-owned repositories"""
        base_dir = output_dir if output_dir else self.repo_manager.config.repo_dir
        print(f"Repositories will be saved in: {base_dir}\n")
        
        # Step 1: Get the authenticated user's ID
        print("Getting current user ID...")
        user_id = self.gitlab_client.get_current_user_id()
        print(f"Authenticated user ID: {user_id}\n")
        
        # Step 2: Get only the projects owned by this user ID
        all_projects = self.gitlab_client.get_user_owned_projects(user_id)
        
        # Step 3: Process the projects with custom output directory
        self.repo_manager.process_user_projects(all_projects, output_dir)


class GroupRepositoryService:
    """Service for managing group repositories"""
    
    def __init__(self, gitlab_config: GitLabConfig, repo_config: RepositoryConfig, group_config: GroupConfig):
        self.gitlab_client = GitLabClient(gitlab_config)
        self.repo_manager = RepositoryManager(repo_config)
        self.group_config = group_config
    
    def clone_group_repositories(self, output_dir: Optional[str] = None) -> None:
        """Clone all repositories from specified groups"""
        if not self.group_config.target_group_ids:
            print("ERROR: Please update TARGET_GROUP_IDS in the configuration with a list of your actual GitLab Group IDs.")
            return
        
        base_dir = output_dir if output_dir else self.repo_manager.config.repo_dir
        print(f"Repositories will be saved in: {base_dir}\n")
        
        all_projects_from_groups = []
        print("Collecting projects from specified groups...")
        
        for group_id in self.group_config.target_group_ids:
            group_projects = self.gitlab_client.get_group_projects(group_id)
            all_projects_from_groups.extend(group_projects)
            print(f"  Collected {len(group_projects)} projects from group ID {group_id}.")
        
        # Process the projects with custom output directory
        self.repo_manager.process_group_projects(all_projects_from_groups, output_dir)


class ComposerService:
    """Service for managing Composer operations"""
    
    def __init__(self):
        self.composer_manager = ComposerManager()
    
    def update_composer_dependencies(self, search_directory: str) -> None:
        """Update Composer dependencies in the specified directory"""
        self.composer_manager.find_and_update_composer(search_directory)


class GitHubUserService:
    """Service for managing GitHub user repositories"""
    
    def __init__(self, github_config: GitHubConfig, repo_config: RepositoryConfig):
        self.github_client = GitHubClient(github_config)
        self.repo_manager = RepositoryManager(repo_config)
    
    def clone_user_repositories(self, username: Optional[str] = None, output_dir: Optional[str] = None) -> None:
        """Clone repositories from a GitHub user"""
        base_dir = output_dir if output_dir else self.repo_manager.config.repo_dir
        print(f"Repositories will be saved in: {base_dir}\n")
        
        if username:
            # Clone repositories from specific user
            repositories = self.github_client.get_user_repositories(username)
        else:
            # Clone repositories from authenticated user
            repositories = self.github_client.get_authenticated_user_repositories()
        
        if not repositories:
            print("No repositories found or an error occurred. Exiting.")
            return
        
        print(f"\nStarting concurrent repository download/update process with {self.repo_manager.config.max_concurrent_downloads} workers...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.repo_manager.config.max_concurrent_downloads) as executor:
            futures = {}
            for repo in repositories:
                clone_url = repo['clone_url']
                repo_name = repo['full_name']
                
                futures[executor.submit(self.repo_manager.clone_or_pull_repo, clone_url, repo_name, output_dir)] = repo_name
            
            for future in concurrent.futures.as_completed(futures):
                repo_name_submitted = futures[future]
                try:
                    repo_name, status_message = future.result()
                    print(f"  -> {status_message}")
                except Exception as exc:
                    print(f"  -> {repo_name_submitted} generated an exception: {exc}")
        
        print("\n--- All GitHub user repositories processed! ---")


class GitHubOrganizationService:
    """Service for managing GitHub organization repositories"""
    
    def __init__(self, github_config: GitHubConfig, repo_config: RepositoryConfig):
        self.github_client = GitHubClient(github_config)
        self.repo_manager = RepositoryManager(repo_config)
    
    def clone_organization_repositories(self, org_name: str, output_dir: Optional[str] = None) -> None:
        """Clone repositories from a GitHub organization"""
        base_dir = output_dir if output_dir else self.repo_manager.config.repo_dir
        print(f"Repositories will be saved in: {base_dir}\n")
        
        repositories = self.github_client.get_organization_repositories(org_name)
        
        if not repositories:
            print("No repositories found or an error occurred. Exiting.")
            return
        
        print(f"\nStarting concurrent repository download/update process with {self.repo_manager.config.max_concurrent_downloads} workers...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.repo_manager.config.max_concurrent_downloads) as executor:
            futures = {}
            for repo in repositories:
                clone_url = repo['clone_url']
                repo_name = repo['full_name']
                
                futures[executor.submit(self.repo_manager.clone_or_pull_repo, clone_url, repo_name, output_dir)] = repo_name
            
            for future in concurrent.futures.as_completed(futures):
                repo_name_submitted = futures[future]
                try:
                    repo_name, status_message = future.result()
                    print(f"  -> {status_message}")
                except Exception as exc:
                    print(f"  -> {repo_name_submitted} generated an exception: {exc}")
        
        print("\n--- All GitHub organization repositories processed! ---") 