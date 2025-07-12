#!/usr/bin/env python3
"""
GitLab Repository Management CLI Tool

A modular, object-oriented CLI tool for managing GitLab repositories and Composer dependencies.
"""

import click
import os
from src.config import GitLabConfig, RepositoryConfig, GroupConfig, ComposerConfig, GitHubConfig
from src.services import UserRepositoryService, GroupRepositoryService, ComposerService, GitHubUserService, GitHubOrganizationService
from src.config_generator import ConfigGenerator


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """GitLab Repository Management Tool
    
    A modular CLI tool for managing GitLab repositories and Composer dependencies.
    """
    pass


@cli.command()
@click.option('--gitlab-url', help='GitLab instance URL (overrides config)')
@click.option('--token', envvar='GITLAB_PRIVATE_TOKEN', help='GitLab Personal Access Token (overrides config)')
@click.option('--repo-dir', help='Directory to save repositories (overrides config)')
@click.option('--max-workers', type=int, help='Maximum concurrent downloads (overrides config)')
@click.option('--output-dir', help='Custom output directory for cloned repositories')
def clone_user(gitlab_url, token, repo_dir, max_workers, output_dir):
    """Clone all repositories owned by the authenticated user"""
    click.echo("🚀 Starting user repository cloning process...")
    
    # Initialize configurations from config file
    gitlab_config = GitLabConfig.from_config()
    repo_config = RepositoryConfig.from_config()
    
    # Override with command line options if provided
    if gitlab_url:
        gitlab_config.url = gitlab_url
    if token:
        gitlab_config.private_token = token
    if repo_dir:
        repo_config.repo_dir = repo_dir
    if max_workers:
        repo_config.max_concurrent_downloads = max_workers
    
    # Create and run service
    service = UserRepositoryService(gitlab_config, repo_config)
    service.clone_user_repositories(output_dir=output_dir)


@cli.command()
@click.option('--gitlab-url', help='GitLab instance URL (overrides config)')
@click.option('--token', envvar='GITLAB_PRIVATE_TOKEN', help='GitLab Personal Access Token (overrides config)')
@click.option('--repo-dir', help='Directory to save repositories (overrides config)')
@click.option('--max-workers', type=int, help='Maximum concurrent downloads (overrides config)')
@click.option('--group-ids', multiple=True, type=int, help='GitLab group IDs to clone from (overrides config)')
@click.option('--output-dir', help='Custom output directory for cloned repositories')
def clone_groups(gitlab_url, token, repo_dir, max_workers, group_ids, output_dir):
    """Clone all repositories from specified GitLab groups"""
    click.echo("🚀 Starting group repository cloning process...")
    
    # Initialize configurations from config file
    gitlab_config = GitLabConfig.from_config()
    repo_config = RepositoryConfig.from_config()
    group_config = GroupConfig.from_config()
    
    # Override with command line options if provided
    if gitlab_url:
        gitlab_config.url = gitlab_url
    if token:
        gitlab_config.private_token = token
    if repo_dir:
        repo_config.repo_dir = repo_dir
    if max_workers:
        repo_config.max_concurrent_downloads = max_workers
    if group_ids:
        group_config.target_group_ids = list(group_ids)
    
    # Create and run service
    service = GroupRepositoryService(gitlab_config, repo_config, group_config)
    service.clone_group_repositories(output_dir=output_dir)


@cli.command()
@click.option('--directory', default=os.getcwd(), help='Directory to search for composer.json files')
def update_composer(directory):
    """Update Composer dependencies in all projects"""
    click.echo("🔧 Starting Composer dependency update process...")
    
    # Create and run service
    service = ComposerService()
    service.update_composer_dependencies(directory)


@cli.command()
@click.option('--force', is_flag=True, help='Overwrite existing config file')
@click.option('--non-interactive', is_flag=True, help='Use default values without prompting')
def init_config(force, non_interactive):
    """Initialize configuration file in user's home directory"""
    click.echo("⚙️  Initializing configuration...")
    
    generator = ConfigGenerator()
    try:
        success = generator.generate_config(force=force, interactive=not non_interactive)
        
        if success:
            if non_interactive:
                click.echo("\n📋 Next steps:")
                click.echo("1. Edit the config file with your GitLab token")
                click.echo("2. Update group IDs as needed")
                click.echo("3. Run 'git-repo-manager clone-groups' to start cloning")
            else:
                click.echo("\n✅ Configuration completed successfully!")
                click.echo("You can now run 'git-repo-manager clone-groups' to start cloning")
    except ValueError as e:
        click.echo(f"❌ {e}")
        return


@cli.command()
def config_info():
    """Show information about the configuration file"""
    click.echo("📁 Configuration Information")
    click.echo("=" * 30)
    
    generator = ConfigGenerator()
    generator.show_config_info()


@cli.command()
def validate_config():
    """Validate the configuration file"""
    click.echo("🔍 Validating configuration...")
    
    generator = ConfigGenerator()
    is_valid = generator.validate_config()
    
    if is_valid:
        click.echo("✅ Configuration is ready to use!")
    else:
        click.echo("❌ Please fix the configuration issues above")


@cli.command()
@click.option('--github-url', help='GitHub API URL (overrides config)')
@click.option('--token', envvar='GITHUB_ACCESS_TOKEN', help='GitHub Access Token (overrides config)')
@click.option('--repo-dir', help='Directory to save repositories (overrides config)')
@click.option('--max-workers', type=int, help='Maximum concurrent downloads (overrides config)')
@click.option('--username', help='GitHub username to clone from (optional)')
@click.option('--output-dir', help='Custom output directory for cloned repositories')
def clone_github_user(github_url, token, repo_dir, max_workers, username, output_dir):
    """Clone repositories from a GitHub user"""
    click.echo("🚀 Starting GitHub user repository cloning process...")
    
    # Initialize configurations from config file
    github_config = GitHubConfig.from_config()
    repo_config = RepositoryConfig.from_config()
    
    # Override with command line options if provided
    if github_url:
        github_config.url = github_url
    if token:
        github_config.access_token = token
    if repo_dir:
        repo_config.repo_dir = repo_dir
    if max_workers:
        repo_config.max_concurrent_downloads = max_workers
    
    # Create and run service
    service = GitHubUserService(github_config, repo_config)
    service.clone_user_repositories(username, output_dir=output_dir)


@cli.command()
@click.option('--github-url', help='GitHub API URL (overrides config)')
@click.option('--token', envvar='GITHUB_ACCESS_TOKEN', help='GitHub Access Token (overrides config)')
@click.option('--repo-dir', help='Directory to save repositories (overrides config)')
@click.option('--max-workers', type=int, help='Maximum concurrent downloads (overrides config)')
@click.option('--output-dir', help='Custom output directory for cloned repositories')
@click.argument('organization', required=True)
def clone_github_org(github_url, token, repo_dir, max_workers, output_dir, organization):
    """Clone repositories from a GitHub organization"""
    click.echo("🚀 Starting GitHub organization repository cloning process...")
    
    # Initialize configurations from config file
    github_config = GitHubConfig.from_config()
    repo_config = RepositoryConfig.from_config()
    
    # Override with command line options if provided
    if github_url:
        github_config.url = github_url
    if token:
        github_config.access_token = token
    if repo_dir:
        repo_config.repo_dir = repo_dir
    if max_workers:
        repo_config.max_concurrent_downloads = max_workers
    
    # Create and run service
    service = GitHubOrganizationService(github_config, repo_config)
    service.clone_organization_repositories(organization, output_dir=output_dir)


@cli.command()
@click.option('--gitlab-url', help='GitLab instance URL (overrides config)')
@click.option('--token', envvar='GITLAB_PRIVATE_TOKEN', help='GitLab Personal Access Token (overrides config)')
@click.option('--repo-dir', help='Directory to save repositories (overrides config)')
@click.option('--max-workers', type=int, help='Maximum concurrent downloads (overrides config)')
@click.option('--group-ids', multiple=True, type=int, help='GitLab group IDs to clone from (overrides config)')
@click.option('--update-composer', is_flag=True, help='Update Composer dependencies after cloning')
@click.option('--output-dir', help='Custom output directory for cloned repositories')
def clone_all(gitlab_url, token, repo_dir, max_workers, group_ids, update_composer, output_dir):
    """Clone all repositories and optionally update Composer dependencies"""
    click.echo("🚀 Starting complete repository management process...")
    
    # Initialize configurations from config file
    gitlab_config = GitLabConfig.from_config()
    repo_config = RepositoryConfig.from_config()
    group_config = GroupConfig.from_config()
    composer_config = ComposerConfig.from_config()
    
    # Override with command line options if provided
    if gitlab_url:
        gitlab_config.url = gitlab_url
    if token:
        gitlab_config.private_token = token
    if repo_dir:
        repo_config.repo_dir = repo_dir
    if max_workers:
        repo_config.max_concurrent_downloads = max_workers
    if group_ids:
        group_config.target_group_ids = list(group_ids)
    
    # Clone user repositories
    click.echo("\n📦 Cloning user repositories...")
    user_service = UserRepositoryService(gitlab_config, repo_config)
    user_service.clone_user_repositories(output_dir=output_dir)
    
    # Clone group repositories
    click.echo("\n📦 Cloning group repositories...")
    group_service = GroupRepositoryService(gitlab_config, repo_config, group_config)
    group_service.clone_group_repositories(output_dir=output_dir)
    
    # Update Composer dependencies if requested or auto-update is enabled
    if update_composer or composer_config.auto_update:
        click.echo("\n🔧 Updating Composer dependencies...")
        composer_service = ComposerService()
        composer_service.update_composer_dependencies(repo_config.repo_dir)
    
    click.echo("\n✅ Complete repository management process finished!")


if __name__ == '__main__':
    cli()
