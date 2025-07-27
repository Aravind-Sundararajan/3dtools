"""OBJ to VTP file format converter."""

import os
import vtk

from ..core.converters import BaseConverter
from ..core.file_utils import create_output_filename


class OBJToVTPConverter(BaseConverter):
    """Converts OBJ files to VTP (VTK XML PolyData) format."""

    def __init__(self):
        """Initialize the OBJ to VTP converter."""
        super().__init__('.obj', '.vtp')

    def convert_single_file(self, input_file: str, output_dir: str) -> bool:
        """Convert a single OBJ file to VTP format.

        Args:
            input_file: Path to the input OBJ file
            output_dir: Directory to save the output VTP file

        Returns:
            True if conversion was successful, False otherwise
        """
        try:
            self.validate_input_file(input_file)

            output_file = create_output_filename(
                input_file, output_dir, '.vtp')

            # Create VTK reader for OBJ files
            reader = vtk.vtkOBJReader()
            reader.SetFileName(input_file)
            reader.Update()

            # Create VTK writer for VTP files
            writer = vtk.vtkXMLPolyDataWriter()
            writer.SetInputConnection(reader.GetOutputPort())
            writer.SetFileName(output_file)

            # Perform the conversion
            success = writer.Write() == 1

            if success:
                print(
                    f"Converted: {os.path.basename(input_file)} -> "
                    f"{os.path.basename(output_file)}")

            return success

        except Exception as e:
            print(f"Error converting {input_file}: {e}")
            return False
