"""Repository management utilities."""
import os
from git import Repo

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
            repo.remotes.origin.pull()
            print("Pull successful")
            return True
        except Exception as e:
            print(f"Error pulling repository: {e}")
            return False
