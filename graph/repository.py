"""Repository management utilities."""
import os
from git import Repo
from pathlib import Path


class RepositoryManager:
    """Manages repository cloning and file discovery."""
    
    @staticmethod
    def clone_if_needed(repo_url, target_path):
        """Clone a GitHub repository if it doesn't exist."""
        if os.path.exists(target_path):
            print(f"Repository already exists at {target_path}")
            return True
        
        try:
            print(f"Started cloning into {os.getcwd()}/{target_path} ...")
            Repo.clone_from(repo_url, target_path)
            print("Finished cloning")
            return True
        except Exception as e:
            print(f"Error cloning repository: {e}")
            return False
    
    @staticmethod
    def pull(target_path):
        """
        Pull the latest changes from the repository.
        
        Args:
            target_path: Path to the cloned repository
        
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(target_path):
            print(f"Repository not found at {target_path}")
            return False
        
        try:
            print(f"Pulling latest changes from {target_path}...")
            repo = Repo(target_path)
            
            # Discard local changes before pulling
            repo.git.checkout("--", ".")
            repo.git.clean("-fd")
            
            repo.remotes.origin.pull()
            print("Pull successful")
            return True
        except Exception as e:
            print(f"Error pulling repository: {e}")
            return False
    
    def get_python_files(self):
        """Find all Python files in the repository."""
        path = Path(self.code_root_folder)
        return sorted(path.rglob("*.py"))
    
    def file_path(self, file_name):
        """Get full path for a file name."""
        return os.path.join(self.code_root_folder, file_name)
