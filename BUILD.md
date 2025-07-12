# Build Documentation

This document explains how to build different package types for the GitLab Repository Manager.

## Prerequisites

### For Windows EXE
- Python 3.7+
- PyInstaller (installed automatically)

### For DEB Package (Debian/Ubuntu)
- Python 3.7+
- `python3-stdeb`
- `dh-python`
- `dpkg-buildpackage`

### For RPM Package (Red Hat/CentOS/Fedora)
- Python 3.7+
- `rpm-build`
- `python3-setuptools`

## Quick Start

### Build for Current Platform
```bash
# Install dependencies
make install

# Build for current platform
make build
```

### Build Specific Package Type
```bash
# Windows EXE
make build-windows

# DEB package
make build-debian

# RPM package
make build-rpm

# All packages
make build-all
```

## Manual Build Commands

### Windows EXE
```bash
python build_scripts/build_exe.py
```

### DEB Package
```bash
python build_scripts/build_deb.py
```

### RPM Package
```bash
python build_scripts/build_rpm.py
```

### All Packages
```bash
python build_scripts/build_all.py
```

## Build Output

### Windows
- **Location**: `dist/windows/`
- **Files**: 
  - `git-repo-manager.exe` - Main executable
  - `package/` - Complete package with dependencies

### DEB Package
- **Location**: `dist/debian/`
- **Files**: `git-repo-manager_*.deb`

### RPM Package
- **Location**: `dist/rpm/`
- **Files**: `git-repo-manager-*.rpm`

## Platform-Specific Instructions

### Windows
1. Install Python 3.7+
2. Run: `python build_scripts/build_exe.py`
3. Find executable in `dist/windows/`

### Ubuntu/Debian
```bash
# Install build dependencies
sudo apt-get update
sudo apt-get install python3-stdeb dh-python

# Build package
python build_scripts/build_deb.py

# Install package
sudo dpkg -i dist/debian/git-repo-manager_*.deb
```

### CentOS/RHEL/Fedora
```bash
# Install build dependencies
sudo yum install rpm-build python3-setuptools

# Build package
python build_scripts/build_rpm.py

# Install package
sudo rpm -i dist/rpm/git-repo-manager-*.rpm
```

## Troubleshooting

### Common Issues

#### PyInstaller Issues (Windows)
```bash
# Reinstall PyInstaller
pip uninstall pyinstaller
pip install pyinstaller

# Clear cache
rm -rf build/ dist/
```

#### DEB Build Issues
```bash
# Install missing dependencies
sudo apt-get install build-essential python3-dev

# Clean and rebuild
make clean
python build_scripts/build_deb.py
```

#### RPM Build Issues
```bash
# Install missing dependencies
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel

# Clean and rebuild
make clean
python build_scripts/build_rpm.py
```

### Build Environment

#### Docker for Cross-Platform Building
```bash
# Ubuntu/Debian container
docker run -it --rm -v $(pwd):/app ubuntu:20.04
apt-get update && apt-get install -y python3 python3-pip
cd /app && python3 build_scripts/build_deb.py

# CentOS container
docker run -it --rm -v $(pwd):/app centos:8
yum install -y python3 python3-pip
cd /app && python3 build_scripts/build_rpm.py
```

## Package Contents

### Windows EXE Package
- `git-repo-manager.exe` - Main executable
- `config.example.yml` - Example configuration
- `README.md` - Documentation
- `run.bat` - Convenience script

### DEB Package
- Binary executable in `/usr/bin/`
- Python modules in `/usr/lib/python3/dist-packages/`
- Documentation in `/usr/share/doc/`
- Configuration example in `/usr/share/doc/`

### RPM Package
- Binary executable in `/usr/bin/`
- Python modules in `/usr/lib/python3/site-packages/`
- Documentation in `/usr/share/doc/`
- Configuration example in `/usr/share/doc/`

## Version Management

### Update Version
1. Edit `setup.py` - Update version number
2. Edit `src/config.py` - Update version in ConfigManager
3. Update package spec files if needed
4. Rebuild packages

### Release Process
```bash
# Clean previous builds
make clean

# Build all packages
make build-all

# Test packages
# Windows: Run executable
# Linux: Install and test packages

# Create release
# Tag git repository
# Upload packages to release
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Build Packages

on: [push, pull_request]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: python build_scripts/build_exe.py

  build-debian:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: python build_scripts/build_deb.py

  build-rpm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: python build_scripts/build_rpm.py
``` 