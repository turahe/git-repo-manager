[![Build Status](https://github.com/turahe/git-repo-manager/actions/workflows/test.yml/badge.svg)](https://github.com/turahe/git-repo-manager/actions/workflows/test.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://turahe.github.io/git-repo-manager/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/turahe/git-repo-manager)](LICENSE)
[![Coverage Status](https://img.shields.io/codecov/c/github/turahe/git-repo-manager?logo=codecov)](https://codecov.io/gh/turahe/git-repo-manager)

# GitLab & GitHub Repository Management Tool

A modular, object-oriented CLI tool for managing GitLab and GitHub repositories and Composer dependencies using Click.

## Features

- **Multi-Platform Support**: Manage repositories from both GitLab and GitHub
- **Modular Architecture**: Clean separation of concerns with dedicated classes for different operations
- **Object-Oriented Design**: Well-structured classes for configuration, API clients, repository management, and Composer operations
- **CLI Interface**: Easy-to-use command-line interface powered by Click
- **Concurrent Operations**: Parallel processing for faster repository cloning
- **Flexible Configuration**: Support for environment variables and command-line options
- **Composer Integration**: Automatic dependency updates for PHP projects

## Installation

1. Clone this repository or download the files
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the application by editing `config.yml` (see Configuration section below)

## Usage

### Basic Commands

```bash
# Show help
python cli.py --help

# Clone user repositories
python cli.py clone-user

# Clone group repositories
python cli.py clone-groups

# Clone GitHub user repositories
python cli.py clone-github-user

# Clone GitHub organization repositories
python cli.py clone-github-org organization-name

# Update Composer dependencies
python cli.py update-composer

# Clone all repositories and update Composer dependencies
python cli.py clone-all --update-composer

# Clone to custom output directory
python cli.py clone-user --output-dir /path/to/custom/directory
python cli.py clone-groups --output-dir /path/to/custom/directory
python cli.py clone-github-user --output-dir /path/to/custom/directory

# Initialize configuration (interactive)
python cli.py init-config

# Initialize configuration (non-interactive)
python cli.py init-config --non-interactive

# Show configuration information
python cli.py config-info

# Validate configuration
python cli.py validate-config

### Advanced Usage

```bash
# Clone user repositories with custom settings
python cli.py clone-user \
  --gitlab-url https://gitlab.company.com \
  --token your-token \
  --repo-dir /path/to/repos \
  --max-workers 10

# Clone specific groups
python cli.py clone-groups \
  --group-ids 123456 789012 \
  --repo-dir /path/to/repos

# Clone GitHub user repositories
python cli.py clone-github-user \
  --username username \
  --repo-dir /path/to/repos \
  --max-workers 10

# Clone GitHub organization repositories
python cli.py clone-github-org organization-name \
  --repo-dir /path/to/repos \
  --max-workers 10

# Clone to custom output directory
python cli.py clone-user \
  --output-dir /custom/path \
  --max-workers 10

python cli.py clone-groups \
  --output-dir /custom/path \
  --group-ids 123456 789012

# Update Composer dependencies in specific directory
python cli.py update-composer --directory /path/to/projects

## Configuration

The application uses a YAML configuration file for settings. The tool looks for configuration in this order:
1. Current directory (`config.yml`)
2. User home directory (`~/.git-repo-manager/config.yml`)
3. Default fallback

Environment variables can override these settings.

### Output Directory Management

The tool supports flexible output directory management:

- **Default Directory**: Uses the `repo_dir` setting from configuration
- **Custom Output Directory**: Use `--output-dir` to specify a custom directory for each clone operation
- **Directory Override**: Use `--repo-dir` to override the configured repository directory

**Examples:**
```bash
# Use default directory from config
python cli.py clone-user

# Use custom output directory
python cli.py clone-user --output-dir /path/to/custom/directory

# Override configured repository directory
python cli.py clone-user --repo-dir /path/to/repos

# Combine with other options
python cli.py clone-groups \
  --output-dir /custom/path \
  --group-ids 123456 789012 \
  --max-workers 10
```

The `--output-dir` option takes precedence over the configured `repo_dir` and allows you to organize repositories in different directory structures for different operations.

### Configuration File

You can create a configuration file using the `init-config` command:

```bash
# Interactive configuration setup
python cli.py init-config

# Non-interactive setup (uses defaults)
python cli.py init-config --non-interactive
```

The interactive mode will prompt you for:
- GitLab URL and Personal Access Token
- GitHub URL and Personal Access Token (optional)
- Repository directory
- Maximum concurrent downloads
- Group IDs to clone from
- Composer settings

This will create `~/.git-repo-manager/config.yml` with your settings:

```yaml
gitlab:
  url: "https://gitlab.com"
  private_token: "your-gitlab-token"

github:
  url: "https://api.github.com"
  access_token: "your-github-token"  # Optional

repository:
  repo_dir: "~/gitlab-repos"  # Default repository directory
  max_concurrent_downloads: 5

groups:
  target_group_ids:
    - 2969050   # circlecreative
    - 60830364  # circle-creative-flutter
    # Add your group IDs here

composer:
  enabled: true
  auto_update: false  # Whether to automatically update after cloning
```

### Environment Variables

Environment variables can override configuration file settings:

```bash
export GITLAB_PRIVATE_TOKEN="your-gitlab-token"
export GITLAB_URL="https://gitlab.company.com"
export GITHUB_ACCESS_TOKEN="your-github-token"
export GITHUB_URL="https://api.github.com"
export REPO_DIR="/path/to/repositories"
export MAX_CONCURRENT_DOWNLOADS="10"
```

## Project Structure

```
├── cli.py                 # Main CLI application
├── config.yml             # Configuration file
├── requirements.txt       # Python dependencies
├── setup.py              # Installation script
├── README.md             # This file
├── src/                  # Source code package
│   ├── __init__.py
│   ├── config.py         # Configuration classes
│   ├── gitlab_client.py  # GitLab API client
│   ├── github_client.py  # GitHub API client
│   ├── repository_manager.py  # Git operations
│   ├── composer_manager.py    # Composer operations
│   └── services.py       # Service orchestration
├── clone.py              # Original user repository script
├── clone-group.py        # Original group repository script
├── composer_updater.py   # Original Composer script
├── test_github.py        # GitHub functionality test script
└── test_output_dir.py    # Output directory feature test script
```

## Architecture

### Configuration (`src/config.py`)
- `GitLabConfig`: GitLab API configuration
- `RepositoryConfig`: Repository operations configuration
- `GroupConfig`: Group-specific configuration

### GitLab Client (`src/gitlab_client.py`)
- `GitLabClient`: Handles all GitLab API interactions
- Methods for fetching user and group projects

### GitHub Client (`src/github_client.py`)
- `GitHubClient`: Handles all GitHub API interactions
- Methods for fetching user and organization repositories

### Repository Manager (`src/repository_manager.py`)
- `RepositoryManager`: Manages Git operations
- Concurrent cloning and updating of repositories
- Branch management for group repositories

### Composer Manager (`src/composer_manager.py`)
- `ComposerManager`: Handles Composer operations
- Automatic detection of composer commands
- Recursive dependency updates

### Services (`src/services.py`)
- `UserRepositoryService`: Orchestrates GitLab user repository operations
- `GroupRepositoryService`: Orchestrates GitLab group repository operations
- `GitHubUserService`: Orchestrates GitHub user repository operations
- `GitHubOrganizationService`: Orchestrates GitHub organization repository operations
- `ComposerService`: Orchestrates Composer operations

## Configuration

### GitLab Token

You need a GitLab Personal Access Token with appropriate permissions:
- `read_api` for reading project information
- `read_repository` for cloning repositories

### GitHub Token

You need a GitHub Personal Access Token with appropriate permissions:
- `repo` for accessing private repositories
- `public_repo` for accessing public repositories only

### Group IDs

The tool reads group IDs from `config.yml`. You can:
1. Modify the `config.yml` file directly to add/remove group IDs
2. Use command-line options to override group IDs: `--group-ids 123456 789012`
3. Set environment variables to override settings

## Error Handling

The tool includes comprehensive error handling for:
- Network connectivity issues
- Authentication failures
- Git command errors
- Composer command errors
- File system operations

## Performance

- **Concurrent Downloads**: Configurable number of parallel workers (default: 5)
- **Efficient API Usage**: Proper pagination handling for large project lists
- **Smart Repository Management**: Only clones new repositories, updates existing ones

## GitHub Integration

This tool now supports both GitLab and GitHub repositories. The GitHub integration provides:

### Features
- **User Repositories**: Clone all repositories from a specific GitHub user
- **Organization Repositories**: Clone all repositories from a GitHub organization
- **Authenticated Access**: Use your GitHub token to access private repositories
- **Concurrent Cloning**: Parallel processing for faster downloads
- **Smart Updates**: Only clones new repositories, updates existing ones

### Setup
1. Create a GitHub Personal Access Token with `repo` permissions
2. Configure the token in your `config.yml` or set `GITHUB_ACCESS_TOKEN` environment variable
3. Use the GitHub commands to clone repositories

### Commands
```bash
# Clone repositories from a GitHub user
python cli.py clone-github-user --username username

# Clone repositories from authenticated user
python cli.py clone-github-user

# Clone repositories from a GitHub organization
python cli.py clone-github-org organization-name
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Run linting
make lint

# Run type checking
make type-check

# Generate coverage report
make coverage

# Or use the test runner script
python run_tests.py
```

### Testing

The project includes comprehensive unit tests for all components:

- **Configuration Tests**: Test all configuration classes and managers
- **GitLab Client Tests**: Test GitLab API interactions
- **GitHub Client Tests**: Test GitHub API interactions  
- **Service Tests**: Test service orchestration classes
- **CLI Tests**: Test command-line interface commands

Run tests with:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_config.py

# Run specific test class
pytest tests/test_config.py::TestGitLabConfig
```

## CI/CD

This project uses GitHub Actions for continuous integration and deployment:

### Workflows

- **Test**: Runs on every push and PR
  - Python 3.8-3.11 compatibility
  - Linting with flake8
  - Type checking with mypy
  - Unit tests with pytest
  - Code coverage reporting

- **Build**: Creates packages for all platforms
  - Windows EXE (PyInstaller)
  - DEB package (Debian/Ubuntu)
  - RPM package (Red Hat/CentOS/Fedora)

- **Security**: Weekly security scanning
  - Safety (vulnerability scanner)
  - Bandit (security linter)
  - Results uploaded to GitHub Code Scanning

- **Documentation**: Generates and validates docs
  - API documentation
  - Link validation
  - Documentation artifacts

- **Release**: Automated releases
  - Triggers on tag creation
  - Builds all package types
  - Uploads to GitHub Releases

## License

This project is open source and available under the MIT License. 