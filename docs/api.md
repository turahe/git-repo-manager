# API Reference

Complete API reference for Git Repository Manager's Python modules and classes.

## Overview

The tool is built with a modular, object-oriented architecture. Each module provides specific functionality:

- **Configuration Management**: `src.config`
- **GitLab Integration**: `src.gitlab_client`
- **GitHub Integration**: `src.github_client`
- **Repository Operations**: `src.repository_manager`
- **Composer Management**: `src.composer_manager`
- **Service Orchestration**: `src.services`

## Configuration Module (`src.config`)

### Classes

#### `ConfigManager`

Manages configuration loading from YAML files and environment variables.

```python
class ConfigManager:
    def __init__(self, config_file: str = "config.yml")
    def load_config(self) -> Dict[str, Any]
    def _load_yaml_config(self) -> Dict[str, Any]
    def _merge_with_env(self, config: Dict[str, Any]) -> Dict[str, Any]
    def _get_default_config(self) -> Dict[str, Any]
```

**Methods:**
- `load_config()`: Load and return configuration
- `_load_yaml_config()`: Load configuration from YAML file
- `_merge_with_env()`: Merge YAML config with environment variables
- `_get_default_config()`: Get default configuration

#### `GitLabConfig`

Configuration for GitLab API access.

```python
@dataclass
class GitLabConfig:
    url: str
    private_token: str
    
    @classmethod
    def from_config(cls) -> 'GitLabConfig'
    @classmethod
    def from_env(cls) -> 'GitLabConfig'
```

**Methods:**
- `from_config()`: Create config from YAML configuration
- `from_env()`: Create config from environment variables

#### `GitHubConfig`

Configuration for GitHub API access.

```python
@dataclass
class GitHubConfig:
    access_token: str
    url: str = "https://api.github.com"
    
    @classmethod
    def from_config(cls) -> 'GitHubConfig'
    @classmethod
    def from_env(cls) -> 'GitHubConfig'
```

**Methods:**
- `from_config()`: Create config from YAML configuration
- `from_env()`: Create config from environment variables

#### `RepositoryConfig`

Configuration for repository operations.

```python
@dataclass
class RepositoryConfig:
    repo_dir: str
    max_concurrent_downloads: int
    
    @classmethod
    def from_config(cls) -> 'RepositoryConfig'
    @classmethod
    def from_env(cls) -> 'RepositoryConfig'
```

**Methods:**
- `from_config()`: Create config from YAML configuration
- `from_env()`: Create config from environment variables

#### `GroupConfig`

Configuration for group operations.

```python
@dataclass
class GroupConfig:
    target_group_ids: List[int]
    
    @classmethod
    def from_config(cls) -> 'GroupConfig'
    @classmethod
    def from_env(cls) -> 'GroupConfig'
```

**Methods:**
- `from_config()`: Create config from YAML configuration
- `from_env()`: Create config from environment variables

#### `ComposerConfig`

Configuration for Composer operations.

```python
@dataclass
class ComposerConfig:
    enabled: bool
    auto_update: bool
    
    @classmethod
    def from_config(cls) -> 'ComposerConfig'
```

**Methods:**
- `from_config()`: Create config from YAML configuration

## GitLab Client Module (`src.gitlab_client`)

### Classes

#### `GitLabClient`

Client for interacting with GitLab API.

```python
class GitLabClient:
    def __init__(self, config: GitLabConfig)
    def get_current_user_id(self) -> int
    def get_user_owned_projects(self, user_id: int) -> List[Dict[str, Any]]
    def get_group_projects(self, group_id: int) -> List[Dict[str, Any]]
```

**Methods:**
- `get_current_user_id()`: Get authenticated user's ID
- `get_user_owned_projects(user_id)`: Get projects owned by user
- `get_group_projects(group_id)`: Get projects in group

**Example:**
```python
from src.config import GitLabConfig
from src.gitlab_client import GitLabClient

config = GitLabConfig.from_config()
client = GitLabClient(config)

user_id = client.get_current_user_id()
projects = client.get_user_owned_projects(user_id)
```

## GitHub Client Module (`src.github_client`)

### Classes

#### `GitHubClient`

Client for interacting with GitHub API.

```python
class GitHubClient:
    def __init__(self, config: GitHubConfig)
    def get_current_user(self) -> Dict[str, Any]
    def get_user_repositories(self, username: str) -> List[Dict[str, Any]]
    def get_organization_repositories(self, org_name: str) -> List[Dict[str, Any]]
    def get_authenticated_user_repositories(self) -> List[Dict[str, Any]]
```

**Methods:**
- `get_current_user()`: Get authenticated user information
- `get_user_repositories(username)`: Get repositories for user
- `get_organization_repositories(org_name)`: Get repositories for organization
- `get_authenticated_user_repositories()`: Get authenticated user's repositories

**Example:**
```python
from src.config import GitHubConfig
from src.github_client import GitHubClient

config = GitHubConfig.from_config()
client = GitHubClient(config)

repos = client.get_user_repositories("john-doe")
```

## Repository Manager Module (`src.repository_manager`)

### Classes

#### `RepositoryManager`

Manages repository cloning and operations.

```python
class RepositoryManager:
    def __init__(self, config: RepositoryConfig)
    def clone_or_pull_repo(self, clone_url: str, repo_name: str, output_dir: Optional[str] = None) -> Tuple[str, str]
    def process_user_projects(self, projects: List[Dict[str, Any]], output_dir: Optional[str] = None) -> None
    def process_group_projects(self, projects: List[Dict[str, Any]], output_dir: Optional[str] = None) -> None
```

**Methods:**
- `clone_or_pull_repo(clone_url, repo_name, output_dir)`: Clone or pull repository
- `process_user_projects(projects, output_dir)`: Process user projects
- `process_group_projects(projects, output_dir)`: Process group projects

**Example:**
```python
from src.config import RepositoryConfig
from src.repository_manager import RepositoryManager

config = RepositoryConfig.from_config()
manager = RepositoryManager(config)

repo_name, status = manager.clone_or_pull_repo(
    "https://github.com/user/repo.git",
    "user/repo",
    "/path/to/output"
)
```

## Composer Manager Module (`src.composer_manager`)

### Classes

#### `ComposerManager`

Manages Composer dependency operations.

```python
class ComposerManager:
    def __init__(self)
    def find_composer_files(self, search_directory: str) -> List[str]
    def update_composer_dependencies(self, composer_file_path: str) -> bool
    def find_and_update_composer(self, search_directory: str) -> None
```

**Methods:**
- `find_composer_files(search_directory)`: Find composer.json files
- `update_composer_dependencies(composer_file_path)`: Update dependencies in composer.json
- `find_and_update_composer(search_directory)`: Find and update all composer files

**Example:**
```python
from src.composer_manager import ComposerManager

manager = ComposerManager()
manager.find_and_update_composer("/path/to/repositories")
```

## Services Module (`src.services`)

### Classes

#### `UserRepositoryService`

Service for managing user-owned repositories.

```python
class UserRepositoryService:
    def __init__(self, gitlab_config: GitLabConfig, repo_config: RepositoryConfig)
    def clone_user_repositories(self, output_dir: Optional[str] = None) -> None
```

**Methods:**
- `clone_user_repositories(output_dir)`: Clone all user-owned repositories

#### `GroupRepositoryService`

Service for managing group repositories.

```python
class GroupRepositoryService:
    def __init__(self, gitlab_config: GitLabConfig, repo_config: RepositoryConfig, group_config: GroupConfig)
    def clone_group_repositories(self, output_dir: Optional[str] = None) -> None
```

**Methods:**
- `clone_group_repositories(output_dir)`: Clone all repositories from specified groups

#### `ComposerService`

Service for managing Composer operations.

```python
class ComposerService:
    def __init__(self)
    def update_composer_dependencies(self, search_directory: str) -> None
```

**Methods:**
- `update_composer_dependencies(search_directory)`: Update Composer dependencies

#### `GitHubUserService`

Service for managing GitHub user repositories.

```python
class GitHubUserService:
    def __init__(self, github_config: GitHubConfig, repo_config: RepositoryConfig)
    def clone_user_repositories(self, username: Optional[str] = None, output_dir: Optional[str] = None) -> None
```

**Methods:**
- `clone_user_repositories(username, output_dir)`: Clone repositories from GitHub user

#### `GitHubOrganizationService`

Service for managing GitHub organization repositories.

```python
class GitHubOrganizationService:
    def __init__(self, github_config: GitHubConfig, repo_config: RepositoryConfig)
    def clone_organization_repositories(self, org_name: str, output_dir: Optional[str] = None) -> None
```

**Methods:**
- `clone_organization_repositories(org_name, output_dir)`: Clone repositories from GitHub organization

## Usage Examples

### Basic Configuration

```python
from src.config import GitLabConfig, RepositoryConfig
from src.gitlab_client import GitLabClient
from src.repository_manager import RepositoryManager

# Load configuration
gitlab_config = GitLabConfig.from_config()
repo_config = RepositoryConfig.from_config()

# Create clients and managers
gitlab_client = GitLabClient(gitlab_config)
repo_manager = RepositoryManager(repo_config)

# Get user projects
user_id = gitlab_client.get_current_user_id()
projects = gitlab_client.get_user_owned_projects(user_id)

# Clone repositories
repo_manager.process_user_projects(projects, "/path/to/output")
```

### Service Usage

```python
from src.config import GitLabConfig, RepositoryConfig, GroupConfig
from src.services import UserRepositoryService, GroupRepositoryService

# Create services
gitlab_config = GitLabConfig.from_config()
repo_config = RepositoryConfig.from_config()
group_config = GroupConfig.from_config()

user_service = UserRepositoryService(gitlab_config, repo_config)
group_service = GroupRepositoryService(gitlab_config, repo_config, group_config)

# Clone repositories
user_service.clone_user_repositories("/path/to/user/repos")
group_service.clone_group_repositories("/path/to/group/repos")
```

### GitHub Integration

```python
from src.config import GitHubConfig, RepositoryConfig
from src.services import GitHubUserService, GitHubOrganizationService

# Create services
github_config = GitHubConfig.from_config()
repo_config = RepositoryConfig.from_config()

user_service = GitHubUserService(github_config, repo_config)
org_service = GitHubOrganizationService(github_config, repo_config)

# Clone repositories
user_service.clone_user_repositories("john-doe", "/path/to/user/repos")
org_service.clone_organization_repositories("my-org", "/path/to/org/repos")
```

### Composer Integration

```python
from src.services import ComposerService

# Create service
composer_service = ComposerService()

# Update dependencies
composer_service.update_composer_dependencies("/path/to/repositories")
```

## Error Handling

### Common Exceptions

```python
# Configuration errors
class ConfigurationError(Exception):
    pass

# Authentication errors
class AuthenticationError(Exception):
    pass

# Network errors
class NetworkError(Exception):
    pass

# Repository errors
class RepositoryError(Exception):
    pass
```

### Error Handling Example

```python
from src.gitlab_client import GitLabClient
from src.config import GitLabConfig

try:
    config = GitLabConfig.from_config()
    client = GitLabClient(config)
    user_id = client.get_current_user_id()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Type Hints

All functions and methods include type hints for better IDE support and documentation:

```python
from typing import List, Dict, Any, Optional, Tuple

def get_user_repositories(self, username: str) -> List[Dict[str, Any]]:
    """Get repositories for a GitHub user."""
    pass

def clone_or_pull_repo(
    self, 
    clone_url: str, 
    repo_name: str, 
    output_dir: Optional[str] = None
) -> Tuple[str, str]:
    """Clone or pull a repository."""
    pass
```

## Testing

### Unit Tests

```python
import pytest
from unittest.mock import Mock, patch
from src.gitlab_client import GitLabClient
from src.config import GitLabConfig

def test_gitlab_client_creation():
    config = GitLabConfig(url="https://gitlab.com", private_token="test")
    client = GitLabClient(config)
    assert client.config == config

@patch('requests.get')
def test_get_current_user_id(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 123}
    mock_get.return_value = mock_response
    
    config = GitLabConfig(url="https://gitlab.com", private_token="test")
    client = GitLabClient(config)
    user_id = client.get_current_user_id()
    
    assert user_id == 123
```

### Integration Tests

```python
import pytest
from src.services import UserRepositoryService
from src.config import GitLabConfig, RepositoryConfig

@pytest.mark.integration
def test_user_repository_service_integration():
    gitlab_config = GitLabConfig.from_config()
    repo_config = RepositoryConfig.from_config()
    
    service = UserRepositoryService(gitlab_config, repo_config)
    service.clone_user_repositories("/tmp/test-repos")
```

## Performance Considerations

### Concurrent Operations

The tool uses `concurrent.futures.ThreadPoolExecutor` for concurrent operations:

```python
import concurrent.futures

def process_projects_concurrently(projects, max_workers=5):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_project, project): project for project in projects}
        for future in concurrent.futures.as_completed(futures):
            project = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                print(f"Project {project} generated an exception: {exc}")
```

### Memory Management

For large repositories, consider using generators and streaming:

```python
def get_projects_generator(client, user_id):
    """Generator for large project lists."""
    page = 1
    while True:
        projects = client.get_user_projects(user_id, page=page)
        if not projects:
            break
        for project in projects:
            yield project
        page += 1
```

## Security Considerations

### Token Management

```python
import os
from src.config import GitLabConfig

# Use environment variables for sensitive data
token = os.getenv('GITLAB_TOKEN')
if not token:
    raise ValueError("GITLAB_TOKEN environment variable not set")

config = GitLabConfig(url="https://gitlab.com", private_token=token)
```

### SSL Verification

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_secure_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session
``` 