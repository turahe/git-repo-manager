# API Documentation

This documentation is auto-generated from the source code.

## src.config

### Classes

#### ComposerConfig

Configuration for Composer operations

**Methods:**

- `__eq__(self, other)`

- `__init__(self, enabled: bool, auto_update: bool) -> None`

- `__repr__(self)`

#### ConfigManager

Manages configuration loading from YAML file and environment variables

**Methods:**

- `__init__(self, config_file: str = 'config.yml')`

- `_get_default_config(self) -> Dict[str, Any]`
  - Get default configuration.

- `_load_yaml_config(self) -> Dict[str, Any]`
  - Load configuration from YAML file.

- `_merge_with_env(self, config: Dict[str, Any]) -> Dict[str, Any]`
  - Merge YAML config with environment variables (env vars take precedence).

- `load_config(self) -> Dict[str, Any]`
  - Load configuration from YAML file with environment variable fallback.

#### GitHubConfig

Configuration for GitHub API access

**Methods:**

- `__eq__(self, other)`

- `__init__(self, access_token: str, url: str = 'https://api.github.com') -> None`

- `__repr__(self)`

#### GitLabConfig

Configuration for GitLab API access

**Methods:**

- `__eq__(self, other)`

- `__init__(self, url: str, private_token: str) -> None`

- `__repr__(self)`

#### GroupConfig

Configuration for group operations

**Methods:**

- `__eq__(self, other)`

- `__init__(self, target_group_ids: List[int]) -> None`

- `__repr__(self)`

#### RepositoryConfig

Configuration for repository operations

**Methods:**

- `__eq__(self, other)`

- `__init__(self, repo_dir: str, max_concurrent_downloads: int) -> None`

- `__repr__(self)`

## src.gitlab_client

### Classes

#### GitLabClient

Client for interacting with GitLab API

**Methods:**

- `__init__(self, config: src.config.GitLabConfig)`

- `get_current_user_id(self) -> int`
  - Fetches the ID of the authenticated user.

- `get_group_projects(self, group_id: int) -> List[Dict[str, Any]]`
  - 
Fetches a list of all projects within a specified GitLab group.

- `get_user_owned_projects(self, user_id: int) -> List[Dict[str, Any]]`
  - 
Fetches a list of projects directly owned by the specified user ID.

## src.github_client

### Classes

#### GitHubClient

Client for interacting with GitHub API

**Methods:**

- `__init__(self, config: src.config.GitHubConfig)`

- `get_authenticated_user_repositories(self) -> List[Dict[str, Any]]`
  - 
Fetches a list of repositories owned by the authenticated user.

- `get_current_user(self) -> Dict[str, Any]`
  - Fetches the authenticated user information.

- `get_organization_repositories(self, org_name: str) -> List[Dict[str, Any]]`
  - 
Fetches a list of repositories for a specific GitHub organization.

- `get_user_repositories(self, username: str) -> List[Dict[str, Any]]`
  - 
Fetches a list of repositories for a specific GitHub user.

## src.repository_manager

### Classes

#### RepositoryManager

Manages Git repository operations

**Methods:**

- `__init__(self, config: src.config.RepositoryConfig)`

- `clone_or_pull_all_branches(self, repo_url: str, local_repo_path_relative: str, output_dir: Optional[str] = None) -> Tuple[str, str, str]`
  - 
Clones a repository if it doesn't exist, otherwise fetches all branches and
creates local branches for all remote branches.

- `clone_or_pull_repo(self, repo_url: str, repo_name_with_namespace: str, output_dir: Optional[str] = None) -> Tuple[str, str]`
  - 
Clones a repository if it doesn't exist, otherwise pulls updates.

- `process_group_projects(self, all_projects: List[Dict[str, Any]], output_dir: Optional[str] = None) -> None`
  - Process group projects with concurrent execution.

- `process_user_projects(self, projects: List[Dict[str, Any]], output_dir: Optional[str] = None) -> None`
  - Process user-owned projects with concurrent execution.

## src.composer_manager

### Classes

#### ComposerManager

Manages Composer operations

**Methods:**

- `__init__(self)`

- `_find_composer_command(self) -> str`
  - Find the appropriate composer command for the system.

- `find_and_update_composer(self, root_dir: str) -> None`
  - 
Traverses a root directory and its subdirectories to find composer.

## src.services

### Classes

#### ComposerService

Service for managing Composer operations

**Methods:**

- `__init__(self)`

- `update_composer_dependencies(self, search_directory: str) -> None`
  - Update Composer dependencies in the specified directory.

#### GitHubOrganizationService

Service for managing GitHub organization repositories

**Methods:**

- `__init__(self, github_config: src.config.GitHubConfig, repo_config: src.config.RepositoryConfig)`

- `clone_organization_repositories(self, org_name: str, output_dir: Optional[str] = None) -> None`
  - Clone repositories from a GitHub organization.

#### GitHubUserService

Service for managing GitHub user repositories

**Methods:**

- `__init__(self, github_config: src.config.GitHubConfig, repo_config: src.config.RepositoryConfig)`

- `clone_user_repositories(self, username: Optional[str] = None, output_dir: Optional[str] = None) -> None`
  - Clone repositories from a GitHub user.

#### GroupRepositoryService

Service for managing group repositories

**Methods:**

- `__init__(self, gitlab_config: src.config.GitLabConfig, repo_config: src.config.RepositoryConfig, group_config: src.config.GroupConfig)`

- `clone_group_repositories(self, output_dir: Optional[str] = None) -> None`
  - Clone all repositories from specified groups.

#### UserRepositoryService

Service for managing user-owned repositories

**Methods:**

- `__init__(self, gitlab_config: src.config.GitLabConfig, repo_config: src.config.RepositoryConfig)`

- `clone_user_repositories(self, output_dir: Optional[str] = None) -> None`
  - Clone all user-owned repositories.
