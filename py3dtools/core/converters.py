"""Base converter class for all file format converters."""

from abc import ABC, abstractmethod
import os

from .exceptions import ValidationError
from .file_utils import ensure_directory_exists, get_files_with_extension


class BaseConverter(ABC):
    """Base class for all file format converters."""

    def __init__(self, input_extension: str, output_extension: str):
        """Initialize the converter with input and output extensions.

        Args:
            input_extension: Expected input file extension (e.g., '.vtp')
            output_extension: Output file extension (e.g., '.stl')
        """
        self.input_extension = input_extension.lower()
        self.output_extension = output_extension.lower()

    def convert_directory(self, input_dir: str, output_dir: str) -> int:
        """Convert all files in a directory.

        Args:
            input_dir: Directory containing input files
            output_dir: Directory to save output files

        Returns:
            Number of successfully converted files
        """
        ensure_directory_exists(output_dir)

        input_files = get_files_with_extension(input_dir, self.input_extension)
        if not input_files:
            print(f"No {self.input_extension} files found in {input_dir}")
            return 0

        success_count = 0
        print(f"Input directory: {input_dir}")
        print(f"Output directory: {output_dir}")

        for input_file in input_files:
            try:
                if self.convert_single_file(input_file, output_dir):
                    success_count += 1
                    print(f"✓ Converted: {os.path.basename(input_file)}")
                else:
                    print(f"✗ Failed: {os.path.basename(input_file)}")
            except Exception as e:
                print(f"✗ Error converting {os.path.basename(input_file)}: {e}")

        print(
            f"Successfully converted {success_count} out of {len(input_files)} files."
        )
        return success_count

    @abstractmethod
    def convert_single_file(self, input_file: str, output_dir: str) -> bool:
        """Convert a single file.

        Args:
            input_file: Path to the input file
            output_dir: Directory to save the output file

        Returns:
            True if conversion was successful, False otherwise
        """
        pass

    def validate_input_file(self, input_file: str) -> None:
        """Validate that the input file exists and has the correct extension.

        Args:
            input_file: Path to the input file

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValidationError: If the file extension is incorrect
        """
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        if not input_file.lower().endswith(self.input_extension):
            raise ValidationError(
                f"Input file {input_file} does not have expected extension {self.input_extension}"
            )
