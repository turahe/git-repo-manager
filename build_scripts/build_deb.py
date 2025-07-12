#!/usr/bin/env python3
"""
Build script for creating DEB package for Debian/Ubuntu
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def install_dependencies():
    """Install required dependencies for building"""
    print("Installing build dependencies...")
    subprocess.run(["sudo", "apt-get", "update"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "python3-stdeb", "dh-python"], check=True)


def build_deb():
    """Build the DEB package"""
    print("Building DEB package...")
    
    # Create build directory
    build_dir = Path("dist/debian")
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean previous builds
    for item in Path(".").glob("*.deb"):
        item.unlink()
    for item in Path(".").glob("*.tar.gz"):
        item.unlink()
    
    # Build source distribution
    subprocess.run([sys.executable, "setup.py", "sdist"], check=True)
    
    # Convert to DEB
    dist_files = list(Path("dist").glob("*.tar.gz"))
    if not dist_files:
        print("❌ No source distribution found!")
        sys.exit(1)
    
    latest_dist = max(dist_files, key=lambda x: x.stat().st_mtime)
    
    # Extract and build DEB
    subprocess.run(["py2dsc", str(latest_dist)], check=True)
    
    # Build DEB package
    debian_dir = Path("deb_dist/gitlab-repo-manager-1.0.0/debian")
    if debian_dir.exists():
        subprocess.run(["dpkg-buildpackage", "-rfakeroot", "-uc", "-us"], 
                      cwd=debian_dir.parent, check=True)
    
    # Move DEB to dist directory
    for deb_file in Path(".").glob("*.deb"):
        shutil.move(str(deb_file), str(build_dir))
    
    print("✅ DEB package built successfully!")
    print(f"📦 Package location: {build_dir}")


def create_debian_control():
    """Create debian control file"""
    control_content = """Source: gitlab-repo-manager
Section: utils
Priority: optional
Maintainer: Your Name <your.email@example.com>
Build-Depends: debhelper (>= 9), dh-python, python3-all, python3-setuptools

Package: gitlab-repo-manager
Architecture: all
Depends: ${python3:Depends}, ${misc:Depends}
Description: GitLab Repository Management Tool
 A modular CLI tool for managing GitLab repositories and Composer dependencies.
 Features include:
  * Clone user and group repositories
  * Concurrent repository operations
  * Composer dependency management
  * YAML configuration support
  * Environment variable override
"""
    
    debian_dir = Path("debian")
    debian_dir.mkdir(exist_ok=True)
    
    with open(debian_dir / "control", "w") as f:
        f.write(control_content)


if __name__ == "__main__":
    install_dependencies()
    create_debian_control()
    build_deb() 