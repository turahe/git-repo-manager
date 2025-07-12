import os
import yaml
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path


class ConfigManager:
    """Manages configuration loading from YAML file and environment variables"""
    
    def __init__(self, config_file: str = "config.yml"):
        if config_file == "config.yml":
            # Look for config in current directory first, then user home
            current_config = Path("config.yml")
            user_config = Path.home() / ".git-repo-manager" / "config.yml"
            
            if current_config.exists():
                self.config_file = str(current_config)
            elif user_config.exists():
                self.config_file = str(user_config)
            else:
                self.config_file = "config.yml"  # Default fallback
        else:
            self.config_file = config_file
        
        self._config_data = None
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file with environment variable fallback"""
        if self._config_data is None:
            self._config_data = self._load_yaml_config()
        return self._config_data
    
    def _load_yaml_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        config_path = Path(self.config_file)
        
        if not config_path.exists():
            print(f"Warning: Config file '{self.config_file}' not found. Using default values.")
            return self._get_default_config()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                return self._merge_with_env(config)
        except yaml.YAMLError as e:
            print(f"Error parsing config file '{self.config_file}': {e}")
            return self._get_default_config()
        except Exception as e:
            print(f"Error loading config file '{self.config_file}': {e}")
            return self._get_default_config()
    
    def _merge_with_env(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge YAML config with environment variables (env vars take precedence)"""
        # GitLab configuration
        if 'gitlab' in config:
            if os.getenv('GITLAB_URL'):
                config['gitlab']['url'] = os.getenv('GITLAB_URL')
            if os.getenv('GITLAB_PRIVATE_TOKEN'):
                config['gitlab']['private_token'] = os.getenv('GITLAB_PRIVATE_TOKEN')
        
        # GitHub configuration
        if 'github' in config:
            if os.getenv('GITHUB_URL'):
                config['github']['url'] = os.getenv('GITHUB_URL')
            if os.getenv('GITHUB_ACCESS_TOKEN'):
                config['github']['access_token'] = os.getenv('GITHUB_ACCESS_TOKEN')
        
        # Repository configuration
        if 'repository' in config:
            if os.getenv('REPO_DIR'):
                config['repository']['repo_dir'] = os.getenv('REPO_DIR')
            max_downloads = os.getenv('MAX_CONCURRENT_DOWNLOADS')
            if max_downloads:
                config['repository']['max_concurrent_downloads'] = int(max_downloads)
        
        return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'gitlab': {
                'url': 'https://gitlab.com',
                'private_token': os.getenv('GITLAB_PRIVATE_TOKEN', '')
            },
            'github': {
                'url': 'https://api.github.com',
                'access_token': os.getenv('GITHUB_ACCESS_TOKEN', '')
            },
            'repository': {
                'repo_dir': os.getcwd(),
                'max_concurrent_downloads': 5
            },
            'groups': {
                'target_group_ids': []
            },
            'composer': {
                'enabled': True,
                'auto_update': False
            }
        }


# Global config manager instance
config_manager = ConfigManager()


@dataclass
class GitLabConfig:
    """Configuration for GitLab API access"""
    url: str
    private_token: str
    
    @classmethod
    def from_config(cls) -> 'GitLabConfig':
        """Create config from YAML configuration"""
        config = config_manager.load_config()
        gitlab_config = config.get('gitlab', {})
        return cls(
            url=gitlab_config.get('url', 'https://gitlab.com'),
            private_token=gitlab_config.get('private_token', '')
        )
    
    @classmethod
    def from_env(cls) -> 'GitLabConfig':
        """Create config from environment variables (legacy support)"""
        return cls(
            url=os.getenv('GITLAB_URL', 'https://gitlab.com'),
            private_token=os.getenv('GITLAB_PRIVATE_TOKEN', '')
        )


@dataclass
class RepositoryConfig:
    """Configuration for repository operations"""
    repo_dir: str
    max_concurrent_downloads: int
    
    @classmethod
    def from_config(cls) -> 'RepositoryConfig':
        """Create config from YAML configuration"""
        config = config_manager.load_config()
        repo_config = config.get('repository', {})
        return cls(
            repo_dir=repo_config.get('repo_dir', os.getcwd()),
            max_concurrent_downloads=repo_config.get('max_concurrent_downloads', 5)
        )
    
    @classmethod
    def from_env(cls) -> 'RepositoryConfig':
        """Create config from environment variables (legacy support)"""
        return cls(
            repo_dir=os.getenv('REPO_DIR', os.getcwd()),
            max_concurrent_downloads=int(os.getenv('MAX_CONCURRENT_DOWNLOADS', '5'))
        )


@dataclass
class GroupConfig:
    """Configuration for group operations"""
    target_group_ids: List[int]
    
    @classmethod
    def from_config(cls) -> 'GroupConfig':
        """Create config from YAML configuration"""
        config = config_manager.load_config()
        groups_config = config.get('groups', {})
        return cls(
            target_group_ids=groups_config.get('target_group_ids', [])
        )
    
    @classmethod
    def from_env(cls) -> 'GroupConfig':
        """Create config from environment variables (legacy support)"""
        return cls(target_group_ids=[])


@dataclass
class ComposerConfig:
    """Configuration for Composer operations"""
    enabled: bool
    auto_update: bool
    
    @classmethod
    def from_config(cls) -> 'ComposerConfig':
        """Create config from YAML configuration"""
        config = config_manager.load_config()
        composer_config = config.get('composer', {})
        return cls(
            enabled=composer_config.get('enabled', True),
            auto_update=composer_config.get('auto_update', False)
        )


@dataclass
class GitHubConfig:
    """Configuration for GitHub API access"""
    access_token: str
    url: str = "https://api.github.com"
    
    @classmethod
    def from_config(cls) -> 'GitHubConfig':
        """Create config from YAML configuration"""
        config = config_manager.load_config()
        github_config = config.get('github', {})
        return cls(
            access_token=github_config.get('access_token', ''),
            url=github_config.get('url', 'https://api.github.com')
        )
    
    @classmethod
    def from_env(cls) -> 'GitHubConfig':
        """Create config from environment variables (legacy support)"""
        return cls(
            access_token=os.getenv('GITHUB_ACCESS_TOKEN', ''),
            url=os.getenv('GITHUB_URL', 'https://api.github.com')
        ) 