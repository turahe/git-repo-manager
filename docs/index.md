# Git Repository Manager Documentation

## Overview

Git Repository Manager is a powerful, modular CLI tool designed for managing GitLab and GitHub repositories and Composer dependencies. Built with Python 3.10+, it provides a comprehensive solution for repository management, dependency updates, and automated workflows.

## Quick Navigation

- [Installation Guide](installation.md)
- [Configuration Guide](configuration.md)
- [Usage Guide](usage.md)
- [API Reference](api.md)
- [CLI Reference](cli.md)
- [Examples](examples.md)
- [Troubleshooting](troubleshooting.md)
- [Development Guide](development.md)

## Key Features

### 🔄 Repository Management
- **GitLab Integration**: Clone user-owned and group repositories
- **GitHub Integration**: Clone user and organization repositories
- **Concurrent Operations**: Multi-threaded repository cloning and updates
- **Custom Output Directories**: Flexible repository storage locations

### 🛠️ Dependency Management
- **Composer Support**: Automatic Composer dependency updates
- **Batch Processing**: Update multiple repositories simultaneously
- **Configurable Settings**: Customizable update strategies

### ⚙️ Configuration Management
- **YAML Configuration**: Human-readable configuration files
- **Environment Variables**: Secure credential management
- **Interactive Setup**: Guided configuration wizard
- **Validation**: Built-in configuration validation

### 🚀 Advanced Features
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Python 3.10+ Support**: Modern Python compatibility
- **Comprehensive Testing**: Unit, integration, and CLI tests
- **CI/CD Ready**: GitHub Actions workflows included

## System Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: See [Installation Guide](installation.md)

## Quick Start

1. **Install the tool**:
   ```bash
   pip install git-repo-manager
   ```

2. **Initialize configuration**:
   ```bash
   git-repo-manager init-config
   ```

3. **Clone repositories**:
   ```bash
   # Clone your GitLab repositories
   git-repo-manager clone-user
   
   # Clone GitHub repositories
   git-repo-manager clone-github-user
   ```

## Architecture

The tool is built with a modular, object-oriented design:

```
src/
├── config.py              # Configuration management
├── gitlab_client.py       # GitLab API client
├── github_client.py       # GitHub API client
├── repository_manager.py   # Repository operations
├── composer_manager.py     # Composer dependency management
└── services.py            # High-level service orchestration
```

## Contributing

We welcome contributions! See our [Development Guide](development.md) for details on:
- Setting up the development environment
- Running tests
- Code style guidelines
- Submitting pull requests

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/turahe/git-repo-manager/issues)
- **Documentation**: This documentation site
- **Examples**: See [Examples](examples.md) for common use cases

---

*Last updated: December 2024* 