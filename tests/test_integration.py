import pytest
from unittest.mock import patch, Mock
from src.config import GitLabConfig, GitHubConfig, RepositoryConfig
from src.gitlab_client import GitLabClient
from src.github_client import GitHubClient
from src.services import UserRepositoryService, GitHubUserService


class TestIntegration:
    """Integration tests for the application"""
    
    @pytest.mark.integration
    def test_gitlab_client_integration(self):
        """Test GitLab client integration with mocked API"""
        config = GitLabConfig(
            url="https://gitlab.com",
            private_token="test-token"
        )
        client = GitLabClient(config)
        
        # Test that client can be created and configured
        assert client.config == config
        assert "Private-Token" in client.headers
        assert client.headers["Private-Token"] == "test-token"
    
    @pytest.mark.integration
    def test_github_client_integration(self):
        """Test GitHub client integration with mocked API"""
        config = GitHubConfig(
            access_token="test-token",
            url="https://api.github.com"
        )
        client = GitHubClient(config)
        
        # Test that client can be created and configured
        assert client.config == config
        assert "Authorization" in client.headers
        assert "token test-token" in client.headers["Authorization"]
    
    @pytest.mark.integration
    def test_user_repository_service_integration(self):
        """Test UserRepositoryService integration"""
        gitlab_config = GitLabConfig(
            url="https://gitlab.com",
            private_token="test-token"
        )
        repo_config = RepositoryConfig(
            repo_dir="/test/repos",
            max_concurrent_downloads=5
        )
        
        service = UserRepositoryService(gitlab_config, repo_config)
        
        # Test that service can be created with proper components
        assert service.gitlab_client.config == gitlab_config
        assert service.repo_manager.config == repo_config
    
    @pytest.mark.integration
    def test_github_user_service_integration(self):
        """Test GitHubUserService integration"""
        github_config = GitHubConfig(
            access_token="test-token",
            url="https://api.github.com"
        )
        repo_config = RepositoryConfig(
            repo_dir="/test/repos",
            max_concurrent_downloads=5
        )
        
        service = GitHubUserService(github_config, repo_config)
        
        # Test that service can be created with proper components
        assert service.github_client.config == github_config
        assert service.repo_manager.config == repo_config
    
    @pytest.mark.integration
    def test_configuration_integration(self):
        """Test configuration integration"""
        # Test GitLab configuration
        gitlab_config = GitLabConfig.from_env()
        assert hasattr(gitlab_config, 'url')
        assert hasattr(gitlab_config, 'private_token')
        
        # Test GitHub configuration
        github_config = GitHubConfig.from_env()
        assert hasattr(github_config, 'url')
        assert hasattr(github_config, 'access_token')
        
        # Test Repository configuration
        repo_config = RepositoryConfig.from_env()
        assert hasattr(repo_config, 'repo_dir')
        assert hasattr(repo_config, 'max_concurrent_downloads')
    
    @pytest.mark.integration
    @patch('src.gitlab_client.requests.get')
    def test_gitlab_api_integration(self, mock_get):
        """Test GitLab API integration with mocked responses"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "username": "testuser"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        config = GitLabConfig(
            url="https://gitlab.com",
            private_token="test-token"
        )
        client = GitLabClient(config)
        
        # Test API call
        user_id = client.get_current_user_id()
        assert user_id == 1
    
    @pytest.mark.integration
    @patch('src.github_client.requests.get')
    def test_github_api_integration(self, mock_get):
        """Test GitHub API integration with mocked responses"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "login": "testuser"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        config = GitHubConfig(
            access_token="test-token",
            url="https://api.github.com"
        )
        client = GitHubClient(config)
        
        # Test API call
        user = client.get_current_user()
        assert user["id"] == 1
        assert user["login"] == "testuser"
    
    @pytest.mark.integration
    def test_service_orchestration_integration(self):
        """Test service orchestration integration"""
        # Test GitLab service orchestration
        gitlab_config = GitLabConfig(
            url="https://gitlab.com",
            private_token="test-token"
        )
        repo_config = RepositoryConfig(
            repo_dir="/test/repos",
            max_concurrent_downloads=5
        )
        
        gitlab_service = UserRepositoryService(gitlab_config, repo_config)
        assert gitlab_service is not None
        
        # Test GitHub service orchestration
        github_config = GitHubConfig(
            access_token="test-token",
            url="https://api.github.com"
        )
        
        github_service = GitHubUserService(github_config, repo_config)
        assert github_service is not None 