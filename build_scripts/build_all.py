#!/usr/bin/env python3
"""
Master build script for creating all package types (EXE, DEB, RPM)
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def detect_platform():
    """Detect the current platform"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "linux":
        # Try to detect distribution
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "ubuntu" in content or "debian" in content:
                    return "debian"
                elif "redhat" in content or "centos" in content or "fedora" in content:
                    return "rpm"
        except FileNotFoundError:
            pass
        return "linux"
    else:
        return "unknown"


def build_windows():
    """Build Windows EXE"""
    print("🪟 Building Windows EXE...")
    try:
        subprocess.run([sys.executable, "build_scripts/build_exe.py"], check=True)
        print("✅ Windows build completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows build failed: {e}")


def build_debian():
    """Build DEB package"""
    print("🐧 Building DEB package...")
    try:
        subprocess.run([sys.executable, "build_scripts/build_deb.py"], check=True)
        print("✅ DEB build completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ DEB build failed: {e}")


def build_rpm():
    """Build RPM package"""
    print("🔴 Building RPM package...")
    try:
        subprocess.run([sys.executable, "build_scripts/build_rpm.py"], check=True)
        print("✅ RPM build completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ RPM build failed: {e}")


def build_all():
    """Build all package types"""
    print("🚀 Starting build process for all platforms...")
    
    # Create dist directory structure
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    for platform_dir in ["windows", "debian", "rpm"]:
        (dist_dir / platform_dir).mkdir(exist_ok=True)
    
    # Build based on current platform
    current_platform = detect_platform()
    
    if current_platform == "windows":
        build_windows()
    elif current_platform == "debian":
        build_debian()
    elif current_platform == "rpm":
        build_rpm()
    else:
        print(f"⚠️  Unknown platform: {current_platform}")
        print("Available build scripts:")
        print("  - build_scripts/build_exe.py (Windows)")
        print("  - build_scripts/build_deb.py (Debian/Ubuntu)")
        print("  - build_scripts/build_rpm.py (Red Hat/CentOS/Fedora)")


def main():
    """Main function"""
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
        if target == "windows" or target == "exe":
            build_windows()
        elif target == "debian" or target == "deb":
            build_debian()
        elif target == "rpm":
            build_rpm()
        elif target == "all":
            build_all()
        else:
            print(f"❌ Unknown target: {target}")
            print("Available targets: windows, debian, rpm, all")
            sys.exit(1)
    else:
        # Default to building for current platform
        build_all()


if __name__ == "__main__":
    main() 