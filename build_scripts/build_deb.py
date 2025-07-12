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
        print("ERROR: No source distribution found!")
        sys.exit(1)
    
    latest_dist = max(dist_files, key=lambda x: x.stat().st_mtime)
    print(f"Using source distribution: {latest_dist}")
    
    # Extract and build DEB
    try:
        subprocess.run(["py2dsc", str(latest_dist)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to convert to DEB format: {e}")
        print("This might be due to stdeb compatibility issues with Python 3.12")
        sys.exit(1)
    
    # Build DEB package
    debian_dir = Path("deb_dist/git-repo-manager-1.0.0/debian")
    if debian_dir.exists():
        try:
            subprocess.run(["dpkg-buildpackage", "-rfakeroot", "-uc", "-us"], 
                          cwd=debian_dir.parent, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to build DEB package: {e}")
            sys.exit(1)
    else:
        print(f"ERROR: Debian directory not found at {debian_dir}")
        sys.exit(1)
    
    # Move DEB to dist directory
    deb_files = list(Path(".").glob("*.deb"))
    if deb_files:
        for deb_file in deb_files:
            shutil.move(str(deb_file), str(build_dir))
        print("SUCCESS: DEB package built successfully!")
        print(f"PACKAGE: Package location: {build_dir}")
    else:
        print("ERROR: No DEB files were created!")
        sys.exit(1)


def create_debian_control():
    """Create debian control file"""
    control_content = """Source: git-repo-manager
Section: utils
Priority: optional
Maintainer: Nur Wachid <wachid@outlook.com>
Build-Depends: debhelper (>= 9), dh-python, python3-all, python3-setuptools

Package: git-repo-manager
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