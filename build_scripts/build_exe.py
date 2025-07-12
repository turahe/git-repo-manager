#!/usr/bin/env python3
"""
Build script for creating Windows EXE using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def install_dependencies():
    """Install required dependencies for building"""
    print("Installing build dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)


def build_exe():
    """Build the Windows EXE"""
    print("Building Windows EXE...")
    
    # Create build directory
    build_dir = Path("dist/windows")
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Get absolute paths for data files
    current_dir = Path.cwd()
    config_example = current_dir / "config.example.yml"
    readme = current_dir / "README.md"
    
    # Verify files exist
    if not config_example.exists():
        print(f"ERROR: config.example.yml not found at {config_example}")
        sys.exit(1)
    
    if not readme.exists():
        print(f"ERROR: README.md not found at {readme}")
        sys.exit(1)
    
    # PyInstaller command with absolute paths
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=git-repo-manager",
        "--distpath=dist/windows",
        "--workpath=build/windows",
        "--specpath=build/windows",
        f"--add-data={config_example};.",
        f"--add-data={readme};.",
        "--hidden-import=click",
        "--hidden-import=yaml",
        "--hidden-import=requests",
        "cli.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("SUCCESS: Windows EXE built successfully!")
        print(f"PACKAGE: Executable location: {build_dir / 'git-repo-manager.exe'}")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Error building Windows EXE: {e}")
        sys.exit(1)


def create_windows_package():
    """Create a Windows package with dependencies"""
    print("Creating Windows package...")
    
    package_dir = Path("dist/windows/package")
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy executable
    exe_path = Path("dist/windows/git-repo-manager.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, package_dir)
    
    # Copy config example
    config_example = Path("config.example.yml")
    if config_example.exists():
        shutil.copy2(config_example, package_dir)
    
    # Copy README
    readme = Path("README.md")
    if readme.exists():
        shutil.copy2(readme, package_dir)
    
    # Create batch file for easy execution
    batch_content = """@echo off
echo GitLab Repository Manager
echo ========================
git-repo-manager.exe %*
"""
    with open(package_dir / "run.bat", "w") as f:
        f.write(batch_content)
    
    print("SUCCESS: Windows package created!")


if __name__ == "__main__":
    install_dependencies()
    build_exe()
    create_windows_package() 