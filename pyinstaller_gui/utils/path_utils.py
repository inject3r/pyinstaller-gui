"""Path utility functions."""

import os
from pathlib import Path
from typing import Optional


class PathUtils:
    """Utility class for path operations."""
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """
        Normalize a path to the platform-specific format.
        
        Converts mixed slashes and redundant separators to the platform's
        standard format. On Windows, converts forward slashes to backslashes.
        On Linux/macOS, normalizes backslashes to forward slashes.
        
        Args:
            path: The path string to normalize.
            
        Returns:
            Normalized path string with platform-appropriate separators.
        """
        return os.path.normpath(path)
    
    @staticmethod
    def get_absolute_path(path: str) -> str:
        """
        Get absolute path.
        
        Converts a relative path to an absolute path by expanding it relative
        to the current working directory.
        
        Args:
            path: The path string (can be relative or absolute).
            
        Returns:
            Absolute path string.
        """
        return os.path.abspath(path)
    
    @staticmethod
    def get_relative_path(path: str, start: Optional[str] = None) -> str:
        """
        Get relative path.
        
        Computes a relative path from the start directory to the target path.
        If start is not provided, uses the current working directory.
        
        Args:
            path: The target path.
            start: The reference directory (default: current working directory).
            
        Returns:
            Relative path string. Returns the original path if the paths
            are on different drives (Windows) or if an error occurs.
        """
        try:
            if start:
                return os.path.relpath(path, start)
            return os.path.relpath(path)
        except ValueError:
            # Different drives on Windows or other ValueError
            return path
    
    @staticmethod
    def get_filename(path: str) -> str:
        """
        Get filename from path.
        
        Extracts the final component of the path (the file or directory name).
        
        Args:
            path: The path string.
            
        Returns:
            Filename (basename) component of the path.
        """
        return os.path.basename(path)
    
    @staticmethod
    def get_directory(path: str) -> str:
        """
        Get directory from path.
        
        Extracts the directory portion of the path, removing the filename.
        
        Args:
            path: The path string.
            
        Returns:
            Directory component of the path (dirname).
        """
        return os.path.dirname(path)
    
    @staticmethod
    def get_extension(path: str) -> str:
        """
        Get file extension.
        
        Extracts the extension including the leading dot (e.g., '.txt').
        
        Args:
            path: The filename or path.
            
        Returns:
            File extension with dot, or empty string if no extension.
        """
        return os.path.splitext(path)[1]
    
    @staticmethod
    def get_filename_without_extension(path: str) -> str:
        """
        Get filename without extension.
        
        Removes the extension from the filename while preserving the
        directory path.
        
        Args:
            path: The filename or full path.
            
        Returns:
            Filename without the extension.
        """
        return os.path.splitext(os.path.basename(path))[0]
    
    @staticmethod
    def join_paths(*paths: str) -> str:
        """
        Join multiple paths.
        
        Combines multiple path components using the platform-appropriate
        path separator.
        
        Args:
            *paths: Variable number of path strings to join.
            
        Returns:
            Combined path string.
        """
        return os.path.join(*paths)
    
    @staticmethod
    def is_subpath(path: str, parent: str) -> bool:
        """
        Check if path is a subpath of parent.
        
        Determines whether the target path is located within the parent
        directory (including nested subdirectories).
        
        Args:
            path: The candidate path to check.
            parent: The potential parent directory.
            
        Returns:
            True if path is inside parent directory, False otherwise.
            Returns False if any OSError occurs during resolution.
        """
        try:
            return Path(parent).resolve() in Path(path).resolve().parents
        except OSError:
            return False
    
    @staticmethod
    def ensure_extension(path: str, extension: str) -> str:
        """
        Ensure path has the given extension.
        
        Appends the specified extension to the path if it doesn't already
        end with that extension.
        
        Args:
            path: The filename or path string.
            extension: The extension to ensure (e.g., '.txt').
            
        Returns:
            Path with the extension appended if it wasn't already present.
        """
        if not path.endswith(extension):
            return path + extension
        return path