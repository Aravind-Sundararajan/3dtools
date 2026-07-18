"""Shared file utility functions."""

import os
from pathlib import Path

from .exceptions import ValidationError, FileNotFoundError


def ensure_directory_exists(directory_path: str) -> None:
    """Ensure a directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory to ensure exists
    """
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path)


def validate_file_extension(file_path: str, expected_extensions: list[str]) -> None:
    """Validate that a file has one of the expected extensions.

    Args:
        file_path: Path to the file to validate
        expected_extensions: List of expected file extensions (e.g., ['.vtp', '.stl'])

    Raises:
        ValidationError: If the file extension is not in the expected list
    """
    file_ext = Path(file_path).suffix.lower()
    if file_ext not in expected_extensions:
        raise ValidationError(
            f"File {file_path} has extension {file_ext}, "
            f"expected one of: {expected_extensions}"
        )


def get_files_with_extension(directory_path: str, extension: str) -> list[str]:
    """Get all files in a directory with a specific extension.

    Args:
        directory_path: Path to the directory to search
        extension: File extension to filter by (e.g., '.vtp')

    Returns:
        List of file paths with the specified extension
    """
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    files = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(extension.lower()):
            files.append(os.path.join(directory_path, filename))

    return files


def create_output_filename(input_path: str, output_dir: str, new_extension: str) -> str:
    """Create an output filename based on input file and new extension.

    Args:
        input_path: Path to the input file
        output_dir: Directory for the output file
        new_extension: New file extension (e.g., '.stl')

    Returns:
        Full path to the output file
    """
    input_filename = Path(input_path).stem
    output_filename = f"{input_filename}{new_extension}"
    return os.path.join(output_dir, output_filename)
