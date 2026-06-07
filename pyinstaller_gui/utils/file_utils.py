"""File utility functions."""

import os
import shutil
from pathlib import Path
from typing import List, Optional


class FileUtils:
    """Utility class for file operations."""
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to the file to check.
            
        Returns:
            True if the file exists and is a regular file, False otherwise.
        """
        return os.path.isfile(file_path)
    
    @staticmethod
    def folder_exists(folder_path: str) -> bool:
        """
        Check if a folder exists.
        
        Args:
            folder_path: Path to the folder to check.
            
        Returns:
            True if the folder exists and is a directory, False otherwise.
        """
        return os.path.isdir(folder_path)
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            File size in bytes, or 0 if the file doesn't exist or an error occurs.
        """
        try:
            return os.path.getsize(file_path)
        except OSError:
            return 0
    
    @staticmethod
    def get_folder_size(folder_path: str) -> int:
        """
        Get folder size in bytes.
        
        Recursively calculates the total size of all files within a directory,
        including all subdirectories.
        
        Args:
            folder_path: Path to the folder.
            
        Returns:
            Total size of all files in the folder in bytes, or 0 if an error occurs.
        """
        total = 0
        try:
            for entry in os.scandir(folder_path):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += FileUtils.get_folder_size(entry.path)
        except OSError:
            pass
        return total
    
    @staticmethod
    def create_directory(path: str) -> bool:
        """
        Create a directory if it doesn't exist.
        
        Creates the directory and any necessary parent directories.
        Does nothing if the directory already exists.
        
        Args:
            path: Path of the directory to create.
            
        Returns:
            True if the directory was created or already exists, False if
            an error occurred during creation.
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except OSError:
            return False
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete a file.
        
        Args:
            file_path: Path to the file to delete.
            
        Returns:
            True if the file was successfully deleted, False if an error occurs.
        """
        try:
            os.remove(file_path)
            return True
        except OSError:
            return False
    
    @staticmethod
    def delete_folder(folder_path: str) -> bool:
        """
        Delete a folder and all its contents.
        
        Recursively deletes the directory and all files and subdirectories
        contained within it.
        
        Args:
            folder_path: Path to the folder to delete.
            
        Returns:
            True if the folder was successfully deleted, False if an error occurs.
        """
        try:
            shutil.rmtree(folder_path)
            return True
        except OSError:
            return False
    
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> List[str]:
        """
        List files in a directory matching pattern.
        
        Args:
            directory: Path to the directory to search.
            pattern: Glob pattern for filtering files (default: '*' for all files).
            
        Returns:
            List of file paths matching the pattern, or empty list if the
            directory doesn't exist or an error occurs.
        """
        try:
            return [str(p) for p in Path(directory).glob(pattern) if p.is_file()]
        except OSError:
            return []
    
    @staticmethod
    def list_folders(directory: str) -> List[str]:
        """
        List folders in a directory.
        
        Args:
            directory: Path to the directory to search.
            
        Returns:
            List of directory paths within the specified directory, or empty list
            if the directory doesn't exist or an error occurs.
        """
        try:
            return [str(p) for p in Path(directory).iterdir() if p.is_dir()]
        except OSError:
            return []