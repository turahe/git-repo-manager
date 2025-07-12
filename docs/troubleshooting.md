# Troubleshooting Guide

This guide helps you resolve common issues when using Git Repository Manager.

## Quick Diagnosis

### Check Tool Status

```bash
# Check if tool is installed correctly
git-repo-manager --version

# Check configuration
git-repo-manager config-info

# Validate configuration
git-repo-manager validate-config
```

### Check System Requirements

```bash
# Check Python version
python --version

# Check if required tools are available
git --version
composer --version
```

## Common Issues and Solutions

### 1. Authentication Issues

#### Problem: "401 Unauthorized" or "Authentication failed"

**Symptoms:**
- Error messages about authentication
- Unable to access repositories
- Token-related errors

**Solutions:**

1. **Check Token Validity**
   ```bash
   # Test GitLab token
   curl -H "Authorization: Bearer YOUR_GITLAB_TOKEN" \
        "https://gitlab.com/api/v4/user"
   
   # Test GitHub token
   curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
        "https://api.github.com/user"
   ```

2. **Reinitialize Configuration**
   ```bash
   git-repo-manager init-config
   ```

3. **Check Environment Variables**
   ```bash
   # Check if tokens are set
   echo $GITLAB_PRIVATE_TOKEN
   echo $GITHUB_ACCESS_TOKEN
   ```

4. **Verify Token Permissions**
   - GitLab: Ensure token has `read_api` scope
   - GitHub: Ensure token has `repo` scope

#### Problem: "403 Forbidden"

**Solutions:**

1. **Check Repository Access**
   ```bash
   # Test specific repository access
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        "https://gitlab.com/api/v4/projects/PROJECT_ID"
   ```

2. **Verify Group Membership**
   - Ensure you're a member of the GitLab group
   - Check group visibility settings

### 2. Network Issues

#### Problem: "Connection timeout" or "Network error"

**Symptoms:**
- Slow or failed connections
- Timeout errors
- Network-related exceptions

**Solutions:**

1. **Check Network Connectivity**
   ```bash
   # Test basic connectivity
   ping gitlab.com
   ping api.github.com
   
   # Test API endpoints
   curl -I https://gitlab.com/api/v4/version
   curl -I https://api.github.com
   ```

2. **Increase Timeout**
   ```bash
   git-repo-manager clone-user --timeout 120
   ```

3. **Use Proxy (if needed)**
   ```bash
   # Set proxy environment variables
   export HTTP_PROXY="http://proxy.company.com:8080"
   export HTTPS_PROXY="http://proxy.company.com:8080"
   ```

4. **Check Firewall Settings**
   - Ensure outbound HTTPS (443) is allowed
   - Check corporate firewall rules

#### Problem: "SSL Certificate" errors

**Solutions:**

1. **Update CA Certificates**
   ```bash
   # On Ubuntu/Debian
   sudo apt update && sudo apt install ca-certificates
   
   # On CentOS/RHEL
   sudo yum update ca-certificates
   ```

2. **Check Certificate Chain**
   ```bash
   openssl s_client -connect gitlab.com:443 -servername gitlab.com
   ```

### 3. Configuration Issues

#### Problem: "Configuration file not found"

**Symptoms:**
- Tool can't find config.yml
- Configuration errors

**Solutions:**

1. **Check Configuration File Location**
   ```bash
   # List possible config locations
   ls -la config.yml
   ls -la ~/.git-repo-manager/config.yml
   ls -la /etc/git-repo-manager/config.yml
   ```

2. **Create Default Configuration**
   ```bash
   git-repo-manager init-config
   ```

3. **Specify Config File**
   ```bash
   git-repo-manager clone-user --config /path/to/config.yml
   ```

#### Problem: "Invalid YAML" or "Configuration error"

**Solutions:**

1. **Validate YAML Syntax**
   ```bash
   # Check YAML syntax
   python -c "import yaml; yaml.safe_load(open('config.yml'))"
   ```

2. **Check Configuration Structure**
   ```bash
   # Show current configuration
   git-repo-manager config-info
   ```

3. **Use Example Configuration**
   ```bash
   # Copy example configuration
   cp config.example.yml config.yml
   # Edit as needed
   nano config.yml
   ```

### 4. Repository Issues

#### Problem: "Repository already exists" or "Directory not empty"

**Solutions:**

1. **Clean Existing Repositories**
   ```bash
   # Remove existing repositories
   rm -rf /path/to/repositories/*
   
   # Or use force option (if available)
   git-repo-manager clone-user --force
   ```

2. **Use Different Output Directory**
   ```bash
   git-repo-manager clone-user --output-dir /path/to/new/repos
   ```

#### Problem: "Git clone failed" or "Repository not found"

**Solutions:**

1. **Check Repository URL**
   ```bash
   # Test repository access
   git ls-remote https://github.com/user/repo.git
   ```

2. **Verify Repository Permissions**
   - Ensure you have access to the repository
   - Check if repository is private/public

3. **Use SSH Instead of HTTPS**
   ```bash
   # Configure Git to use SSH
   git config --global url."git@github.com:".insteadOf "https://github.com/"
   ```

### 5. Composer Issues

#### Problem: "Composer not found" or "Composer command failed"

**Solutions:**

1. **Install Composer**
   ```bash
   # Install Composer globally
   curl -sS https://getcomposer.org/installer | php
   sudo mv composer.phar /usr/local/bin/composer
   ```

2. **Check Composer Installation**
   ```bash
   composer --version
   which composer
   ```

3. **Update Composer**
   ```bash
   composer self-update
   ```

#### Problem: "Composer dependencies update failed"

**Solutions:**

1. **Check Composer.json**
   ```bash
   # Validate composer.json
   composer validate
   ```

2. **Clear Composer Cache**
   ```bash
   composer clear-cache
   ```

3. **Update with Verbose Output**
   ```bash
   git-repo-manager update-composer /path/to/repos --verbose
   ```

### 6. Permission Issues

#### Problem: "Permission denied" or "Access denied"

**Solutions:**

1. **Check File Permissions**
   ```bash
   # Check config file permissions
   ls -la config.yml
   
   # Fix permissions
   chmod 600 config.yml
   chmod 700 ~/.git-repo-manager
   ```

2. **Check Directory Permissions**
   ```bash
   # Check output directory permissions
   ls -la /path/to/output/directory
   
   # Fix directory permissions
   chmod 755 /path/to/output/directory
   ```

3. **Run as Correct User**
   ```bash
   # Ensure you're running as the correct user
   whoami
   sudo -u correct-user git-repo-manager clone-user
   ```

### 7. Performance Issues

#### Problem: "Slow cloning" or "Memory issues"

**Solutions:**

1. **Reduce Concurrent Operations**
   ```bash
   git-repo-manager clone-user --max-concurrent 2
   ```

2. **Use Shallow Clones**
   ```bash
   git-repo-manager clone-user --shallow
   ```

3. **Optimize Network Settings**
   ```bash
   # Increase Git buffer size
   git config --global http.postBuffer 524288000
   git config --global http.maxRequestBuffer 100M
   ```

4. **Use Specific Patterns**
   ```bash
   # Clone only specific repositories
   git-repo-manager clone-user --include-pattern "important-*"
   ```

## Debug Mode

### Enable Debug Logging

```bash
# Set debug environment variable
export LOG_LEVEL="DEBUG"

# Run with verbose output
git-repo-manager clone-user --verbose --log-level DEBUG

# Check debug information
git-repo-manager config-info --debug
```

### Debug Network Issues

```bash
#!/bin/bash
# debug-network.sh

echo "=== Network Debug Information ==="

# Test basic connectivity
echo "1. Testing basic connectivity..."
ping -c 3 gitlab.com
ping -c 3 api.github.com

# Test API endpoints
echo "2. Testing API endpoints..."
curl -I https://gitlab.com/api/v4/version
curl -I https://api.github.com

# Test with authentication
echo "3. Testing authenticated endpoints..."
if [ ! -z "$GITLAB_PRIVATE_TOKEN" ]; then
    curl -H "Authorization: Bearer $GITLAB_PRIVATE_TOKEN" \
         "https://gitlab.com/api/v4/user" | head -5
fi

if [ ! -z "$GITHUB_ACCESS_TOKEN" ]; then
    curl -H "Authorization: token $GITHUB_ACCESS_TOKEN" \
         "https://api.github.com/user" | head -5
fi

echo "=== Debug Complete ==="
```

### Debug Configuration

```bash
#!/bin/bash
# debug-config.sh

echo "=== Configuration Debug Information ==="

# Check Python version
echo "1. Python version:"
python --version

# Check tool installation
echo "2. Tool installation:"
git-repo-manager --version

# Check configuration
echo "3. Configuration:"
git-repo-manager config-info --mask-sensitive

# Check environment variables
echo "4. Environment variables:"
echo "GITLAB_URL: ${GITLAB_URL:-not set}"
echo "GITLAB_PRIVATE_TOKEN: ${GITLAB_PRIVATE_TOKEN:+set}"
echo "GITHUB_ACCESS_TOKEN: ${GITHUB_ACCESS_TOKEN:+set}"

# Check file permissions
echo "5. File permissions:"
ls -la config.yml 2>/dev/null || echo "config.yml not found"
ls -la ~/.git-repo-manager/ 2>/dev/null || echo "~/.git-repo-manager/ not found"

echo "=== Debug Complete ==="
```

## Error Codes Reference

| Error Code | Description | Common Causes | Solutions |
|------------|-------------|---------------|-----------|
| `1` | General error | Various | Check logs, run with --verbose |
| `2` | Configuration error | Invalid config | Validate configuration |
| `3` | Authentication error | Invalid tokens | Check token validity |
| `4` | Network error | Connectivity issues | Check network, increase timeout |
| `5` | Permission error | File/directory permissions | Fix permissions |

## Log Analysis

### Common Log Patterns

```bash
# Search for errors in logs
grep -i "error\|failed\|exception" /path/to/log/file

# Search for authentication issues
grep -i "401\|403\|unauthorized\|forbidden" /path/to/log/file

# Search for network issues
grep -i "timeout\|connection\|network" /path/to/log/file
```

### Log File Locations

- **Default logs**: `./logs/` (relative to current directory)
- **System logs**: `/var/log/git-repo-manager.log`
- **User logs**: `~/.git-repo-manager/logs/`

## Getting Help

### Before Asking for Help

1. **Collect Information**
   ```bash
   # System information
   uname -a
   python --version
   git --version
   
   # Tool information
   git-repo-manager --version
   git-repo-manager config-info --mask-sensitive
   
   # Error logs
   tail -50 /path/to/log/file
   ```

2. **Reproduce the Issue**
   ```bash
   # Run with debug output
   git-repo-manager clone-user --verbose --log-level DEBUG
   ```

3. **Check Known Issues**
   - Search existing GitHub issues
   - Check documentation for known limitations

### Contact Support

When contacting support, include:

1. **Environment Information**
   - Operating system and version
   - Python version
   - Tool version

2. **Error Details**
   - Complete error message
   - Steps to reproduce
   - Relevant log files

3. **Configuration**
   - Configuration file (with sensitive data masked)
   - Environment variables used

4. **Network Information**
   - Corporate firewall/proxy settings
   - Network restrictions

## Prevention Tips

### Best Practices

1. **Regular Maintenance**
   ```bash
   # Update tool regularly
   pip install --upgrade git-repo-manager
   
   # Rotate tokens periodically
   # Update configuration as needed
   ```

2. **Monitor Usage**
   ```bash
   # Check for errors in logs
   tail -f /var/log/git-repo-manager.log
   
   # Monitor repository health
   git-repo-manager config-info
   ```

3. **Backup Configuration**
   ```bash
   # Backup configuration
   cp config.yml config.yml.backup
   cp ~/.git-repo-manager/config.yml ~/.git-repo-manager/config.yml.backup
   ```

4. **Test Changes**
   ```bash
   # Test configuration changes
   git-repo-manager validate-config
   
   # Test with small subset
   git-repo-manager clone-user --include-pattern "test-*"
   ```

This troubleshooting guide should help you resolve most common issues. If you continue to experience problems, please refer to the [Examples](examples.md) for additional solutions or contact support with detailed information about your specific issue. 