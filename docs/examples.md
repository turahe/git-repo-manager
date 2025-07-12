# Examples

This guide provides practical examples of how to use Git Repository Manager for various scenarios.

## Quick Start Examples

### Basic Setup

```bash
# 1. Initialize configuration
git-repo-manager init-config

# 2. Clone your GitLab repositories
git-repo-manager clone-user

# 3. Update Composer dependencies
git-repo-manager update-composer ./repositories
```

### GitHub Integration

```bash
# Clone repositories from a specific user
git-repo-manager clone-github-user --username john-doe

# Clone organization repositories
git-repo-manager clone-github-org --org-name my-company

# Clone with custom output directory
git-repo-manager clone-github-user --username john-doe --output-dir ./github-repos
```

## Development Environment Setup

### Personal Development Setup

```bash
#!/bin/bash
# setup-dev.sh

echo "Setting up development environment..."

# Initialize configuration
git-repo-manager init-config

# Create directories
mkdir -p ~/repositories/{gitlab,github,composer}

# Clone GitLab repositories
git-repo-manager clone-user --output-dir ~/repositories/gitlab

# Clone GitHub repositories
git-repo-manager clone-github-user --username your-username --output-dir ~/repositories/github

# Update Composer dependencies
git-repo-manager update-composer ~/repositories/gitlab
git-repo-manager update-composer ~/repositories/github

echo "Development environment setup complete!"
```

### Team Development Setup

```bash
#!/bin/bash
# setup-team.sh

echo "Setting up team development environment..."

# Initialize configuration
git-repo-manager init-config

# Create team directories
mkdir -p /var/repositories/{team-a,team-b,shared}

# Clone team repositories
git-repo-manager clone-groups --output-dir /var/repositories/team-a
git-repo-manager clone-github-org --org-name team-a --output-dir /var/repositories/team-a

# Clone shared repositories
git-repo-manager clone-groups --group-id 123 --output-dir /var/repositories/shared

# Update dependencies
git-repo-manager update-composer /var/repositories/team-a
git-repo-manager update-composer /var/repositories/team-b
git-repo-manager update-composer /var/repositories/shared

echo "Team environment setup complete!"
```

## Production Deployment Examples

### Automated Backup System

```bash
#!/bin/bash
# backup-repos.sh

BACKUP_DIR="/backup/repositories/$(date +%Y%m%d)"
LOG_FILE="/var/log/repo-backup.log"

echo "Starting repository backup at $(date)" | tee -a $LOG_FILE

# Create backup directory
mkdir -p $BACKUP_DIR

# Clone repositories with backup
git-repo-manager clone-user \
  --output-dir $BACKUP_DIR/gitlab \
  --max-concurrent 5 \
  --continue-on-error \
  --log-file $LOG_FILE

git-repo-manager clone-github-user --username company-user \
  --output-dir $BACKUP_DIR/github \
  --max-concurrent 5 \
  --continue-on-error \
  --log-file $LOG_FILE

# Update dependencies with backup
git-repo-manager update-composer $BACKUP_DIR/gitlab --backup
git-repo-manager update-composer $BACKUP_DIR/github --backup

echo "Backup completed at $(date)" | tee -a $LOG_FILE
```

### CI/CD Pipeline Integration

```yaml
# .gitlab-ci.yml
stages:
  - setup
  - clone
  - update
  - test

setup:
  stage: setup
  script:
    - pip install git-repo-manager
    - git-repo-manager init-config --non-interactive
  only:
    - main

clone_repos:
  stage: clone
  script:
    - git-repo-manager clone-github-org --org-name my-org --output-dir $CI_PROJECT_DIR/repos
  artifacts:
    paths:
      - repos/
  only:
    - main

update_dependencies:
  stage: update
  script:
    - git-repo-manager update-composer $CI_PROJECT_DIR/repos --strategy auto --backup
  only:
    - main

test_repos:
  stage: test
  script:
    - cd repos
    - for repo in */; do
        echo "Testing $repo"
        cd "$repo"
        composer install --no-dev
        php vendor/bin/phpunit
        cd ..
      done
  only:
    - main
```

## Advanced Usage Examples

### Selective Repository Cloning

```bash
# Clone only web projects
git-repo-manager clone-user \
  --include-pattern "web-*" \
  --exclude-pattern "deprecated-*" \
  --output-dir ./web-projects

# Clone only API projects from organization
git-repo-manager clone-github-org --org-name my-company \
  --include-pattern "api-*" \
  --output-dir ./api-projects

# Clone with specific settings
git-repo-manager clone-groups \
  --group-id 123 \
  --include-pattern "production-*" \
  --exclude-pattern "test-*" \
  --output-dir ./production-repos \
  --max-concurrent 3 \
  --shallow
```

### Batch Operations

```bash
#!/bin/bash
# batch-operations.sh

# Define directories
GITLAB_DIR="./gitlab-repos"
GITHUB_DIR="./github-repos"
COMPOSER_DIR="./composer-repos"

# Clone from multiple sources
echo "Cloning GitLab repositories..."
git-repo-manager clone-user --output-dir $GITLAB_DIR --max-concurrent 5

echo "Cloning GitHub repositories..."
git-repo-manager clone-github-user --username company-user --output-dir $GITHUB_DIR --max-concurrent 5

echo "Cloning organization repositories..."
git-repo-manager clone-github-org --org-name my-company --output-dir $GITHUB_DIR --max-concurrent 5

# Update all repositories
echo "Updating Composer dependencies..."
for dir in $GITLAB_DIR $GITHUB_DIR; do
  if [ -d "$dir" ]; then
    echo "Updating $dir..."
    git-repo-manager update-composer "$dir" --strategy auto --backup
  fi
done

echo "Batch operations completed!"
```

### Monitoring and Logging

```bash
#!/bin/bash
# monitor-repos.sh

LOG_FILE="/var/log/repo-monitor.log"
ERROR_LOG="/var/log/repo-errors.log"

# Function to log with timestamp
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

log "Starting repository monitoring..."

# Clone with detailed logging
git-repo-manager clone-user \
  --output-dir /var/repositories \
  --max-concurrent 3 \
  --log-file $LOG_FILE \
  --log-level INFO \
  --continue-on-error 2>&1 | tee -a $ERROR_LOG

# Check for errors
if [ $? -ne 0 ]; then
    log "Errors occurred during cloning. Check $ERROR_LOG for details."
    exit 1
fi

log "Repository monitoring completed successfully."
```

## Configuration Examples

### Development Configuration

```yaml
# config-dev.yml
gitlab:
  url: "https://gitlab.com"
  private_token: "${GITLAB_TOKEN}"

github:
  url: "https://api.github.com"
  access_token: "${GITHUB_TOKEN}"

repository:
  repo_dir: "./repositories"
  max_concurrent_downloads: 3

groups:
  target_group_ids: [123, 456]

composer:
  enabled: true
  auto_update: false

logging:
  level: "DEBUG"
  file: "./logs/dev.log"
```

### Production Configuration

```yaml
# config-prod.yml
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
  fetch_all_branches: false

groups:
  target_group_ids: [123, 456, 789]
  include_archived: false
  exclude_patterns:
    - "deprecated-*"

composer:
  enabled: true
  auto_update: true
  backup_before_update: true
  exclude_packages:
    - "vendor/legacy-package"

logging:
  level: "WARNING"
  file: "/var/log/git-repo-manager.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

security:
  verify_ssl: true
  allow_insecure: false
  token_encryption: true
```

### CI/CD Configuration

```yaml
# config-ci.yml
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

## Script Examples

### Automated Daily Sync

```bash
#!/bin/bash
# daily-sync.sh

# Configuration
REPO_DIR="/var/repositories"
LOG_DIR="/var/log/repo-sync"
DATE=$(date +%Y%m%d)

# Create log directory
mkdir -p $LOG_DIR

# Function to sync repositories
sync_repos() {
    local source=$1
    local log_file="$LOG_DIR/sync-$source-$DATE.log"
    
    echo "Syncing $source repositories..." | tee -a $log_file
    
    case $source in
        "gitlab")
            git-repo-manager clone-user \
                --output-dir $REPO_DIR/gitlab \
                --max-concurrent 5 \
                --continue-on-error \
                --log-file $log_file
            ;;
        "github")
            git-repo-manager clone-github-user --username company-user \
                --output-dir $REPO_DIR/github \
                --max-concurrent 5 \
                --continue-on-error \
                --log-file $log_file
            ;;
        "groups")
            git-repo-manager clone-groups \
                --output-dir $REPO_DIR/groups \
                --max-concurrent 5 \
                --continue-on-error \
                --log-file $log_file
            ;;
    esac
}

# Sync all sources
sync_repos "gitlab"
sync_repos "github"
sync_repos "groups"

# Update dependencies
echo "Updating Composer dependencies..." | tee -a $LOG_DIR/composer-$DATE.log
git-repo-manager update-composer $REPO_DIR --strategy auto --backup --log-file $LOG_DIR/composer-$DATE.log

echo "Daily sync completed at $(date)"
```

### Repository Health Check

```bash
#!/bin/bash
# health-check.sh

REPO_DIR="/var/repositories"
HEALTH_LOG="/var/log/repo-health.log"

echo "Starting repository health check at $(date)" | tee -a $HEALTH_LOG

# Check repository status
check_repo_health() {
    local repo_path=$1
    local repo_name=$(basename $repo_path)
    
    if [ -d "$repo_path/.git" ]; then
        cd "$repo_path"
        
        # Check if repository is up to date
        git fetch --dry-run >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ $repo_name: Repository is healthy" | tee -a $HEALTH_LOG
        else
            echo "⚠️  $repo_name: Repository needs attention" | tee -a $HEALTH_LOG
        fi
        
        # Check Composer dependencies
        if [ -f "composer.json" ]; then
            composer validate --no-check-publish >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                echo "✅ $repo_name: Composer dependencies are valid" | tee -a $HEALTH_LOG
            else
                echo "❌ $repo_name: Composer dependencies have issues" | tee -a $HEALTH_LOG
            fi
        fi
        
        cd - >/dev/null
    else
        echo "❌ $repo_name: Not a valid Git repository" | tee -a $HEALTH_LOG
    fi
}

# Check all repositories
find $REPO_DIR -maxdepth 2 -type d -name ".git" | while read git_dir; do
    repo_path=$(dirname "$git_dir")
    check_repo_health "$repo_path"
done

echo "Health check completed at $(date)" | tee -a $HEALTH_LOG
```

### Backup and Restore

```bash
#!/bin/bash
# backup-restore.sh

BACKUP_DIR="/backup/repositories"
RESTORE_DIR="/restore/repositories"
DATE=$(date +%Y%m%d)

# Backup function
backup_repos() {
    echo "Creating backup at $BACKUP_DIR/$DATE"
    mkdir -p "$BACKUP_DIR/$DATE"
    
    # Clone fresh copy for backup
    git-repo-manager clone-user --output-dir "$BACKUP_DIR/$DATE/gitlab"
    git-repo-manager clone-github-user --username company-user --output-dir "$BACKUP_DIR/$DATE/github"
    
    # Create archive
    tar -czf "$BACKUP_DIR/repos-$DATE.tar.gz" -C "$BACKUP_DIR" "$DATE"
    
    echo "Backup completed: $BACKUP_DIR/repos-$DATE.tar.gz"
}

# Restore function
restore_repos() {
    local backup_file=$1
    
    if [ ! -f "$backup_file" ]; then
        echo "Backup file not found: $backup_file"
        exit 1
    fi
    
    echo "Restoring from backup: $backup_file"
    mkdir -p "$RESTORE_DIR"
    tar -xzf "$backup_file" -C "$RESTORE_DIR"
    
    echo "Restore completed to: $RESTORE_DIR"
}

# Main script
case "$1" in
    "backup")
        backup_repos
        ;;
    "restore")
        if [ -z "$2" ]; then
            echo "Usage: $0 restore <backup-file>"
            exit 1
        fi
        restore_repos "$2"
        ;;
    *)
        echo "Usage: $0 {backup|restore <backup-file>}"
        exit 1
        ;;
esac
```

## Troubleshooting Examples

### Debug Network Issues

```bash
#!/bin/bash
# debug-network.sh

echo "Debugging network connectivity..."

# Test GitLab connectivity
echo "Testing GitLab connectivity..."
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
     -H "Content-Type: application/json" \
     "$GITLAB_URL/api/v4/user" \
     --connect-timeout 10 \
     --max-time 30

# Test GitHub connectivity
echo "Testing GitHub connectivity..."
curl -H "Authorization: token $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     "https://api.github.com/user" \
     --connect-timeout 10 \
     --max-time 30

# Test with verbose output
echo "Running with verbose output..."
git-repo-manager clone-user --verbose --log-level DEBUG
```

### Fix Common Issues

```bash
#!/bin/bash
# fix-issues.sh

echo "Fixing common issues..."

# Fix permission issues
echo "Fixing file permissions..."
chmod 600 config.yml
chmod 700 ~/.git-repo-manager

# Clear cached data
echo "Clearing cached data..."
rm -rf ~/.cache/git-repo-manager

# Reinstall dependencies
echo "Reinstalling dependencies..."
pip install --upgrade git-repo-manager

# Validate configuration
echo "Validating configuration..."
git-repo-manager validate-config

echo "Issue fixing completed!"
```

## Performance Optimization Examples

### Optimize for Large Repositories

```bash
#!/bin/bash
# optimize-large-repos.sh

echo "Optimizing for large repositories..."

# Use shallow clones for speed
git-repo-manager clone-user \
    --shallow \
    --max-concurrent 3 \
    --timeout 120 \
    --output-dir ./large-repos

# Use specific patterns to reduce scope
git-repo-manager clone-groups \
    --include-pattern "production-*" \
    --exclude-pattern "test-*,dev-*" \
    --shallow \
    --max-concurrent 2 \
    --output-dir ./production-repos

echo "Large repository optimization completed!"
```

### Memory-Efficient Processing

```bash
#!/bin/bash
# memory-efficient.sh

echo "Running memory-efficient processing..."

# Process repositories in batches
BATCH_SIZE=10
REPO_DIR="./repositories"

# Get list of repositories
repos=($(find $REPO_DIR -maxdepth 1 -type d -name "*"))

# Process in batches
for ((i=0; i<${#repos[@]}; i+=$BATCH_SIZE)); do
    batch=("${repos[@]:i:$BATCH_SIZE}")
    
    echo "Processing batch $((i/BATCH_SIZE + 1))..."
    
    for repo in "${batch[@]}"; do
        if [ -d "$repo/.git" ]; then
            echo "Processing $repo"
            git-repo-manager update-composer "$repo" --strategy auto
        fi
    done
    
    # Clear memory
    echo "Clearing memory..."
    sync
    echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true
done

echo "Memory-efficient processing completed!"
```

These examples demonstrate various use cases and best practices for using Git Repository Manager effectively in different environments and scenarios. 