# Installation Guide

This guide covers how to install Git Repository Manager on different platforms and environments.

## Prerequisites

### System Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux
- **Git**: For repository operations
- **Composer**: For PHP dependency management (optional)

### Python Installation

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

#### macOS
```bash
# Using Homebrew
brew install python@3.10

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3-pip
```

## Installation Methods

### Method 1: Using pip (Recommended)

```bash
# Install from PyPI
pip install git-repo-manager

# Or install with development dependencies
pip install git-repo-manager[dev]
```

### Method 2: From Source

```bash
# Clone the repository
git clone https://github.com/turahe/git-repo-manager.git
cd git-repo-manager

# Install in development mode
pip install -e .

# Or install with all dependencies
pip install -e ".[dev]"
```

### Method 3: Using pipx (Isolated Environment)

```bash
# Install pipx if not already installed
pip install pipx

# Install the tool
pipx install git-repo-manager
```

## Verification

After installation, verify the installation:

```bash
# Check if the command is available
git-repo-manager --help

# Check version
git-repo-manager --version
```

## Dependencies

### Core Dependencies

The tool automatically installs these dependencies:

- **click**: CLI framework
- **requests**: HTTP library for API calls
- **pyyaml**: YAML configuration parsing
- **pyinstaller**: For building executables (optional)

### Optional Dependencies

For development and testing:

```bash
pip install -r requirements.txt
```

Development dependencies include:
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **flake8**: Code linting
- **mypy**: Type checking
- **safety**: Security scanning
- **bandit**: Security linting

## Platform-Specific Notes

### Windows

1. **PowerShell Execution Policy**: If you encounter execution policy issues:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Git Installation**: Ensure Git is installed and available in PATH
   - Download from [git-scm.com](https://git-scm.com/download/win)

### macOS

1. **Xcode Command Line Tools**: Install if not already present:
   ```bash
   xcode-select --install
   ```

2. **Homebrew**: Recommended for managing dependencies:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

### Linux

1. **System Dependencies**: Install required system packages:
   ```bash
   # Ubuntu/Debian
   sudo apt install git composer
   
   # CentOS/RHEL
   sudo yum install git composer
   ```

## Docker Installation

For containerized environments:

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    composer \
    && rm -rf /var/lib/apt/lists/*

# Install the tool
RUN pip install git-repo-manager

# Set working directory
WORKDIR /workspace

# Run the tool
ENTRYPOINT ["git-repo-manager"]
```

## Troubleshooting

### Common Issues

1. **"git-repo-manager: command not found"**
   - Ensure Python scripts directory is in PATH
   - Try: `python -m git_repo_manager`

2. **Permission Denied**
   - Use `pip install --user` for user installation
   - Or create a virtual environment

3. **Import Errors**
   - Check Python version: `python --version`
   - Reinstall dependencies: `pip install -r requirements.txt`

### Virtual Environment

For isolated installation:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install the tool
pip install git-repo-manager
```

## Next Steps

After installation:

1. **Configure the tool**: See [Configuration Guide](configuration.md)
2. **Learn basic usage**: See [Usage Guide](usage.md)
3. **Explore examples**: See [Examples](examples.md)

## Support

If you encounter installation issues:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Search existing [GitHub Issues](https://github.com/turahe/git-repo-manager/issues)
3. Create a new issue with detailed information about your environment 