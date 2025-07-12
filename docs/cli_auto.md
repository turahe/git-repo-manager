# CLI Reference

This documentation is auto-generated from the CLI commands.

## Global Help

```bash
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

  GitLab Repository Management Tool

  A modular CLI tool for managing GitLab repositories and Composer
  dependencies.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  clone-all          Clone all repositories and optionally update...
  clone-github-org   Clone repositories from a GitHub organization
  clone-github-user  Clone repositories from a GitHub user
  clone-groups       Clone all repositories from specified GitLab groups
  clone-user         Clone all repositories owned by the authenticated user
  config-info        Show information about the configuration file
  init-config        Initialize configuration file in user's home directory
  update-composer    Update Composer dependencies in all projects
  validate-config    Validate the configuration file

```

## init-config

```bash
Usage: cli.py init-config [OPTIONS]

  Initialize configuration file in user's home directory

Options:
  --force            Overwrite existing config file
  --non-interactive  Use default values without prompting
  --help             Show this message and exit.

```

## validate-config

```bash
Usage: cli.py validate-config [OPTIONS]

  Validate the configuration file

Options:
  --help  Show this message and exit.

```

## config-info

```bash
Usage: cli.py config-info [OPTIONS]

  Show information about the configuration file

Options:
  --help  Show this message and exit.

```

## clone-user

```bash
Usage: cli.py clone-user [OPTIONS]

  Clone all repositories owned by the authenticated user

Options:
  --gitlab-url TEXT      GitLab instance URL (overrides config)
  --token TEXT           GitLab Personal Access Token (overrides config)
  --repo-dir TEXT        Directory to save repositories (overrides config)
  --max-workers INTEGER  Maximum concurrent downloads (overrides config)
  --output-dir TEXT      Custom output directory for cloned repositories
  --help                 Show this message and exit.

```

## clone-groups

```bash
Usage: cli.py clone-groups [OPTIONS]

  Clone all repositories from specified GitLab groups

Options:
  --gitlab-url TEXT      GitLab instance URL (overrides config)
  --token TEXT           GitLab Personal Access Token (overrides config)
  --repo-dir TEXT        Directory to save repositories (overrides config)
  --max-workers INTEGER  Maximum concurrent downloads (overrides config)
  --group-ids INTEGER    GitLab group IDs to clone from (overrides config)
  --output-dir TEXT      Custom output directory for cloned repositories
  --help                 Show this message and exit.

```

## clone-github-user

```bash
Usage: cli.py clone-github-user [OPTIONS]

  Clone repositories from a GitHub user

Options:
  --github-url TEXT      GitHub API URL (overrides config)
  --token TEXT           GitHub Access Token (overrides config)
  --repo-dir TEXT        Directory to save repositories (overrides config)
  --max-workers INTEGER  Maximum concurrent downloads (overrides config)
  --username TEXT        GitHub username to clone from (optional)
  --output-dir TEXT      Custom output directory for cloned repositories
  --help                 Show this message and exit.

```

## clone-github-org

```bash
Usage: cli.py clone-github-org [OPTIONS] ORGANIZATION

  Clone repositories from a GitHub organization

Options:
  --github-url TEXT      GitHub API URL (overrides config)
  --token TEXT           GitHub Access Token (overrides config)
  --repo-dir TEXT        Directory to save repositories (overrides config)
  --max-workers INTEGER  Maximum concurrent downloads (overrides config)
  --output-dir TEXT      Custom output directory for cloned repositories
  --help                 Show this message and exit.

```

## update-composer

```bash
Usage: cli.py update-composer [OPTIONS]

  Update Composer dependencies in all projects

Options:
  --directory TEXT  Directory to search for composer.json files
  --help            Show this message and exit.

```
