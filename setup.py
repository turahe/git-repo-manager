from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gitlab-repo-manager",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A modular CLI tool for managing GitLab repositories and Composer dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gitlab-repo-manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gitlab-repo-manager=cli:cli",
        ],
    },
    keywords="gitlab, repository, composer, cli, management",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/gitlab-repo-manager/issues",
        "Source": "https://github.com/yourusername/gitlab-repo-manager",
    },
) 