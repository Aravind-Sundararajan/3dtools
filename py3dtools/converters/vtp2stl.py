"""VTP to STL file format converter."""

import os
import vtk

from ..core.converters import BaseConverter
from ..core.file_utils import create_output_filename


class VTPToSTLConverter(BaseConverter):
    """Converts VTP (VTK XML PolyData) files to STL format."""

    def __init__(self):
        """Initialize the VTP to STL converter."""
        super().__init__('.vtp', '.stl')

    def convert_single_file(self, input_file: str, output_dir: str) -> bool:
        """Convert a single VTP file to STL format.

        Args:
            input_file: Path to the input VTP file
            output_dir: Directory to save the output STL file

        Returns:
            True if conversion was successful, False otherwise
        """
        try:
            self.validate_input_file(input_file)

            output_file = create_output_filename(
                input_file, output_dir, '.stl')

            # Create VTK reader for VTP files
            reader = vtk.vtkXMLPolyDataReader()
            reader.SetFileName(input_file)
            reader.Update()

            # Create VTK writer for STL files
            writer = vtk.vtkSTLWriter()
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
