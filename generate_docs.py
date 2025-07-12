#!/usr/bin/env python3
"""
Documentation generator for Git Repository Manager.
This script generates API documentation from source code.
"""

import os
import sys
import inspect
import importlib
from pathlib import Path
from typing import Dict, List, Any

def get_module_info(module_name: str) -> Dict[str, Any]:
    """Extract information from a module."""
    try:
        module = importlib.import_module(module_name)
        info = {
            'name': module_name,
            'docstring': module.__doc__ or '',
            'classes': [],
            'functions': []
        }
        
        # Get classes
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:
                class_info = {
                    'name': name,
                    'docstring': obj.__doc__ or '',
                    'methods': []
                }
                
                # Get methods
                for method_name, method_obj in inspect.getmembers(obj, inspect.isfunction):
                    if method_obj.__module__ == module_name:
                        method_info = {
                            'name': method_name,
                            'docstring': method_obj.__doc__ or '',
                            'signature': str(inspect.signature(method_obj))
                        }
                        class_info['methods'].append(method_info)
                
                info['classes'].append(class_info)
        
        # Get functions
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if obj.__module__ == module_name:
                function_info = {
                    'name': name,
                    'docstring': obj.__doc__ or '',
                    'signature': str(inspect.signature(obj))
                }
                info['functions'].append(function_info)
        
        return info
    except ImportError as e:
        print(f"Warning: Could not import {module_name}: {e}")
        return {'name': module_name, 'error': str(e)}

def generate_api_docs() -> str:
    """Generate API documentation from source code."""
    modules = [
        'src.config',
        'src.gitlab_client',
        'src.github_client',
        'src.repository_manager',
        'src.composer_manager',
        'src.services'
    ]
    
    docs = []
    docs.append("# API Documentation")
    docs.append("")
    docs.append("This documentation is auto-generated from the source code.")
    docs.append("")
    
    for module_name in modules:
        module_info = get_module_info(module_name)
        
        if 'error' in module_info:
            docs.append(f"## {module_name}")
            docs.append(f"")
            docs.append(f"Error: {module_info['error']}")
            docs.append("")
            continue
        
        docs.append(f"## {module_info['name']}")
        docs.append("")
        
        if module_info['docstring']:
            docs.append(module_info['docstring'])
            docs.append("")
        
        # Classes
        if module_info['classes']:
            docs.append("### Classes")
            docs.append("")
            
            for class_info in module_info['classes']:
                docs.append(f"#### {class_info['name']}")
                docs.append("")
                
                if class_info['docstring']:
                    docs.append(class_info['docstring'])
                    docs.append("")
                
                # Methods
                if class_info['methods']:
                    docs.append("**Methods:**")
                    docs.append("")
                    
                    for method_info in class_info['methods']:
                        docs.append(f"- `{method_info['name']}{method_info['signature']}`")
                        if method_info['docstring']:
                            docs.append(f"  - {method_info['docstring'].split('.')[0]}.")
                        docs.append("")
        
        # Functions
        if module_info['functions']:
            docs.append("### Functions")
            docs.append("")
            
            for function_info in module_info['functions']:
                docs.append(f"#### {function_info['name']}")
                docs.append("")
                docs.append(f"```python")
                docs.append(f"{function_info['name']}{function_info['signature']}")
                docs.append(f"```")
                docs.append("")
                
                if function_info['docstring']:
                    docs.append(function_info['docstring'])
                    docs.append("")
    
    return "\n".join(docs)

def generate_cli_docs() -> str:
    """Generate CLI documentation."""
    try:
        import click
        from cli import cli
        
        docs = []
        docs.append("# CLI Reference")
        docs.append("")
        docs.append("This documentation is auto-generated from the CLI commands.")
        docs.append("")
        
        # Get CLI help
        import subprocess
        result = subprocess.run([sys.executable, 'cli.py', '--help'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            docs.append("## Global Help")
            docs.append("")
            docs.append("```bash")
            docs.append(result.stdout)
            docs.append("```")
            docs.append("")
        
        # Get help for each command
        commands = [
            'init-config',
            'validate-config',
            'config-info',
            'clone-user',
            'clone-groups',
            'clone-github-user',
            'clone-github-org',
            'update-composer'
        ]
        
        for command in commands:
            try:
                result = subprocess.run([sys.executable, 'cli.py', command, '--help'], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    docs.append(f"## {command}")
                    docs.append("")
                    docs.append("```bash")
                    docs.append(result.stdout)
                    docs.append("```")
                    docs.append("")
            except Exception as e:
                print(f"Warning: Could not get help for {command}: {e}")
        
        return "\n".join(docs)
    except Exception as e:
        return f"# CLI Reference\n\nError generating CLI documentation: {e}"

def main():
    """Generate documentation files."""
    print("Generating documentation...")
    
    # Create docs directory if it doesn't exist
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Generate API documentation
    api_docs = generate_api_docs()
    with open(docs_dir / "api_auto.md", "w", encoding="utf-8") as f:
        f.write(api_docs)
    print("Generated api_auto.md")
    
    # Generate CLI documentation
    cli_docs = generate_cli_docs()
    with open(docs_dir / "cli_auto.md", "w", encoding="utf-8") as f:
        f.write(cli_docs)
    print("Generated cli_auto.md")
    
    # Generate README for docs
    readme_content = """# Documentation

This directory contains comprehensive documentation for Git Repository Manager.

## Manual Documentation

- [Index](index.md) - Main documentation index
- [Installation](installation.md) - Installation guide
- [Configuration](configuration.md) - Configuration guide
- [Usage](usage.md) - Usage guide
- [CLI Reference](cli.md) - Command-line interface reference
- [API Reference](api.md) - API documentation
- [Examples](examples.md) - Usage examples
- [Troubleshooting](troubleshooting.md) - Troubleshooting guide
- [Development](development.md) - Development guide

## Auto-Generated Documentation

- [API Auto](api_auto.md) - Auto-generated API documentation
- [CLI Auto](cli_auto.md) - Auto-generated CLI documentation

## Building Documentation

To regenerate the auto-generated documentation:

```bash
python generate_docs.py
```

## Documentation Structure

The documentation is organized into several categories:

1. **User Guides** - Installation, configuration, usage
2. **Reference** - CLI and API documentation
3. **Examples** - Practical usage examples
4. **Troubleshooting** - Common issues and solutions
5. **Development** - Contributing and development setup

## Contributing to Documentation

When contributing to documentation:

1. Follow the existing style and format
2. Include practical examples
3. Update both manual and auto-generated docs as needed
4. Test all code examples
5. Keep documentation up to date with code changes
"""
    
    with open(docs_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("Generated README.md")
    
    print("Documentation generation completed!")

if __name__ == "__main__":
    main() 