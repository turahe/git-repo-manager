import os
import subprocess
import concurrent.futures
from typing import List, Dict, Any, Tuple, Optional
from .config import RepositoryConfig


class RepositoryManager:
    """Manages Git repository operations"""
    
    def __init__(self, config: RepositoryConfig):
        self.config = config
    
    def clone_or_pull_repo(self, repo_url: str, repo_name_with_namespace: str, output_dir: Optional[str] = None) -> Tuple[str, str]:
        """
        Clones a repository if it doesn't exist, otherwise pulls updates.
        Returns the name of the repository and a status message.
        
        Args:
            repo_url: The URL of the repository to clone
            repo_name_with_namespace: The name/namespace of the repository
            output_dir: Optional custom output directory (overrides config.repo_dir)
        """
        base_dir = output_dir if output_dir else self.config.repo_dir
        repo_path = os.path.join(base_dir, repo_name_with_namespace)
        
        # Ensure the parent directories for the repo_path exist
        os.makedirs(os.path.dirname(repo_path), exist_ok=True)
        
        if os.path.exists(repo_path):
            print(f"  Processing '{repo_name_with_namespace}': Exists. Pulling...")
            try:
                subprocess.run(["git", "pull"], cwd=repo_path, check=True, capture_output=True, text=True)
                status_message = f"Pulled changes for '{repo_name_with_namespace}'."
            except subprocess.CalledProcessError as e:
                status_message = f"Error pulling changes for '{repo_name_with_namespace}': {e.stderr.strip()}"
            except FileNotFoundError:
                status_message = f"Error: 'git' command not found for '{repo_name_with_namespace}'. Make sure Git is installed and in your PATH."
        else:
            print(f"  Processing '{repo_name_with_namespace}': Cloning...")
            try:
                subprocess.run(["git", "clone", repo_url, repo_path], cwd=base_dir, check=True, capture_output=True, text=True)
                status_message = f"Cloned '{repo_name_with_namespace}'."
            except subprocess.CalledProcessError as e:
                status_message = f"Error cloning '{repo_name_with_namespace}': {e.stderr.strip()}"
            except FileNotFoundError:
                status_message = f"Error: 'git' command not found for '{repo_name_with_namespace}'. Make sure Git is installed and in your PATH."
        
        return repo_name_with_namespace, status_message
    
    def clone_or_pull_all_branches(self, repo_url: str, local_repo_path_relative: str, output_dir: Optional[str] = None) -> Tuple[str, str, str]:
        """
        Clones a repository if it doesn't exist, otherwise fetches all branches and
        creates local branches for all remote branches.
        Returns the repository's relative path, a status ('SUCCESS'/'FAILED'), and a status message.
        
        Args:
            repo_url: The URL of the repository to clone
            local_repo_path_relative: The relative path for the repository
            output_dir: Optional custom output directory (overrides config.repo_dir)
        """
        base_dir = output_dir if output_dir else self.config.repo_dir
        full_local_repo_path = os.path.join(base_dir, local_repo_path_relative)
        status_type = "FAILED"
        status_message = ""
        
        os.makedirs(os.path.dirname(full_local_repo_path), exist_ok=True)
        
        if os.path.exists(full_local_repo_path):
            print(f"  Processing '{local_repo_path_relative}': Exists. Fetching all branches and creating local copies...")
            try:
                subprocess.run(["git", "fetch", "--all", "--prune"], cwd=full_local_repo_path, check=True, capture_output=True, text=True)
                
                result = subprocess.run(["git", "branch", "-r"], cwd=full_local_repo_path, check=True, capture_output=True, text=True)
                remote_branches = [
                    branch.strip().replace("origin/", "")
                    for branch in result.stdout.splitlines()
                    if "->" not in branch and "origin/" in branch
                ]
                
                for branch in remote_branches:
                    check_local_branch = subprocess.run(["git", "show-ref", "--verify", f"refs/heads/{branch}"], cwd=full_local_repo_path, capture_output=True, text=True)
                    if check_local_branch.returncode != 0:
                        subprocess.run(["git", "branch", branch, f"origin/{branch}"], cwd=full_local_repo_path, check=True, capture_output=True, text=True)
                
                status_type = "SUCCESS"
                status_message = f"Fetched all branches and created local branches for '{local_repo_path_relative}'."
                
            except subprocess.CalledProcessError as e:
                status_message = f"Error processing all branches for '{local_repo_path_relative}': {e.stderr.strip()}"
            except FileNotFoundError:
                status_message = f"Error: 'git' command not found for '{local_repo_path_relative}'. Make sure Git is installed and in your PATH."
        else:
            print(f"  Processing '{local_repo_path_relative}': Cloning...")
            try:
                subprocess.run(["git", "clone", repo_url, full_local_repo_path], cwd=base_dir, check=True, capture_output=True, text=True)
                
                result = subprocess.run(["git", "branch", "-r"], cwd=full_local_repo_path, check=True, capture_output=True, text=True)
                remote_branches = [
                    branch.strip().replace("origin/", "")
                    for branch in result.stdout.splitlines()
                    if "->" not in branch and "origin/" in branch
                ]
                
                for branch in remote_branches:
                    check_local_branch = subprocess.run(["git", "show-ref", "--verify", f"refs/heads/{branch}"], cwd=full_local_repo_path, capture_output=True, text=True)
                    if check_local_branch.returncode != 0:
                        subprocess.run(["git", "branch", branch, f"origin/{branch}"], cwd=full_local_repo_path, check=True, capture_output=True, text=True)
                
                status_type = "SUCCESS"
                status_message = f"Cloned '{local_repo_path_relative}' and created all local branches."
            except subprocess.CalledProcessError as e:
                status_message = f"Error cloning '{local_repo_path_relative}': {e.stderr.strip()}"
            except FileNotFoundError:
                status_message = f"Error: 'git' command not found for '{local_repo_path_relative}'. Make sure Git is installed and in your PATH."
        
        return local_repo_path_relative, status_type, status_message
    
    def process_user_projects(self, projects: List[Dict[str, Any]], output_dir: Optional[str] = None) -> None:
        """Process user-owned projects with concurrent execution"""
        if not projects:
            print("No personal projects found or an error occurred. Exiting.")
            return
        
        print(f"\nStarting concurrent personal project download/update process with {self.config.max_concurrent_downloads} workers...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.max_concurrent_downloads) as executor:
            futures = {
                executor.submit(self.clone_or_pull_repo, project['ssh_url_to_repo'], project['path_with_namespace'], output_dir): project['path_with_namespace'] 
                for project in projects
            }
            
            for future in concurrent.futures.as_completed(futures):
                repo_name_submitted = futures[future]
                try:
                    repo_name, status_message = future.result()
                    print(f"  -> {status_message}")
                except Exception as exc:
                    print(f"  -> {repo_name_submitted} generated an exception: {exc}")
        
        print("\n--- All personal GitLab projects processed! ---")
    
    def process_group_projects(self, all_projects: List[Dict[str, Any]], output_dir: Optional[str] = None) -> None:
        """Process group projects with concurrent execution"""
        if not all_projects:
            print("No projects found across any specified groups or an error occurred. Exiting.")
            return
        
        print(f"\nTotal projects to process: {len(all_projects)}")
        print(f"Starting concurrent project download/update process with {self.config.max_concurrent_downloads} workers...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.max_concurrent_downloads) as executor:
            futures = {}
            for project in all_projects:
                ssh_url = project['ssh_url_to_repo']
                group_base_name = project['namespace']['name']
                project_name = project['name']
                local_repo_path_relative = os.path.join(group_base_name, project_name)
                
                futures[executor.submit(self.clone_or_pull_all_branches, ssh_url, local_repo_path_relative, output_dir)] = local_repo_path_relative
            
            for future in concurrent.futures.as_completed(futures):
                repo_name_submitted = futures[future]
                try:
                    repo_name, status_type, status_message = future.result()
                    print(f"  -> {status_message}")
                except Exception as exc:
                    print(f"  -> {repo_name_submitted} generated an exception: {exc}")
        
        print("\n--- All group GitLab projects processed! ---") 