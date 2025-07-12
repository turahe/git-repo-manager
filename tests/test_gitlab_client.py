import pytest
from unittest.mock import patch, Mock
from src.gitlab_client import GitLabClient
from src.config import GitLabConfig


class TestGitLabClient:
    """Test GitLabClient class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.config = GitLabConfig(
            url="https://gitlab.com",
            private_token="test-token"
        )
        self.client = GitLabClient(self.config)
    
    def test_gitlab_client_creation(self):
        """Test creating GitLabClient instance"""
        assert self.client.config == self.config
        assert "Private-Token" in self.client.headers
        assert "test-token" in self.client.headers["Private-Token"]
    
    def test_get_current_user_id_success(self):
        """Test successful get_current_user_id call"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 1,
            "username": "testuser",
            "name": "Test User"
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.get', return_value=mock_response):
            user_id = self.client.get_current_user_id()
            assert user_id == 1
    
    def test_get_current_user_id_authentication_error(self):
        """Test get_current_user_id with authentication error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(SystemExit):
                self.client.get_current_user_id()
    
    def test_get_user_owned_projects_success(self):
        """Test successful get_user_owned_projects call"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "project1", "http_url_to_repo": "https://gitlab.com/project1.git"},
            {"id": 2, "name": "project2", "http_url_to_repo": "https://gitlab.com/project2.git"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {}
        
        with patch('requests.get', return_value=mock_response):
            projects = self.client.get_user_owned_projects(1)
            assert len(projects) == 2
            assert projects[0]["name"] == "project1"
            assert projects[1]["name"] == "project2"
    
    def test_get_user_owned_projects_pagination(self):
        """Test get_user_owned_projects with pagination"""
        # First page response
        mock_response1 = Mock()
        mock_response1.json.return_value = [{"id": 1, "name": "project1"}]
        mock_response1.raise_for_status.return_value = None
        mock_response1.headers = {"X-Next-Page": "2"}
        
        # Second page response
        mock_response2 = Mock()
        mock_response2.json.return_value = [{"id": 2, "name": "project2"}]
        mock_response2.raise_for_status.return_value = None
        mock_response2.headers = {}
        
        with patch('requests.get', side_effect=[mock_response1, mock_response2]):
            projects = self.client.get_user_owned_projects(1)
            assert len(projects) == 2
            assert projects[0]["name"] == "project1"
            assert projects[1]["name"] == "project2"
    
    def test_get_user_owned_projects_authentication_error(self):
        """Test get_user_owned_projects with authentication error"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(SystemExit):
                self.client.get_user_owned_projects(1)
    
    def test_get_group_projects_success(self):
        """Test successful get_group_projects call"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "name": "group-project1", "http_url_to_repo": "https://gitlab.com/group/project1.git"},
            {"id": 2, "name": "group-project2", "http_url_to_repo": "https://gitlab.com/group/project2.git"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {}
        
        with patch('requests.get', return_value=mock_response):
            projects = self.client.get_group_projects(123)
            assert len(projects) == 2
            assert projects[0]["name"] == "group-project1"
            assert projects[1]["name"] == "group-project2"
    
    def test_get_group_projects_not_found(self):
        """Test get_group_projects with group not found"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        
        with patch('requests.get', return_value=mock_response):
            projects = self.client.get_group_projects(999)
            assert projects == []
    
    def test_get_group_projects_forbidden(self):
        """Test get_group_projects with forbidden access"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = Exception("403 Forbidden")
        
        with patch('requests.get', return_value=mock_response):
            projects = self.client.get_group_projects(123)
            assert projects == []
    
    def test_get_group_projects_request_exception(self):
        """Test handling of request exceptions in get_group_projects"""
        with patch('requests.get', side_effect=Exception("Network error")):
            projects = self.client.get_group_projects(123)
            assert projects == [] 