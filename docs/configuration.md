# Configuration Guide

This guide covers how to configure Git Repository Manager for your specific needs.

## Configuration Overview

The tool uses a hierarchical configuration system with multiple sources:

1. **YAML Configuration File** (Primary)
2. **Environment Variables** (Override YAML)
3. **Command Line Arguments** (Override both)

## Quick Setup

### Interactive Configuration

The easiest way to set up configuration:

```bash
git-repo-manager init-config
```

This will guide you through an interactive setup process.

### Manual Configuration

Create a configuration file manually:

```bash
# Copy example configuration
cp config.example.yml config.yml

# Edit the configuration
nano config.yml
```

## Configuration File Structure

### Basic Configuration

```yaml
# GitLab Configuration
gitlab:
  url: "https://gitlab.com"
  private_token: "your-gitlab-token"

# GitHub Configuration
github:
  url: "https://api.github.com"
  access_token: "your-github-token"

# Repository Settings
repository:
  repo_dir: "/path/to/repositories"
  max_concurrent_downloads: 5

# Group Configuration
groups:
  target_group_ids: [123, 456, 789]

# Composer Settings
composer:
  enabled: true
  auto_update: false
```

### Advanced Configuration

```yaml
# GitLab Configuration
gitlab:
  url: "https://gitlab.company.com"
  private_token: "${GITLAB_TOKEN}"
  timeout: 30
  retry_attempts: 3

# GitHub Configuration
github:
  url: "https://api.github.com"
  access_token: "${GITHUB_TOKEN}"
  timeout: 30
  retry_attempts: 3

# Repository Settings
repository:
  repo_dir: "${HOME}/repositories"
  max_concurrent_downloads: 10
  clone_depth: 1
  fetch_all_branches: false
  exclude_patterns:
    - "*.tmp"
    - "node_modules"

# Group Configuration
groups:
  target_group_ids: [123, 456, 789]
  include_archived: false
  exclude_patterns:
    - "deprecated-*"

# Composer Settings
composer:
  enabled: true
  auto_update: true
  update_strategy: "interactive"
  backup_before_update: true
  exclude_packages:
    - "vendor/package1"
    - "vendor/package2"

# Logging Configuration
logging:
  level: "INFO"
  file: "/var/log/git-repo-manager.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Security Settings
security:
  verify_ssl: true
  allow_insecure: false
  token_encryption: true
```

## Environment Variables

You can override configuration using environment variables:

### GitLab Variables

```bash
export GITLAB_URL="https://gitlab.company.com"
export GITLAB_PRIVATE_TOKEN="your-token"
```

### GitHub Variables

```bash
export GITHUB_URL="https://api.github.com"
export GITHUB_ACCESS_TOKEN="your-token"
```

### Repository Variables

```bash
export REPO_DIR="/path/to/repositories"
export MAX_CONCURRENT_DOWNLOADS="10"
```

### Composer Variables

```bash
export COMPOSER_ENABLED="true"
export COMPOSER_AUTO_UPDATE="false"
```

## Configuration File Locations

The tool looks for configuration files in this order:

1. **Current Directory**: `./config.yml`
2. **User Home**: `~/.git-repo-manager/config.yml`
3. **System-wide**: `/etc/git-repo-manager/config.yml`

## Configuration Validation

### Validate Configuration

```bash
# Validate current configuration
git-repo-manager validate-config

# Validate specific file
git-repo-manager validate-config --config /path/to/config.yml
```

### Configuration Info

```bash
# Show current configuration
git-repo-manager config-info

# Show configuration with sensitive data masked
git-repo-manager config-info --mask-sensitive
```

## Security Best Practices

### Token Management

1. **Use Environment Variables**: Store tokens in environment variables
2. **Restrict File Permissions**: Set proper file permissions on config files
3. **Rotate Tokens Regularly**: Update tokens periodically
4. **Use Least Privilege**: Grant minimal required permissions

### Example Secure Setup

```bash
# Create secure configuration directory
mkdir -p ~/.git-repo-manager
chmod 700 ~/.git-repo-manager

# Create configuration file
cat > ~/.git-repo-manager/config.yml << EOF
gitlab:
  url: "https://gitlab.company.com"
  private_token: "\${GITLAB_TOKEN}"

github:
  url: "https://api.github.com"
  access_token: "\${GITHUB_TOKEN}"

repository:
  repo_dir: "\${HOME}/repositories"
  max_concurrent_downloads: 5
EOF

# Set secure permissions
chmod 600 ~/.git-repo-manager/config.yml

# Set environment variables
export GITLAB_TOKEN="your-gitlab-token"
export GITHUB_TOKEN="your-github-token"
```

## Configuration Examples

### Development Environment

```yaml
gitlab:
  url: "https://gitlab.com"
  private_token: "${GITLAB_TOKEN}"

github:
  url: "https://api.github.com"
  access_token: "${GITHUB_TOKEN}"

repository:
  repo_dir: "./repositories"
  max_concurrent_downloads: 3

composer:
  enabled: true
  auto_update: false
```

### Production Environment

```yaml
gitlab:
  url: "https://gitlab.company.com"
  private_token: "${GITLAB_TOKEN}"
  timeout: 60
  retry_attempts: 5

github:
  url: "https://api.github.com"
  access_token: "${GITHUB_TOKEN}"
  timeout: 60
  retry_attempts: 5

repository:
  repo_dir: "/var/repositories"
  max_concurrent_downloads: 10
  clone_depth: 1

groups:
  target_group_ids: [123, 456, 789]
  include_archived: false

composer:
  enabled: true
  auto_update: true
  backup_before_update: true

logging:
  level: "WARNING"
  file: "/var/log/git-repo-manager.log"
```

### CI/CD Environment

```yaml
gitlab:
  url: "https://gitlab.company.com"
  private_token: "${CI_GITLAB_TOKEN}"

github:
  url: "https://api.github.com"
  access_token: "${CI_GITHUB_TOKEN}"

repository:
  repo_dir: "${CI_PROJECT_DIR}/repositories"
  max_concurrent_downloads: 5

composer:
  enabled: true
  auto_update: true

logging:
  level: "INFO"
  format: "json"
```

## Troubleshooting Configuration

### Common Issues

1. **Configuration Not Found**
   ```bash
   # Check configuration file location
   git-repo-manager config-info
   
   # Create default configuration
   git-repo-manager init-config
   ```

2. **Invalid Configuration**
   ```bash
   # Validate configuration
   git-repo-manager validate-config
   
   # Check YAML syntax
   python -c "import yaml; yaml.safe_load(open('config.yml'))"
   ```

3. **Permission Issues**
   ```bash
   # Check file permissions
   ls -la config.yml
   
   # Fix permissions
   chmod 600 config.yml
   ```

### Debug Configuration

```bash
# Enable debug logging
export LOG_LEVEL="DEBUG"

# Run with verbose output
git-repo-manager --verbose clone-user

# Check configuration loading
git-repo-manager config-info --debug
```

## Next Steps

After configuring the tool:

1. **Test the configuration**: See [Usage Guide](usage.md)
2. **Learn about advanced features**: See [Examples](examples.md)
3. **Set up automation**: See [Development Guide](development.md) 