# Development Guide

This guide covers how to contribute to Git Repository Manager development, set up the development environment, and understand the codebase architecture.

## Development Environment Setup

### Prerequisites

1. **Python 3.10+**
   ```bash
   # Check Python version
   python --version
   
   # Install Python 3.10+ if needed
   # Ubuntu/Debian
   sudo apt install python3.10 python3.10-venv python3.10-dev
   
   # macOS
   brew install python@3.10
   
   # Windows
   # Download from python.org
   ```

2. **Git**
   ```bash
   # Install Git
   # Ubuntu/Debian
   sudo apt install git
   
   # macOS
   brew install git
   
   # Windows
   # Download from git-scm.com
   ```

3. **Development Tools**
   ```bash
   # Install development dependencies
   pip install -e ".[dev]"
   ```

### Setting Up the Development Environment

1. **Clone the Repository**
   ```bash
   git clone https://github.com/turahe/git-repo-manager.git
   cd git-repo-manager
   ```

2. **Create Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   # Install in development mode
   pip install -e ".[dev]"
   
   # Or install all dependencies
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Verify Installation**
   ```bash
   # Check if tool works
   git-repo-manager --version
   
   # Run tests
   python run_tests.py
   ```

## Project Structure

```
git-repo-manager/
├── src/                          # Source code
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── gitlab_client.py          # GitLab API client
│   ├── github_client.py          # GitHub API client
│   ├── repository_manager.py     # Repository operations
│   ├── composer_manager.py       # Composer dependency management
│   └── services.py               # High-level service orchestration
├── tests/                        # Test files
│   ├── __init__.py
│   ├── test_cli.py              # CLI tests
│   ├── test_config.py           # Configuration tests
│   ├── test_gitlab_client.py    # GitLab client tests
│   ├── test_github_client.py    # GitHub client tests
│   ├── test_services.py         # Service tests
│   └── test_integration.py      # Integration tests
├── docs/                         # Documentation
├── build_scripts/                # Build and packaging scripts
├── .github/                      # GitHub Actions workflows
├── cli.py                        # CLI entry point
├── pyproject.toml               # Project configuration
├── requirements.txt              # Dependencies
├── setup.py                     # Setup script
├── Makefile                     # Build automation
└── README.md                    # Project documentation
```

## Code Architecture

### Design Principles

1. **Modularity**: Each module has a single responsibility
2. **Testability**: All code is designed for easy testing
3. **Configuration**: Externalized configuration management
4. **Error Handling**: Comprehensive error handling and logging
5. **Type Safety**: Full type hints for better IDE support

### Core Modules

#### Configuration (`src/config.py`)

Handles all configuration management with support for:
- YAML configuration files
- Environment variable overrides
- Default configuration values
- Configuration validation

```python
# Example usage
from src.config import GitLabConfig, RepositoryConfig

gitlab_config = GitLabConfig.from_config()
repo_config = RepositoryConfig.from_config()
```

#### GitLab Client (`src/gitlab_client.py`)

Provides GitLab API integration:
- Authentication handling
- Project listing and filtering
- Group operations
- Error handling and retries

```python
# Example usage
from src.gitlab_client import GitLabClient
from src.config import GitLabConfig

config = GitLabConfig.from_config()
client = GitLabClient(config)

user_id = client.get_current_user_id()
projects = client.get_user_owned_projects(user_id)
```

#### GitHub Client (`src/github_client.py`)

Provides GitHub API integration:
- Authentication handling
- Repository listing
- Organization operations
- Pagination support

```python
# Example usage
from src.github_client import GitHubClient
from src.config import GitHubConfig

config = GitHubConfig.from_config()
client = GitHubClient(config)

repos = client.get_user_repositories("username")
```

#### Repository Manager (`src/repository_manager.py`)

Handles Git operations:
- Repository cloning and pulling
- Concurrent operations
- Progress tracking
- Error handling

```python
# Example usage
from src.repository_manager import RepositoryManager
from src.config import RepositoryConfig

config = RepositoryConfig.from_config()
manager = RepositoryManager(config)

repo_name, status = manager.clone_or_pull_repo(
    "https://github.com/user/repo.git",
    "user/repo"
)
```

#### Composer Manager (`src/composer_manager.py`)

Manages Composer dependency operations:
- Finding composer.json files
- Updating dependencies
- Backup and restore
- Validation

```python
# Example usage
from src.composer_manager import ComposerManager

manager = ComposerManager()
manager.find_and_update_composer("/path/to/repositories")
```

#### Services (`src/services.py`)

High-level service orchestration:
- User repository service
- Group repository service
- GitHub user service
- GitHub organization service
- Composer service

```python
# Example usage
from src.services import UserRepositoryService
from src.config import GitLabConfig, RepositoryConfig

gitlab_config = GitLabConfig.from_config()
repo_config = RepositoryConfig.from_config()

service = UserRepositoryService(gitlab_config, repo_config)
service.clone_user_repositories("/path/to/output")
```

## Testing

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test categories
pytest tests/ -v --tb=short

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run integration tests only
pytest tests/ -m integration -v

# Run unit tests only
pytest tests/ -v -m "not integration"
```

### Test Structure

```
tests/
├── test_cli.py              # CLI command tests
├── test_config.py           # Configuration tests
├── test_gitlab_client.py    # GitLab client tests
├── test_github_client.py    # GitHub client tests
├── test_services.py         # Service tests
├── test_integration.py      # Integration tests
└── conftest.py             # Test configuration
```

### Writing Tests

#### Unit Tests

```python
import pytest
from unittest.mock import Mock, patch
from src.gitlab_client import GitLabClient
from src.config import GitLabConfig

def test_gitlab_client_creation():
    """Test GitLab client creation."""
    config = GitLabConfig(url="https://gitlab.com", private_token="test")
    client = GitLabClient(config)
    assert client.config == config

@patch('requests.get')
def test_get_current_user_id(mock_get):
    """Test getting current user ID."""
    mock_response = Mock()
    mock_response.json.return_value = {"id": 123}
    mock_get.return_value = mock_response
    
    config = GitLabConfig(url="https://gitlab.com", private_token="test")
    client = GitLabClient(config)
    user_id = client.get_current_user_id()
    
    assert user_id == 123
```

#### Integration Tests

```python
import pytest
from src.services import UserRepositoryService
from src.config import GitLabConfig, RepositoryConfig

@pytest.mark.integration
def test_user_repository_service_integration():
    """Test user repository service integration."""
    gitlab_config = GitLabConfig.from_config()
    repo_config = RepositoryConfig.from_config()
    
    service = UserRepositoryService(gitlab_config, repo_config)
    service.clone_user_repositories("/tmp/test-repos")
```

### Test Configuration

```python
# conftest.py
import pytest
import tempfile
import os

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir

@pytest.fixture
def mock_config():
    """Mock configuration for tests."""
    return {
        'gitlab': {
            'url': 'https://gitlab.com',
            'private_token': 'test-token'
        },
        'repository': {
            'repo_dir': '/tmp/test',
            'max_concurrent_downloads': 5
        }
    }
```

## Code Style and Standards

### Python Style Guide

Follow PEP 8 with these additions:

```python
# Type hints for all functions
def get_user_repositories(self, username: str) -> List[Dict[str, Any]]:
    """Get repositories for a GitHub user."""
    pass

# Docstrings for all classes and methods
class GitLabClient:
    """Client for interacting with GitLab API."""
    
    def get_current_user_id(self) -> int:
        """Get authenticated user's ID."""
        pass

# Error handling with specific exceptions
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    raise NetworkError(f"Failed to connect to {url}: {e}")
```

### Linting and Formatting

```bash
# Run linting
flake8 src/ tests/

# Run type checking
mypy src/

# Run security checks
bandit src/
safety check

# Auto-format code
black src/ tests/
isort src/ tests/
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## Building and Packaging

### Development Build

```bash
# Install in development mode
pip install -e .

# Build package
python setup.py build

# Create source distribution
python setup.py sdist

# Create wheel
python setup.py bdist_wheel
```

### Production Build

```bash
# Build all packages
python build_scripts/build_all.py

# Build specific platform
python build_scripts/build_exe.py      # Windows
python build_scripts/build_deb.py      # Debian
python build_scripts/build_rpm.py      # RPM
```

### Docker Build

```dockerfile
# Dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    composer \
    && rm -rf /var/lib/apt/lists/*

# Copy source code
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Install the tool
RUN pip install -e .

# Set entry point
ENTRYPOINT ["git-repo-manager"]
```

## Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12, 3.13]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8 mypy
    
    - name: Lint with flake8
      run: flake8 src/ tests/
    
    - name: Type check with mypy
      run: mypy src/
    
    - name: Test with pytest
      run: pytest tests/ --cov=src --cov-report=xml
```

## Contributing

### Development Workflow

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone
   git clone https://github.com/your-username/git-repo-manager.git
   cd git-repo-manager
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   ```bash
   # Make your changes
   # Write tests for new functionality
   # Update documentation
   ```

4. **Run Tests**
   ```bash
   # Run all tests
   python run_tests.py
   
   # Run specific tests
   pytest tests/test_your_feature.py -v
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add feature: description of changes"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   # Create PR on GitHub
   ```

### Code Review Guidelines

1. **Code Quality**
   - Follow PEP 8 style guide
   - Include type hints
   - Write comprehensive docstrings
   - Handle errors appropriately

2. **Testing**
   - Write unit tests for new functionality
   - Include integration tests for complex features
   - Maintain good test coverage

3. **Documentation**
   - Update relevant documentation
   - Add examples for new features
   - Update API documentation

4. **Security**
   - Don't commit sensitive data
   - Use environment variables for secrets
   - Follow security best practices

### Issue Reporting

When reporting issues, include:

1. **Environment Information**
   ```bash
   # System information
   uname -a
   python --version
   git --version
   ```

2. **Tool Information**
   ```bash
   git-repo-manager --version
   git-repo-manager config-info --mask-sensitive
   ```

3. **Error Details**
   - Complete error message
   - Steps to reproduce
   - Expected vs actual behavior

4. **Logs**
   ```bash
   # Enable debug logging
   export LOG_LEVEL="DEBUG"
   git-repo-manager clone-user --verbose
   ```

## Performance Optimization

### Profiling

```python
import cProfile
import pstats

# Profile specific function
def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    service.clone_user_repositories()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

### Memory Optimization

```python
# Use generators for large datasets
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

### Concurrent Operations

```python
import concurrent.futures

def process_projects_concurrently(projects, max_workers=5):
    """Process projects concurrently."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_project, project): project for project in projects}
        for future in concurrent.futures.as_completed(futures):
            project = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                print(f"Project {project} generated an exception: {exc}")
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

### Input Validation

```python
import re
from typing import Optional

def validate_username(username: str) -> bool:
    """Validate GitHub username format."""
    if not username:
        return False
    
    # GitHub username rules
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'
    return bool(re.match(pattern, username))

def sanitize_url(url: str) -> Optional[str]:
    """Sanitize and validate URL."""
    if not url:
        return None
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        return None
    
    return url
```

### SSL Verification

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_secure_session():
    """Create secure HTTP session with retry logic."""
    session = requests.Session()
    
    # Configure retry strategy
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

## Release Process

### Version Management

```python
# Version in pyproject.toml
[project]
name = "git-repo-manager"
version = "1.0.0"
```

### Release Checklist

1. **Update Version**
   ```bash
   # Update version in pyproject.toml
   # Update CHANGELOG.md
   # Update documentation
   ```

2. **Run Full Test Suite**
   ```bash
   python run_tests.py
   pytest tests/ --cov=src
   ```

3. **Build Packages**
   ```bash
   python build_scripts/build_all.py
   ```

4. **Create Release**
   ```bash
   # Create git tag
   git tag v1.0.0
   git push origin v1.0.0
   
   # Create GitHub release
   # Upload built packages
   ```

5. **Publish to PyPI**
   ```bash
   # Build distribution
   python setup.py sdist bdist_wheel
   
   # Upload to PyPI
   twine upload dist/*
   ```

This development guide provides comprehensive information for contributing to the Git Repository Manager project. Follow these guidelines to ensure high-quality contributions and maintain code consistency across the project. 