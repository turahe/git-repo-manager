from unittest.mock import patch, Mock
from src.github_client import GitHubClient
from src.config import GitHubConfig
import pytest


class TestGitHubClient:
    """Test GitHubClient class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.config = GitHubConfig(
            access_token="test-token",
            url="https://api.github.com"
        )
        self.client = GitHubClient(self.config)
    
    def test_github_client_creation(self):
        """Test creating GitHubClient instance"""
        assert self.client.config == self.config
        assert "Authorization" in self.client.headers
        assert "token test-token" in self.client.headers["Authorization"]
        assert "Accept" in self.client.headers
        assert "application/vnd.github.v3+json" in self.client.headers["Accept"]
    
    def test_get_current_user_success(self):
        """Test successful get_current_user call"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 1,
            "login": "testuser",
            "name": "Test User"
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.get', return_value=mock_response):
            user = self.client.get_current_user()
            assert user["id"] == 1
            assert user["login"] == "testuser"
            assert user["name"] == "Test User"
    
    def test_get_current_user_authentication_error(self):
        """Test get_current_user with authentication error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(SystemExit):
                self.client.get_current_user()
    
    def test_get_user_repositories_success(self):
        """Test successful get_user_repositories call"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "full_name": "user/repo1", "clone_url": "https://github.com/user/repo1.git"},
            {"id": 2, "full_name": "user/repo2", "clone_url": "https://github.com/user/repo2.git"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_response.links = {}
        
        with patch('requests.get', return_value=mock_response):
            repos = self.client.get_user_repositories("testuser")
            assert len(repos) == 2
            assert repos[0]["full_name"] == "user/repo1"
            assert repos[1]["full_name"] == "user/repo2"
    
    def test_get_user_repositories_pagination(self):
        """Test get_user_repositories with pagination"""
        # First page response
        mock_response1 = Mock()
        mock_response1.json.return_value = [{"id": 1, "full_name": "user/repo1"}]
        mock_response1.raise_for_status.return_value = None
        mock_response1.links = {"next": {"url": "https://api.github.com/users/testuser/repos?page=2"}}
        
        # Second page response
        mock_response2 = Mock()
        mock_response2.json.return_value = [{"id": 2, "full_name": "user/repo2"}]
        mock_response2.raise_for_status.return_value = None
        mock_response2.links = {}
        
        with patch('requests.get', side_effect=[mock_response1, mock_response2]):
            repos = self.client.get_user_repositories("testuser")
            assert len(repos) == 2
            assert repos[0]["full_name"] == "user/repo1"
            assert repos[1]["full_name"] == "user/repo2"
    
    def test_get_user_repositories_not_found(self):
        """Test get_user_repositories with user not found"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        
        with patch('requests.get', return_value=mock_response):
            repos = self.client.get_user_repositories("nonexistent")
            assert repos == []
    
    def test_get_organization_repositories_success(self):
        """Test successful get_organization_repositories call"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "full_name": "org/repo1", "clone_url": "https://github.com/org/repo1.git"},
            {"id": 2, "full_name": "org/repo2", "clone_url": "https://github.com/org/repo2.git"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_response.links = {}
        
        with patch('requests.get', return_value=mock_response):
            repos = self.client.get_organization_repositories("testorg")
            assert len(repos) == 2
            assert repos[0]["full_name"] == "org/repo1"
            assert repos[1]["full_name"] == "org/repo2"
    
    def test_get_organization_repositories_not_found(self):
        """Test get_organization_repositories with organization not found"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        
        with patch('requests.get', return_value=mock_response):
            repos = self.client.get_organization_repositories("nonexistent")
            assert repos == []
    
    def test_get_authenticated_user_repositories_success(self):
        """Test successful get_authenticated_user_repositories call"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "full_name": "user/repo1", "clone_url": "https://github.com/user/repo1.git"},
            {"id": 2, "full_name": "user/repo2", "clone_url": "https://github.com/user/repo2.git"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_response.links = {}
        
        with patch('requests.get', return_value=mock_response):
            repos = self.client.get_authenticated_user_repositories()
            assert len(repos) == 2
            assert repos[0]["full_name"] == "user/repo1"
            assert repos[1]["full_name"] == "user/repo2"
    
    def test_get_authenticated_user_repositories_authentication_error(self):
        """Test get_authenticated_user_repositories with authentication error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
        
        with patch('requests.get', return_value=mock_response):
            repos = self.client.get_authenticated_user_repositories()
            assert repos == []
    
    def test_request_exception_handling(self):
        """Test handling of request exceptions"""
        with patch('requests.get', side_effect=Exception("Network error")):
            repos = self.client.get_user_repositories("testuser")
            assert repos == [] 