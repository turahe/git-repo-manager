#!/usr/bin/env python3
"""
Build script for creating RPM package for Red Hat/CentOS/Fedora
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def install_dependencies():
    """Install required dependencies for building"""
    print("Installing build dependencies...")
    subprocess.run(["sudo", "yum", "install", "-y", "rpm-build", "python3-setuptools"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "rpmvenv"], check=True)


def build_rpm():
    """Build the RPM package"""
    print("Building RPM package...")
    
    # Create build directory
    build_dir = Path("dist/rpm")
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean previous builds
    for item in Path(".").glob("*.rpm"):
        item.unlink()
    for item in Path(".").glob("*.tar.gz"):
        item.unlink()
    
    # Build source distribution
    subprocess.run([sys.executable, "setup.py", "sdist"], check=True)
    
    # Create RPM spec file
    create_rpm_spec()
    
    # Build RPM
    dist_files = list(Path("dist").glob("*.tar.gz"))
    if not dist_files:
        print("❌ No source distribution found!")
        sys.exit(1)
    
    latest_dist = max(dist_files, key=lambda x: x.stat().st_mtime)
    
    # Build RPM
    subprocess.run(["rpmbuild", "-ta", str(latest_dist)], check=True)
    
    # Move RPM to dist directory
    rpm_dir = Path.home() / "rpmbuild/RPMS/noarch"
    if rpm_dir.exists():
        for rpm_file in rpm_dir.glob("*.rpm"):
            shutil.move(str(rpm_file), str(build_dir))
    
    print("✅ RPM package built successfully!")
    print(f"📦 Package location: {build_dir}")


def create_rpm_spec():
    """Create RPM spec file"""
    spec_content = """%global __python %{__python3}
%global python_abi %(python3 -c "import sys; print('python%d.%d' % sys.version_info[:2])")

Name:           gitlab-repo-manager
Version:        1.0.0
Release:        1%{?dist}
Summary:        GitLab Repository Management Tool

License:        MIT
URL:            https://github.com/yourusername/gitlab-repo-manager
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-click
Requires:       python3-requests
Requires:       python3-pyyaml

%description
A modular CLI tool for managing GitLab repositories and Composer dependencies.
Features include:
* Clone user and group repositories
* Concurrent repository operations
* Composer dependency management
* YAML configuration support
* Environment variable override

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.md config.example.yml
%{python3_sitelib}/src/
%{python3_sitelib}/gitlab_repo_manager-*.egg-info/
%{_bindir}/gitlab-repo-manager

%changelog
* Wed Jan 01 2024 Your Name <your.email@example.com> - 1.0.0-1
- Initial release
"""
    
    with open("gitlab-repo-manager.spec", "w") as f:
        f.write(spec_content)


if __name__ == "__main__":
    install_dependencies()
    build_rpm() 