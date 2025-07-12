from unittest.mock import patch, Mock, MagicMock
from src.services import (
    UserRepositoryService, GroupRepositoryService, ComposerService,
    GitHubUserService, GitHubOrganizationService
)
from src.config import GitLabConfig, RepositoryConfig, GroupConfig, GitHubConfig


class TestUserRepositoryService:
    """Test UserRepositoryService class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.gitlab_config = GitLabConfig(
            url="https://gitlab.com",
            private_token="test-token"
        )
        self.repo_config = RepositoryConfig(
            repo_dir="/test/repos",
            max_concurrent_downloads=5
        )
        self.service = UserRepositoryService(self.gitlab_config, self.repo_config)
    
    def test_service_creation(self):
        """Test creating UserRepositoryService instance"""
        assert self.service.gitlab_client.config == self.gitlab_config
        assert self.service.repo_manager.config == self.repo_config
    
    @patch('src.services.UserRepositoryService._get_executor')
    @patch('src.services.UserRepositoryService._as_completed')
    def test_clone_user_repositories_success(self, mock_as_completed, mock_executor):
        """Test successful clone_user_repositories"""
        # Mock the GitLab client
        mock_projects = [
            {"id": 1, "name": "project1", "http_url_to_repo": "https://gitlab.com/project1.git"},
            {"id": 2, "name": "project2", "http_url_to_repo": "https://gitlab.com/project2.git"}
        ]
        self.service.gitlab_client.get_current_user_id = Mock(return_value=1)
        self.service.gitlab_client.get_user_owned_projects = Mock(return_value=mock_projects)
        
        # Mock the repository manager
        mock_future1 = Mock()
        mock_future1.result.return_value = ("project1", "Cloned project1")
        mock_future2 = Mock()
        mock_future2.result.return_value = ("project2", "Updated project2")
        
        mock_executor.return_value.__enter__.return_value.submit.side_effect = [
            mock_future1, mock_future2
        ]
        mock_as_completed.return_value = [mock_future1, mock_future2]
        
        # Mock futures dictionary
        with patch.object(self.service, '_get_futures_dict', return_value={
            mock_future1: "project1",
            mock_future2: "project2"
        }):
            self.service.clone_user_repositories()
    
    def test_clone_user_repositories_no_projects(self):
        """Test clone_user_repositories with no projects"""
        self.service.gitlab_client.get_current_user_id = Mock(return_value=1)
        self.service.gitlab_client.get_user_owned_projects = Mock(return_value=[])
        
        self.service.clone_user_repositories()


class TestGroupRepositoryService:
    """Test GroupRepositoryService class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.gitlab_config = GitLabConfig(
            url="https://gitlab.com",
            private_token="test-token"
        )
        self.repo_config = RepositoryConfig(
            repo_dir="/test/repos",
            max_concurrent_downloads=5
        )
        self.group_config = GroupConfig(target_group_ids=[1, 2])
        self.service = GroupRepositoryService(self.gitlab_config, self.repo_config, self.group_config)
    
    def test_service_creation(self):
        """Test creating GroupRepositoryService instance"""
        assert self.service.gitlab_client.config == self.gitlab_config
        assert self.service.repo_manager.config == self.repo_config
        assert self.service.group_config == self.group_config
    
    @patch('src.services.GroupRepositoryService._get_executor')
    @patch('src.services.GroupRepositoryService._as_completed')
    def test_clone_group_repositories_success(self, mock_as_completed, mock_executor):
        """Test successful clone_group_repositories"""
        # Mock the GitLab client
        mock_projects = [
            {"id": 1, "name": "group-project1", "http_url_to_repo": "https://gitlab.com/group/project1.git"},
            {"id": 2, "name": "group-project2", "http_url_to_repo": "https://gitlab.com/group/project2.git"}
        ]
        self.service.gitlab_client.get_group_projects = Mock(return_value=mock_projects)
        
        # Mock the repository manager
        mock_future1 = Mock()
        mock_future1.result.return_value = ("group-project1", "Cloned group-project1")
        mock_future2 = Mock()
        mock_future2.result.return_value = ("group-project2", "Updated group-project2")
        
        mock_executor.return_value.__enter__.return_value.submit.side_effect = [
            mock_future1, mock_future2
        ]
        mock_as_completed.return_value = [mock_future1, mock_future2]
        
        # Mock futures dictionary
        with patch.object(self.service, '_get_futures_dict', return_value={
            mock_future1: "group-project1",
            mock_future2: "group-project2"
        }):
            self.service.clone_group_repositories()


class TestGitHubUserService:
    """Test GitHubUserService class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.github_config = GitHubConfig(
            access_token="test-token",
            url="https://api.github.com"
        )
        self.repo_config = RepositoryConfig(
            repo_dir="/test/repos",
            max_concurrent_downloads=5
        )
        self.service = GitHubUserService(self.github_config, self.repo_config)
    
    def test_service_creation(self):
        """Test creating GitHubUserService instance"""
        assert self.service.github_client.config == self.github_config
        assert self.service.repo_manager.config == self.repo_config
    
    @patch('concurrent.futures.ThreadPoolExecutor')
    @patch('concurrent.futures.as_completed')
    def test_clone_user_repositories_success(self, mock_as_completed, mock_executor):
        """Test successful clone_user_repositories"""
        # Mock the GitHub client
        mock_repos = [
            {"id": 1, "full_name": "user/repo1", "clone_url": "https://github.com/user/repo1.git"},
            {"id": 2, "full_name": "user/repo2", "clone_url": "https://github.com/user/repo2.git"}
        ]
        self.service.github_client.get_user_repositories = Mock(return_value=mock_repos)
        
        # Mock the repository manager
        mock_future1 = Mock()
        mock_future1.result.return_value = ("user/repo1", "Cloned user/repo1")
        mock_future2 = Mock()
        mock_future2.result.return_value = ("user/repo2", "Updated user/repo2")
        
        mock_executor_instance = Mock()
        mock_executor_instance.submit.side_effect = [mock_future1, mock_future2]
        mock_executor.return_value.__enter__.return_value = mock_executor_instance
        mock_as_completed.return_value = [mock_future1, mock_future2]
        
        # Mock futures dictionary
        futures_dict = {mock_future1: "user/repo1", mock_future2: "user/repo2"}
        
        with patch.object(self.service.repo_manager, 'clone_or_pull_repo'):
            self.service.clone_user_repositories("testuser")
    
    def test_clone_user_repositories_no_repos(self):
        """Test clone_user_repositories with no repositories"""
        self.service.github_client.get_user_repositories = Mock(return_value=[])
        
        self.service.clone_user_repositories("testuser")


class TestGitHubOrganizationService:
    """Test GitHubOrganizationService class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.github_config = GitHubConfig(
            access_token="test-token",
            url="https://api.github.com"
        )
        self.repo_config = RepositoryConfig(
            repo_dir="/test/repos",
            max_concurrent_downloads=5
        )
        self.service = GitHubOrganizationService(self.github_config, self.repo_config)
    
    def test_service_creation(self):
        """Test creating GitHubOrganizationService instance"""
        assert self.service.github_client.config == self.github_config
        assert self.service.repo_manager.config == self.repo_config
    
    @patch('concurrent.futures.ThreadPoolExecutor')
    @patch('concurrent.futures.as_completed')
    def test_clone_organization_repositories_success(self, mock_as_completed, mock_executor):
        """Test successful clone_organization_repositories"""
        # Mock the GitHub client
        mock_repos = [
            {"id": 1, "full_name": "org/repo1", "clone_url": "https://github.com/org/repo1.git"},
            {"id": 2, "full_name": "org/repo2", "clone_url": "https://github.com/org/repo2.git"}
        ]
        self.service.github_client.get_organization_repositories = Mock(return_value=mock_repos)
        
        # Mock the repository manager
        mock_future1 = Mock()
        mock_future1.result.return_value = ("org/repo1", "Cloned org/repo1")
        mock_future2 = Mock()
        mock_future2.result.return_value = ("org/repo2", "Updated org/repo2")
        
        mock_executor_instance = Mock()
        mock_executor_instance.submit.side_effect = [mock_future1, mock_future2]
        mock_executor.return_value.__enter__.return_value = mock_executor_instance
        mock_as_completed.return_value = [mock_future1, mock_future2]
        
        # Mock futures dictionary
        futures_dict = {mock_future1: "org/repo1", mock_future2: "org/repo2"}
        
        with patch.object(self.service.repo_manager, 'clone_or_pull_repo'):
            self.service.clone_organization_repositories("testorg")
    
    def test_clone_organization_repositories_no_repos(self):
        """Test clone_organization_repositories with no repositories"""
        self.service.github_client.get_organization_repositories = Mock(return_value=[])
        
        self.service.clone_organization_repositories("testorg")


class TestComposerService:
    """Test ComposerService class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.service = ComposerService()
    
    def test_service_creation(self):
        """Test creating ComposerService instance"""
        assert self.service.composer_manager is not None
    
    @patch('src.services.ComposerManager.find_and_update_composer')
    def test_update_composer_dependencies(self, mock_find_and_update):
        """Test update_composer_dependencies"""
        self.service.update_composer_dependencies("/test/directory")
        mock_find_and_update.assert_called_once_with("/test/directory") 