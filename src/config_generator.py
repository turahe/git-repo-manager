import os
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigGenerator:
    """Generates configuration files for the GitLab Repository Manager"""
    
    def __init__(self):
        self.home_dir = Path.home()
        self.config_path = self.home_dir / ".gitlab-repo-manager" / "config.yml"
    
    def generate_config(self, force: bool = False, interactive: bool = True) -> bool:
        """
        Generate a config.yml file in the user's home directory
        
        Args:
            force: If True, overwrite existing config file
            interactive: If True, prompt user for configuration values
            
        Returns:
            True if config was generated successfully, False otherwise
        """
        # Create config directory
        config_dir = self.config_path.parent
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if config already exists
        if self.config_path.exists() and not force:
            print(f"⚠️  Config file already exists: {self.config_path}")
            print("Use --force to overwrite existing config")
            return False
        
        # Generate config data
        if interactive:
            config_data = self._interactive_config()
        else:
            config_data = self._get_default_config()
        
        # Write config file
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, indent=2, sort_keys=False)
            
            print(f"✅ Config file generated: {self.config_path}")
            if not interactive:
                print("📝 Please edit the config file with your GitLab token and group IDs")
            return True
            
        except Exception as e:
            print(f"❌ Error generating config file: {e}")
            return False
    
    def _interactive_config(self) -> Dict[str, Any]:
        """Interactive configuration setup"""
        print("🚀 GitLab Repository Manager - Interactive Configuration")
        print("=" * 55)
        print()
        
        config = {}
        
        # GitLab Configuration
        print("📋 GitLab Configuration")
        print("-" * 25)
        
        # GitLab URL
        default_url = "https://gitlab.com"
        gitlab_url = input(f"GitLab URL [{default_url}]: ").strip()
        if not gitlab_url:
            gitlab_url = default_url
        
        # GitLab Token
        print("\n🔑 GitLab Personal Access Token")
        print("   You need a GitLab Personal Access Token with 'read_api' and 'read_repository' permissions.")
        print("   Get it from: https://gitlab.com/-/user_settings/personal_access_tokens")
        print()
        
        while True:
            private_token = input("Enter your GitLab Personal Access Token: ").strip()
            if private_token:
                break
            print("❌ Token is required. Please enter your GitLab token.")
        
        config['gitlab'] = {
            'url': gitlab_url,
            'private_token': private_token
        }
        
        # GitHub Configuration
        print("\n📋 GitHub Configuration")
        print("-" * 25)
        
        # GitHub URL
        default_github_url = "https://api.github.com"
        github_url = input(f"GitHub API URL [{default_github_url}]: ").strip()
        if not github_url:
            github_url = default_github_url
        
        # GitHub Token
        print("\n🔑 GitHub Personal Access Token")
        print("   You need a GitHub Personal Access Token with 'repo' permissions.")
        print("   Get it from: https://github.com/settings/tokens")
        print("   (Optional - leave empty if you don't want to use GitHub)")
        print()
        
        github_token = input("Enter your GitHub Personal Access Token (optional): ").strip()
        
        config['github'] = {
            'url': github_url,
            'access_token': github_token
        }
        
        # Repository Configuration
        print("\n📁 Repository Configuration")
        print("-" * 30)
        
        default_repo_dir = str(self.home_dir / 'gitlab-repos')
        repo_dir = input(f"Repository directory [{default_repo_dir}]: ").strip()
        if not repo_dir:
            repo_dir = default_repo_dir
        
        default_workers = "5"
        max_workers = input(f"Maximum concurrent downloads [{default_workers}]: ").strip()
        if not max_workers:
            max_workers = default_workers
        
        try:
            max_workers = int(max_workers)
        except ValueError:
            max_workers = 5
        
        config['repository'] = {
            'repo_dir': repo_dir,
            'max_concurrent_downloads': max_workers
        }
        
        # Group Configuration
        print("\n👥 Group Configuration")
        print("-" * 25)
        print("Enter GitLab group IDs to clone repositories from.")
        print("You can find group IDs in the GitLab web interface.")
        print("Press Enter without a value to use default groups.")
        print()
        
        group_ids = []
        while True:
            group_input = input("Enter group ID (or press Enter to finish): ").strip()
            if not group_input:
                break
            
            try:
                group_id = int(group_input)
                group_ids.append(group_id)
                print(f"✅ Added group ID: {group_id}")
            except ValueError:
                print("❌ Invalid group ID. Please enter a number.")
        
        # Use default groups if none provided
        if not group_ids:
            print("📋 Using default group IDs...")
            group_ids = [
                2969050,   # circlecreative
                60830364,  # circle-creative-flutter
                12276251,  # church-id
                7629247,   # kreditimpian-id
                6443630,   # itsynergy
                4939058,   # pluses-media
                2987114,   # o2system
                2968903,   # baliparamartha
                108468311, # x-api
                110485899, # neo
                60815546,  # sendx
                60815062,  # motoriz
                60789937,  # cicilsewa
                60789934,  # tokobot
                14193703,  # xignature
                13844839,  # simplex
                13844814,  # Lawtify
            ]
        
        config['groups'] = {
            'target_group_ids': group_ids
        }
        
        # Composer Configuration
        print("\n🔧 Composer Configuration")
        print("-" * 25)
        
        composer_enabled = input("Enable Composer dependency updates? (y/N): ").strip().lower()
        composer_enabled = composer_enabled in ['y', 'yes']
        
        auto_update = False
        if composer_enabled:
            auto_update = input("Automatically update Composer dependencies after cloning? (y/N): ").strip().lower()
            auto_update = auto_update in ['y', 'yes']
        
        config['composer'] = {
            'enabled': composer_enabled,
            'auto_update': auto_update
        }
        
        # Summary
        print("\n📋 Configuration Summary")
        print("=" * 25)
        print(f"GitLab URL: {gitlab_url}")
        print(f"GitHub URL: {github_url}")
        print(f"GitHub Token: {'Configured' if github_token else 'Not configured'}")
        print(f"Repository Directory: {repo_dir}")
        print(f"Max Concurrent Downloads: {max_workers}")
        print(f"Group IDs: {len(group_ids)} groups")
        print(f"Composer Enabled: {composer_enabled}")
        print(f"Auto Update Composer: {auto_update}")
        print()
        
        confirm = input("Save this configuration? (Y/n): ").strip().lower()
        if confirm in ['n', 'no']:
            print("❌ Configuration cancelled.")
            raise ValueError("Configuration cancelled by user")
        
        return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration structure"""
        return {
            'gitlab': {
                'url': 'https://gitlab.com',
                'private_token': 'your-gitlab-token-here'
            },
            'repository': {
                'repo_dir': str(self.home_dir / 'gitlab-repos'),
                'max_concurrent_downloads': 5
            },
            'groups': {
                'target_group_ids': [
                    2969050,   # circlecreative
                    60830364,  # circle-creative-flutter
                    12276251,  # church-id
                    7629247,   # kreditimpian-id
                    6443630,   # itsynergy
                    4939058,   # pluses-media
                    2987114,   # o2system
                    2968903,   # baliparamartha
                    108468311, # x-api
                    110485899, # neo
                    60815546,  # sendx
                    60815062,  # motoriz
                    60789937,  # cicilsewa
                    60789934,  # tokobot
                    14193703,  # xignature
                    13844839,  # simplex
                    13844814,  # Lawtify
                ]
            },
            'composer': {
                'enabled': True,
                'auto_update': False
            }
        }
    
    def get_config_path(self) -> Path:
        """Get the path to the user's config file"""
        return self.config_path
    
    def config_exists(self) -> bool:
        """Check if user config file exists"""
        return self.config_path.exists()
    
    def show_config_info(self):
        """Show information about the config file"""
        if self.config_exists():
            print(f"📁 Config file location: {self.config_path}")
            print(f"📄 Config file exists: Yes")
            
            # Show config file size
            size = self.config_path.stat().st_size
            print(f"📊 Config file size: {size} bytes")
            
            # Show last modified
            mtime = self.config_path.stat().st_mtime
            from datetime import datetime
            mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"🕒 Last modified: {mtime_str}")
        else:
            print(f"📁 Config file location: {self.config_path}")
            print(f"📄 Config file exists: No")
            print("💡 Run 'gitlab-repo-manager init-config' to create config file")
    
    def validate_config(self) -> bool:
        """Validate the existing config file"""
        if not self.config_exists():
            print("❌ Config file does not exist")
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Check required sections
            required_sections = ['gitlab', 'repository', 'groups', 'composer']
            for section in required_sections:
                if section not in config:
                    print(f"❌ Missing required section: {section}")
                    return False
            
            # Check GitLab token
            if not config['gitlab'].get('private_token') or config['gitlab']['private_token'] == 'your-gitlab-token-here':
                print("⚠️  GitLab token not configured")
                print("   Please update the 'private_token' in the gitlab section")
            
            # Check group IDs
            group_ids = config['groups'].get('target_group_ids', [])
            if not group_ids:
                print("⚠️  No group IDs configured")
                print("   Please add group IDs to the 'target_group_ids' list")
            
            print("✅ Config file is valid")
            return True
            
        except yaml.YAMLError as e:
            print(f"❌ Invalid YAML in config file: {e}")
            return False
        except Exception as e:
            print(f"❌ Error reading config file: {e}")
            return False 