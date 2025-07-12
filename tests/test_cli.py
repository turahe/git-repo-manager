from unittest.mock import patch, Mock
import click
from click.testing import CliRunner
from cli import cli


class TestCLI:
    """Test CLI commands"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.runner = CliRunner()
    
    def test_cli_help(self):
        """Test CLI help command"""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "Usage:" in result.output
    
    @patch('cli.UserRepositoryService')
    @patch('cli.GitLabConfig')
    @patch('cli.RepositoryConfig')
    def test_clone_user_command(self, mock_repo_config, mock_gitlab_config, mock_service):
        """Test clone-user command"""
        # Mock configurations
        mock_gitlab_config.from_config.return_value = Mock()
        mock_repo_config.from_config.return_value = Mock()
        
        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        
        result = self.runner.invoke(cli, ['clone-user'])
        assert result.exit_code == 0
    
    @patch('cli.GroupRepositoryService')
    @patch('cli.GitLabConfig')
    @patch('cli.RepositoryConfig')
    @patch('cli.GroupConfig')
    def test_clone_groups_command(self, mock_group_config, mock_repo_config, mock_gitlab_config, mock_service):
        """Test clone-groups command"""
        # Mock configurations
        mock_gitlab_config.from_config.return_value = Mock()
        mock_repo_config.from_config.return_value = Mock()
        mock_group_config.from_config.return_value = Mock()
        
        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        
        result = self.runner.invoke(cli, ['clone-groups'])
        assert result.exit_code == 0
    
    @patch('cli.GitHubUserService')
    @patch('cli.GitHubConfig')
    @patch('cli.RepositoryConfig')
    def test_clone_github_user_command(self, mock_repo_config, mock_github_config, mock_service):
        """Test clone-github-user command"""
        # Mock configurations
        mock_github_config.from_config.return_value = Mock()
        mock_repo_config.from_config.return_value = Mock()
        
        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        
        result = self.runner.invoke(cli, ['clone-github-user'])
        assert result.exit_code == 0
    
    @patch('cli.GitHubOrganizationService')
    @patch('cli.GitHubConfig')
    @patch('cli.RepositoryConfig')
    def test_clone_github_org_command(self, mock_repo_config, mock_github_config, mock_service):
        """Test clone-github-org command"""
        # Mock configurations
        mock_github_config.from_config.return_value = Mock()
        mock_repo_config.from_config.return_value = Mock()
        
        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        
        result = self.runner.invoke(cli, ['clone-github-org', 'testorg'])
        assert result.exit_code == 0
    
    @patch('cli.ComposerService')
    def test_update_composer_command(self, mock_service):
        """Test update-composer command"""
        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        
        result = self.runner.invoke(cli, ['update-composer'])
        assert result.exit_code == 0
    
    @patch('cli.ConfigGenerator')
    def test_init_config_command(self, mock_generator):
        """Test init-config command"""
        # Mock generator
        mock_generator_instance = Mock()
        mock_generator.return_value = mock_generator_instance
        
        result = self.runner.invoke(cli, ['init-config'])
        assert result.exit_code == 0
    
    @patch('cli.ConfigGenerator')
    def test_init_config_non_interactive_command(self, mock_generator):
        """Test init-config non-interactive command"""
        # Mock generator
        mock_generator_instance = Mock()
        mock_generator.return_value = mock_generator_instance
        
        result = self.runner.invoke(cli, ['init-config', '--non-interactive'])
        assert result.exit_code == 0
    
    @patch('cli.ConfigGenerator')
    def test_config_info_command(self, mock_generator):
        """Test config-info command"""
        # Mock generator
        mock_generator_instance = Mock()
        mock_generator.return_value = mock_generator_instance
        
        result = self.runner.invoke(cli, ['config-info'])
        assert result.exit_code == 0
    
    @patch('cli.ConfigGenerator')
    def test_validate_config_command(self, mock_generator):
        """Test validate-config command"""
        # Mock generator
        mock_generator_instance = Mock()
        mock_generator_instance.validate_config.return_value = True
        mock_generator.return_value = mock_generator_instance
        
        result = self.runner.invoke(cli, ['validate-config'])
        assert result.exit_code == 0
    
    def test_clone_user_with_options(self):
        """Test clone-user command with options"""
        with patch('cli.UserRepositoryService') as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            
            with patch('cli.GitLabConfig') as mock_gitlab_config:
                mock_gitlab_config.from_config.return_value = Mock()
                
                with patch('cli.RepositoryConfig') as mock_repo_config:
                    mock_repo_config.from_config.return_value = Mock()
                    
                    result = self.runner.invoke(cli, [
                        'clone-user',
                        '--gitlab-url', 'https://gitlab.company.com',
                        '--token', 'custom-token',
                        '--repo-dir', '/custom/path',
                        '--max-workers', '10'
                    ])
                    assert result.exit_code == 0
    
    def test_clone_github_user_with_options(self):
        """Test clone-github-user command with options"""
        with patch('cli.GitHubUserService') as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            
            with patch('cli.GitHubConfig') as mock_github_config:
                mock_github_config.from_config.return_value = Mock()
                
                with patch('cli.RepositoryConfig') as mock_repo_config:
                    mock_repo_config.from_config.return_value = Mock()
                    
                    result = self.runner.invoke(cli, [
                        'clone-github-user',
                        '--username', 'testuser',
                        '--github-url', 'https://api.github.com',
                        '--token', 'custom-token',
                        '--repo-dir', '/custom/path',
                        '--max-workers', '10'
                    ])
                    assert result.exit_code == 0 