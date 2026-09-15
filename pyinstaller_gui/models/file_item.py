"""File item data model."""

from dataclasses import dataclass
from enum import Enum, auto


class FileType(Enum):
    """
    Enum for file types.
    
    Defines the three types of items that can be added to the build:
    - FILE: Regular data files (images, configs, text files, etc.)
    - FOLDER: Entire directory structures
    - BINARY: Executable binaries (DLLs, SOs, DYLIBs, EXEs)
    """
    FILE = auto()
    FOLDER = auto()
    BINARY = auto()
    
    def __str__(self):
        """
        Return a human-readable string representation of the file type.
        
        Returns:
            Capitalized name of the enum member: "File", "Folder", or "Binary".
        """
        return self.name.capitalize()


@dataclass
class FileItem:
    """
    Represents a file or folder to be added to the build.
    
    This dataclass stores information about an item that should be bundled
    with the executable. It includes the path to the item, its type, and
    the destination directory inside the bundle.
    
    Attributes:
        path: The filesystem path to the file or folder.
        file_type: The type of item (FILE, FOLDER, or BINARY).
        dest: Destination directory inside the bundled app, relative to the
            top-level application directory. Defaults to "." (the root of
            the bundle).
    
    The class implements equality and hashing based on the path, type, and
    destination, allowing FileItem objects to be used in sets and as
    dictionary keys.
    """
    
    path: str
    file_type: FileType
    dest: str = "."
    
    def __post_init__(self):
        """Normalize an empty/whitespace destination to the bundle root ('.')."""
        if not self.dest or not str(self.dest).strip():
            self.dest = "."
    
    def __eq__(self, other):
        """
        Check equality with another object.
        
        Two FileItem objects are considered equal if they have the same
        path, file type, and destination.
        
        Args:
            other: The object to compare with.
            
        Returns:
            True if the objects are equal, False otherwise.
        """
        if not isinstance(other, FileItem):
            return False
        return (
            self.path == other.path
            and self.file_type == other.file_type
            and self.dest == other.dest
        )
    
    def __hash__(self):
        """
        Compute hash value for the FileItem.
        
        The hash is based on the path, file type, and destination, ensuring
        that items with different properties generate different hash values.
        
        Returns:
            Hash value computed from the path, file_type, and dest.
        """
        return hash((self.path, self.file_type, self.dest))
