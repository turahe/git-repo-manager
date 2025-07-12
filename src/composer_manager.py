import os
import subprocess
from typing import Optional


class ComposerManager:
    """Manages Composer operations"""
    
    def __init__(self):
        self.composer_cmd = self._find_composer_command()
    
    def _find_composer_command(self) -> str:
        """Find the appropriate composer command for the system"""
        commands = ['composer', 'composer.bat', 'composer.cmd']
        
        for cmd in commands:
            try:
                subprocess.run([cmd, '--version'], capture_output=True, check=True)
                return cmd
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        raise FileNotFoundError("Composer command not found. Make sure Composer is installed and in your PATH.")
    
    def find_and_update_composer(self, root_dir: str) -> None:
        """
        Traverses a root directory and its subdirectories to find composer.json files.
        If found, it runs 'composer update' in that directory.

        Args:
            root_dir (str): The starting directory to search from.
        """
        print(f"Starting search for composer.json in: {root_dir}")
        
        if not os.path.isdir(root_dir):
            print(f"Error: The specified search directory does not exist: {root_dir}")
            return
        
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if 'composer.json' in filenames:
                composer_path = os.path.join(dirpath, 'composer.json')
                print(f"\nFound composer.json at: {composer_path}")
                print(f"Changing directory to: {dirpath}")
                
                original_dir = os.getcwd()  # Store original directory
                try:
                    os.chdir(dirpath)
                    print("Running 'composer update'...")
                    
                    result = subprocess.run([self.composer_cmd, 'update'], capture_output=True, text=True, check=True)
                    
                    print("Composer update output:")
                    print(result.stdout)
                    if result.stderr:
                        print("Composer update errors (if any):")
                        print(result.stderr)
                    print("Composer update completed successfully.")
                    
                except FileNotFoundError:
                    print("Error: 'composer' command not found. Make sure Composer is installed and in your PATH.")
                    print("On Windows, try running: composer --version in your terminal to verify installation.")
                    print("If composer is installed but not in PATH, you may need to add it to your system PATH.")
                except subprocess.CalledProcessError as e:
                    print(f"Error running 'composer update' in {dirpath}:")
                    print(e.stdout)
                    print(e.stderr)
                except Exception as e:
                    print(f"An unexpected error occurred in {dirpath}: {e}")
                finally:
                    os.chdir(original_dir)  # Always change back to the original directory
                    print(f"Returned to original directory: {os.getcwd()}")
        
        print("\nSearch and update process completed.") 