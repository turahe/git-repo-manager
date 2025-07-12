# CLI Reference

Complete command-line interface reference for Git Repository Manager.

## Overview

```bash
git-repo-manager [OPTIONS] COMMAND [ARGS]...
```

## Global Options

| Option | Type | Description |
|--------|------|-------------|
| `--config PATH` | string | Configuration file path |
| `--verbose` | flag | Enable verbose output |
| `--log-level LEVEL` | string | Set logging level (DEBUG, INFO, WARNING, ERROR) |
| `--log-file PATH` | string | Log file path |
| `--output-format FORMAT` | string | Output format (text, json, yaml) |
| `--help` | flag | Show help message |
| `--version` | flag | Show version information |

## Commands

### Configuration Commands

#### `init-config`

Initialize configuration interactively or non-interactively.

```bash
git-repo-manager init-config [OPTIONS]
```

**Options:**
- `--non-interactive` - Non-interactive mode
- `--gitlab-url URL` - GitLab URL
- `--gitlab-token TOKEN` - GitLab private token
- `--github-token TOKEN` - GitHub access token
- `--repo-dir PATH` - Repository directory
- `--max-concurrent N` - Maximum concurrent downloads

**Examples:**
```bash
# Interactive setup
git-repo-manager init-config

# Non-interactive setup
git-repo-manager init-config --non-interactive \
  --gitlab-url "https://gitlab.com" \
  --gitlab-token "your-token"
```

#### `validate-config`

Validate configuration file.

```bash
git-repo-manager validate-config [OPTIONS]
```

**Options:**
- `--config PATH` - Configuration file to validate

**Examples:**
```bash
# Validate current configuration
git-repo-manager validate-config

# Validate specific file
git-repo-manager validate-config --config /path/to/config.yml
```

#### `config-info`

Show configuration information.

```bash
git-repo-manager config-info [OPTIONS]
```

**Options:**
- `--mask-sensitive` - Mask sensitive data
- `--format FORMAT` - Output format (text, json, yaml)
- `--debug` - Show debug information

**Examples:**
```bash
# Show current configuration
git-repo-manager config-info

# Show with masked sensitive data
git-repo-manager config-info --mask-sensitive

# Show in JSON format
git-repo-manager config-info --format json
```

### GitLab Commands

#### `clone-user`

Clone repositories owned by the authenticated user.

```bash
git-repo-manager clone-user [OPTIONS]
```

**Options:**
- `--output-dir PATH` - Output directory for repositories
- `--max-concurrent N` - Maximum concurrent downloads
- `--include-pattern PATTERN` - Include repositories matching pattern
- `--exclude-pattern PATTERN` - Exclude repositories matching pattern
- `--shallow` - Use shallow clone
- `--timeout N` - Request timeout in seconds
- `--retry-attempts N` - Number of retry attempts
- `--continue-on-error` - Continue on errors
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Basic usage
git-repo-manager clone-user

# With custom output directory
git-repo-manager clone-user --output-dir /path/to/repos

# With filtering
git-repo-manager clone-user \
  --include-pattern "web-*" \
  --exclude-pattern "deprecated-*" \
  --output-dir /path/to/repos
```

#### `clone-groups`

Clone repositories from GitLab groups.

```bash
git-repo-manager clone-groups [OPTIONS]
```

**Options:**
- `--group-id ID` - Specific group ID to clone from
- `--output-dir PATH` - Output directory for repositories
- `--max-concurrent N` - Maximum concurrent downloads
- `--include-pattern PATTERN` - Include repositories matching pattern
- `--exclude-pattern PATTERN` - Exclude repositories matching pattern
- `--include-archived` - Include archived repositories
- `--shallow` - Use shallow clone
- `--timeout N` - Request timeout in seconds
- `--retry-attempts N` - Number of retry attempts
- `--continue-on-error` - Continue on errors
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Clone from configured groups
git-repo-manager clone-groups

# Clone from specific group
git-repo-manager clone-groups --group-id 123

# With custom output directory
git-repo-manager clone-groups --output-dir /path/to/repos
```

### GitHub Commands

#### `clone-github-user`

Clone repositories from GitHub user.

```bash
git-repo-manager clone-github-user [OPTIONS]
```

**Options:**
- `--username USERNAME` - GitHub username
- `--output-dir PATH` - Output directory for repositories
- `--max-concurrent N` - Maximum concurrent downloads
- `--include-pattern PATTERN` - Include repositories matching pattern
- `--exclude-pattern PATTERN` - Exclude repositories matching pattern
- `--include-forked` - Include forked repositories
- `--shallow` - Use shallow clone
- `--timeout N` - Request timeout in seconds
- `--retry-attempts N` - Number of retry attempts
- `--continue-on-error` - Continue on errors
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Clone from specific user
git-repo-manager clone-github-user --username john-doe

# Clone authenticated user's repositories
git-repo-manager clone-github-user

# With custom output directory
git-repo-manager clone-github-user --username john-doe --output-dir /path/to/repos
```

#### `clone-github-org`

Clone repositories from GitHub organization.

```bash
git-repo-manager clone-github-org [OPTIONS]
```

**Options:**
- `--org-name NAME` - GitHub organization name
- `--output-dir PATH` - Output directory for repositories
- `--max-concurrent N` - Maximum concurrent downloads
- `--include-pattern PATTERN` - Include repositories matching pattern
- `--exclude-pattern PATTERN` - Exclude repositories matching pattern
- `--include-forked` - Include forked repositories
- `--shallow` - Use shallow clone
- `--timeout N` - Request timeout in seconds
- `--retry-attempts N` - Number of retry attempts
- `--continue-on-error` - Continue on errors
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Clone organization repositories
git-repo-manager clone-github-org --org-name my-organization

# With custom output directory
git-repo-manager clone-github-org --org-name my-org --output-dir /path/to/repos
```

### Composer Commands

#### `update-composer`

Update Composer dependencies in repositories.

```bash
git-repo-manager update-composer PATH [OPTIONS]
```

**Arguments:**
- `PATH` - Directory containing repositories to update

**Options:**
- `--strategy STRATEGY` - Update strategy (interactive, auto, dry-run)
- `--backup` - Create backup before updating
- `--exclude-packages PACKAGES` - Exclude specific packages
- `--log-file PATH` - Log file path
- `--max-concurrent N` - Maximum concurrent updates
- `--timeout N` - Update timeout in seconds
- `--continue-on-error` - Continue on errors
- `--verbose` - Enable verbose output

**Examples:**
```bash
# Update dependencies in directory
git-repo-manager update-composer /path/to/repositories

# Update with backup
git-repo-manager update-composer /path/to/repositories --backup

# Update with specific strategy
git-repo-manager update-composer /path/to/repositories --strategy auto
```

## Environment Variables

The following environment variables can be used to override configuration:

### GitLab Variables
- `GITLAB_URL` - GitLab instance URL
- `GITLAB_PRIVATE_TOKEN` - GitLab private token

### GitHub Variables
- `GITHUB_URL` - GitHub API URL
- `GITHUB_ACCESS_TOKEN` - GitHub access token

### Repository Variables
- `REPO_DIR` - Repository directory
- `MAX_CONCURRENT_DOWNLOADS` - Maximum concurrent downloads

### Composer Variables
- `COMPOSER_ENABLED` - Enable Composer operations
- `COMPOSER_AUTO_UPDATE` - Enable auto-update

### Logging Variables
- `LOG_LEVEL` - Logging level
- `LOG_FILE` - Log file path

## Exit Codes

| Code | Description |
|------|-------------|
| `0` | Success |
| `1` | General error |
| `2` | Configuration error |
| `3` | Authentication error |
| `4` | Network error |
| `5` | Permission error |

## Examples

### Basic Workflow

```bash
# 1. Initialize configuration
git-repo-manager init-config

# 2. Clone GitLab repositories
git-repo-manager clone-user --output-dir ./gitlab-repos

# 3. Clone GitHub repositories
git-repo-manager clone-github-user --username john-doe --output-dir ./github-repos

# 4. Update Composer dependencies
git-repo-manager update-composer ./gitlab-repos
git-repo-manager update-composer ./github-repos
```

### Advanced Usage

```bash
# Clone with filtering and custom settings
git-repo-manager clone-user \
  --output-dir /path/to/repos \
  --max-concurrent 10 \
  --include-pattern "web-*" \
  --exclude-pattern "deprecated-*" \
  --shallow \
  --timeout 60 \
  --verbose

# Update with backup and logging
git-repo-manager update-composer /path/to/repos \
  --strategy auto \
  --backup \
  --log-file /path/to/composer.log \
  --exclude-packages "vendor/package1" \
  --verbose
```

### CI/CD Usage

```bash
# In CI/CD pipeline
git-repo-manager clone-github-org --org-name my-org \
  --output-dir $CI_PROJECT_DIR/repos \
  --max-concurrent 3 \
  --continue-on-error

git-repo-manager update-composer $CI_PROJECT_DIR/repos \
  --strategy auto \
  --backup
```

## Help and Support

### Getting Help

```bash
# Show general help
git-repo-manager --help

# Show command help
git-repo-manager clone-user --help

# Show version
git-repo-manager --version
```

### Debugging

```bash
# Enable debug logging
export LOG_LEVEL="DEBUG"

# Run with verbose output
git-repo-manager clone-user --verbose --log-level DEBUG

# Check configuration
git-repo-manager config-info --debug
```

## Configuration File Format

The tool uses YAML configuration files. See [Configuration Guide](configuration.md) for detailed format specification.

## Security Considerations

- Store sensitive tokens in environment variables
- Use secure file permissions for configuration files
- Rotate tokens regularly
- Use least privilege principle for API tokens

## Performance Tips

- Use `--max-concurrent` to optimize for your network
- Use `--shallow` for faster cloning
- Use `--timeout` to handle slow networks
- Use `--continue-on-error` for batch operations 