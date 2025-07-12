# Usage Guide

This guide covers how to use Git Repository Manager for various repository management tasks.

## Quick Start

### 1. Initialize Configuration

```bash
# Interactive configuration setup
git-repo-manager init-config
```

### 2. Clone Your Repositories

```bash
# Clone your GitLab repositories
git-repo-manager clone-user

# Clone GitHub repositories
git-repo-manager clone-github-user
```

### 3. Update Dependencies

```bash
# Update Composer dependencies
git-repo-manager update-composer /path/to/repositories
```

## GitLab Operations

### Clone User Repositories

Clone all repositories owned by the authenticated user:

```bash
# Basic usage
git-repo-manager clone-user

# With custom output directory
git-repo-manager clone-user --output-dir /path/to/repos

# With specific configuration
git-repo-manager clone-user --config /path/to/config.yml
```

### Clone Group Repositories

Clone repositories from specific GitLab groups:

```bash
# Clone from configured groups
git-repo-manager clone-groups

# Clone from specific group
git-repo-manager clone-groups --group-id 123

# With custom output directory
git-repo-manager clone-groups --output-dir /path/to/repos
```

### Advanced GitLab Operations

```bash
# Clone with specific settings
git-repo-manager clone-user \
  --output-dir /path/to/repos \
  --max-concurrent 10 \
  --exclude-pattern "deprecated-*"

# Clone only specific repositories
git-repo-manager clone-user \
  --include-pattern "project-*" \
  --output-dir /path/to/repos
```

## GitHub Operations

### Clone User Repositories

```bash
# Clone repositories from specific user
git-repo-manager clone-github-user --username john-doe

# Clone authenticated user's repositories
git-repo-manager clone-github-user

# With custom output directory
git-repo-manager clone-github-user --username john-doe --output-dir /path/to/repos
```

### Clone Organization Repositories

```bash
# Clone organization repositories
git-repo-manager clone-github-org --org-name my-organization

# With custom output directory
git-repo-manager clone-github-org --org-name my-organization --output-dir /path/to/repos
```

### Advanced GitHub Operations

```bash
# Clone with filtering
git-repo-manager clone-github-user --username john-doe \
  --include-pattern "web-*" \
  --exclude-pattern "deprecated-*" \
  --output-dir /path/to/repos

# Clone organization with specific settings
git-repo-manager clone-github-org --org-name my-org \
  --include-pattern "api-*" \
  --output-dir /path/to/repos
```

## Composer Operations

### Update Dependencies

```bash
# Update Composer dependencies in specific directory
git-repo-manager update-composer /path/to/repositories

# Update with backup
git-repo-manager update-composer /path/to/repositories --backup

# Update with specific strategy
git-repo-manager update-composer /path/to/repositories --strategy interactive
```

### Advanced Composer Operations

```bash
# Update with exclusions
git-repo-manager update-composer /path/to/repositories \
  --exclude-packages "vendor/package1" \
  --exclude-packages "vendor/package2"

# Update with backup and logging
git-repo-manager update-composer /path/to/repositories \
  --backup \
  --log-file /path/to/composer.log
```

## Configuration Management

### Initialize Configuration

```bash
# Interactive setup
git-repo-manager init-config

# Non-interactive setup
git-repo-manager init-config --non-interactive \
  --gitlab-url "https://gitlab.com" \
  --gitlab-token "your-token" \
  --github-token "your-token"
```

### Validate Configuration

```bash
# Validate current configuration
git-repo-manager validate-config

# Validate specific file
git-repo-manager validate-config --config /path/to/config.yml
```

### Show Configuration Info

```bash
# Show current configuration
git-repo-manager config-info

# Show with sensitive data masked
git-repo-manager config-info --mask-sensitive

# Show in JSON format
git-repo-manager config-info --format json
```

## Combined Operations

### Clone and Update

```bash
# Clone repositories and update dependencies
git-repo-manager clone-user --update-composer

# Clone with specific settings and update
git-repo-manager clone-github-user --username john-doe \
  --output-dir /path/to/repos \
  --update-composer \
  --backup
```

### Batch Operations

```bash
# Clone from multiple sources
git-repo-manager clone-user --output-dir /path/to/gitlab-repos
git-repo-manager clone-github-user --username john-doe --output-dir /path/to/github-repos

# Update all repositories
git-repo-manager update-composer /path/to/gitlab-repos
git-repo-manager update-composer /path/to/github-repos
```

## Output and Logging

### Verbose Output

```bash
# Enable verbose logging
git-repo-manager clone-user --verbose

# Show detailed progress
git-repo-manager clone-user --progress
```

### Logging Options

```bash
# Log to file
git-repo-manager clone-user --log-file /path/to/log.txt

# Set log level
git-repo-manager clone-user --log-level DEBUG

# JSON output
git-repo-manager clone-user --output-format json
```

## Error Handling

### Retry Failed Operations

```bash
# Retry failed clones
git-repo-manager clone-user --retry-failed

# Retry with specific attempts
git-repo-manager clone-user --retry-attempts 3
```

### Skip Errors

```bash
# Continue on errors
git-repo-manager clone-user --continue-on-error

# Skip specific error types
git-repo-manager clone-user --skip-errors "404,403"
```

## Performance Optimization

### Concurrent Operations

```bash
# Increase concurrent downloads
git-repo-manager clone-user --max-concurrent 10

# Limit concurrent operations
git-repo-manager clone-user --max-concurrent 2
```

### Network Optimization

```bash
# Use shallow clones
git-repo-manager clone-user --shallow

# Set timeout
git-repo-manager clone-user --timeout 60

# Use specific Git protocol
git-repo-manager clone-user --git-protocol https
```

## Examples

### Development Setup

```bash
# Setup for development
git-repo-manager init-config
git-repo-manager clone-user --output-dir ./repos
git-repo-manager update-composer ./repos
```

### Production Deployment

```bash
# Production setup
git-repo-manager clone-groups \
  --output-dir /var/repositories \
  --max-concurrent 5 \
  --backup

git-repo-manager update-composer /var/repositories \
  --strategy auto \
  --backup
```

### CI/CD Pipeline

```bash
# In CI/CD pipeline
git-repo-manager clone-github-org --org-name my-org \
  --output-dir $CI_PROJECT_DIR/repos \
  --max-concurrent 3

git-repo-manager update-composer $CI_PROJECT_DIR/repos \
  --strategy auto
```

## Command Reference

### Global Options

```bash
git-repo-manager [OPTIONS] COMMAND [ARGS]...

Options:
  --config PATH          Configuration file path
  --verbose             Enable verbose output
  --log-level LEVEL     Set logging level (DEBUG, INFO, WARNING, ERROR)
  --log-file PATH       Log file path
  --output-format FORMAT Output format (text, json, yaml)
  --help                Show help message
  --version             Show version information
```

### Common Commands

```bash
Commands:
  init-config           Initialize configuration
  validate-config      Validate configuration
  config-info          Show configuration information
  clone-user           Clone user repositories (GitLab)
  clone-groups         Clone group repositories (GitLab)
  clone-github-user    Clone user repositories (GitHub)
  clone-github-org     Clone organization repositories (GitHub)
  update-composer      Update Composer dependencies
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```bash
   # Check token validity
   git-repo-manager config-info --mask-sensitive
   
   # Reinitialize configuration
   git-repo-manager init-config
   ```

2. **Network Issues**
   ```bash
   # Test connectivity
   curl -H "Authorization: Bearer YOUR_TOKEN" https://gitlab.com/api/v4/user
   
   # Use different timeout
   git-repo-manager clone-user --timeout 120
   ```

3. **Permission Issues**
   ```bash
   # Check file permissions
   ls -la config.yml
   
   # Fix permissions
   chmod 600 config.yml
   ```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL="DEBUG"

# Run with debug output
git-repo-manager clone-user --verbose --log-level DEBUG
```

## Next Steps

After learning basic usage:

1. **Explore advanced features**: See [Examples](examples.md)
2. **Set up automation**: See [Development Guide](development.md)
3. **Troubleshoot issues**: See [Troubleshooting](troubleshooting.md) 