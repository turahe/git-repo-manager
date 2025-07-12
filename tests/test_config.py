import os
import tempfile
import pytest
from unittest.mock import patch, mock_open
from src.config import (
    GitLabConfig, RepositoryConfig, GroupConfig, ComposerConfig, GitHubConfig,
    ConfigManager
)


class TestGitLabConfig:
    """Test GitLabConfig class"""
    
    def test_gitlab_config_creation(self):
        """Test creating GitLabConfig instance"""
        config = GitLabConfig(url="https://gitlab.com", private_token="test-token")
        assert config.url == "https://gitlab.com"
        assert config.private_token == "test-token"
    
    def test_gitlab_config_from_env(self):
        """Test creating GitLabConfig from environment variables"""
        with patch.dict(os.environ, {
            'GITLAB_URL': 'https://gitlab.company.com',
            'GITLAB_PRIVATE_TOKEN': 'env-token'
        }):
            config = GitLabConfig.from_env()
            assert config.url == "https://gitlab.company.com"
            assert config.private_token == "env-token"
    
    def test_gitlab_config_from_config(self):
        """Test creating GitLabConfig from config file"""
        mock_config = {
            'gitlab': {
                'url': 'https://gitlab.com',
                'private_token': 'config-token'
            }
        }
        
        with patch('src.config.config_manager.load_config', return_value=mock_config):
            config = GitLabConfig.from_config()
            assert config.url == "https://gitlab.com"
            assert config.private_token == "config-token"


class TestGitHubConfig:
    """Test GitHubConfig class"""
    
    def test_github_config_creation(self):
        """Test creating GitHubConfig instance"""
        config = GitHubConfig(access_token="test-token", url="https://api.github.com")
        assert config.access_token == "test-token"
        assert config.url == "https://api.github.com"
    
    def test_github_config_default_url(self):
        """Test GitHubConfig with default URL"""
        config = GitHubConfig(access_token="test-token")
        assert config.url == "https://api.github.com"
    
    def test_github_config_from_env(self):
        """Test creating GitHubConfig from environment variables"""
        with patch.dict(os.environ, {
            'GITHUB_ACCESS_TOKEN': 'env-token',
            'GITHUB_URL': 'https://api.github.com'
        }):
            config = GitHubConfig.from_env()
            assert config.access_token == "env-token"
            assert config.url == "https://api.github.com"
    
    def test_github_config_from_config(self):
        """Test creating GitHubConfig from config file"""
        mock_config = {
            'github': {
                'url': 'https://api.github.com',
                'access_token': 'config-token'
            }
        }
        
        with patch('src.config.config_manager.load_config', return_value=mock_config):
            config = GitHubConfig.from_config()
            assert config.access_token == "config-token"
            assert config.url == "https://api.github.com"


class TestRepositoryConfig:
    """Test RepositoryConfig class"""
    
    def test_repository_config_creation(self):
        """Test creating RepositoryConfig instance"""
        config = RepositoryConfig(repo_dir="/test/path", max_concurrent_downloads=10)
        assert config.repo_dir == "/test/path"
        assert config.max_concurrent_downloads == 10
    
    def test_repository_config_from_env(self):
        """Test creating RepositoryConfig from environment variables"""
        with patch.dict(os.environ, {
            'REPO_DIR': '/env/path',
            'MAX_CONCURRENT_DOWNLOADS': '15'
        }):
            config = RepositoryConfig.from_env()
            assert config.repo_dir == "/env/path"
            assert config.max_concurrent_downloads == 15
    
    def test_repository_config_from_config(self):
        """Test creating RepositoryConfig from config file"""
        mock_config = {
            'repository': {
                'repo_dir': '/config/path',
                'max_concurrent_downloads': 20
            }
        }
        
        with patch('src.config.config_manager.load_config', return_value=mock_config):
            config = RepositoryConfig.from_config()
            assert config.repo_dir == "/config/path"
            assert config.max_concurrent_downloads == 20


class TestGroupConfig:
    """Test GroupConfig class"""
    
    def test_group_config_creation(self):
        """Test creating GroupConfig instance"""
        config = GroupConfig(target_group_ids=[1, 2, 3])
        assert config.target_group_ids == [1, 2, 3]
    
    def test_group_config_from_config(self):
        """Test creating GroupConfig from config file"""
        mock_config = {
            'groups': {
                'target_group_ids': [10, 20, 30]
            }
        }
        
        with patch('src.config.config_manager.load_config', return_value=mock_config):
            config = GroupConfig.from_config()
            assert config.target_group_ids == [10, 20, 30]


class TestComposerConfig:
    """Test ComposerConfig class"""
    
    def test_composer_config_creation(self):
        """Test creating ComposerConfig instance"""
        config = ComposerConfig(enabled=True, auto_update=True)
        assert config.enabled is True
        assert config.auto_update is True
    
    def test_composer_config_from_config(self):
        """Test creating ComposerConfig from config file"""
        mock_config = {
            'composer': {
                'enabled': True,
                'auto_update': False
            }
        }
        
        with patch('src.config.config_manager.load_config', return_value=mock_config):
            config = ComposerConfig.from_config()
            assert config.enabled is True
            assert config.auto_update is False


class TestConfigManager:
    """Test ConfigManager class"""
    
    def test_config_manager_creation(self):
        """Test creating ConfigManager instance"""
        manager = ConfigManager()
        assert manager is not None
    
    def test_get_default_config(self):
        """Test getting default configuration"""
        manager = ConfigManager()
        config = manager._get_default_config()
        
        assert 'gitlab' in config
        assert 'github' in config
        assert 'repository' in config
        assert 'groups' in config
        assert 'composer' in config
    
    def test_merge_with_env(self):
        """Test merging configuration with environment variables"""
        manager = ConfigManager()
        config = {
            'gitlab': {'url': 'old-url', 'private_token': 'old-token'},
            'github': {'url': 'old-github-url', 'access_token': 'old-github-token'},
            'repository': {'repo_dir': 'old-dir', 'max_concurrent_downloads': 5}
        }
        
        with patch.dict(os.environ, {
            'GITLAB_URL': 'new-url',
            'GITLAB_PRIVATE_TOKEN': 'new-token',
            'GITHUB_URL': 'new-github-url',
            'GITHUB_ACCESS_TOKEN': 'new-github-token',
            'REPO_DIR': 'new-dir',
            'MAX_CONCURRENT_DOWNLOADS': '10'
        }):
            merged_config = manager._merge_with_env(config)
            
            assert merged_config['gitlab']['url'] == 'new-url'
            assert merged_config['gitlab']['private_token'] == 'new-token'
            assert merged_config['github']['url'] == 'new-github-url'
            assert merged_config['github']['access_token'] == 'new-github-token'
            assert merged_config['repository']['repo_dir'] == 'new-dir'
            assert merged_config['repository']['max_concurrent_downloads'] == 10
    
    def test_load_config_file_exists(self):
        """Test loading configuration from existing file"""
        mock_config_data = {
            'gitlab': {'url': 'test-url', 'private_token': 'test-token'},
            'github': {'url': 'test-github-url', 'access_token': 'test-github-token'},
            'repository': {'repo_dir': 'test-dir', 'max_concurrent_downloads': 5},
            'groups': {'target_group_ids': [1, 2, 3]},
            'composer': {'enabled': True, 'auto_update': False}
        }
        
        with patch('builtins.open', mock_open(read_data='gitlab:\n  url: test-url\n')):
            with patch('yaml.safe_load', return_value=mock_config_data):
                with patch('os.path.exists', return_value=True):
                    manager = ConfigManager()
                    config = manager.load_config()
                    assert config == mock_config_data
    
    def test_load_config_file_not_exists(self):
        """Test loading configuration when file doesn't exist"""
        with patch('os.path.exists', return_value=False):
            manager = ConfigManager()
            config = manager.load_config()
            assert 'gitlab' in config
            assert 'github' in config
            assert 'repository' in config
            assert 'groups' in config
            assert 'composer' in config 