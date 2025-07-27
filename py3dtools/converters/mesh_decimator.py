"""Mesh decimation converter for reducing mesh complexity."""

import os
import vtk

from ..core.converters import BaseConverter
from ..core.file_utils import create_output_filename


class MeshDecimatorConverter(BaseConverter):
    """Decimates meshes to reduce complexity while preserving shape."""

    def __init__(self, target_reduction: float = 0.5, preserve_topology: bool = True):
        """Initialize the mesh decimator converter.

        Args:
            target_reduction: Target reduction ratio (0.0 to 1.0, where 1.0 = 100% reduction)
            preserve_topology: Whether to preserve mesh topology during decimation
        """
        super().__init__('.vtp', '_decimated.vtp')
        self.target_reduction = max(0.0, min(1.0, target_reduction))
        self.preserve_topology = preserve_topology

    def convert_single_file(self, input_file: str, output_dir: str) -> bool:
        """Decimate a single mesh file.

        Args:
            input_file: Path to the input mesh file
            output_dir: Directory to save the decimated mesh file

        Returns:
            True if decimation was successful, False otherwise
        """
        try:
            self.validate_input_file(input_file)

            output_file = create_output_filename(
                input_file, output_dir, '_decimated.vtp')

            # Read the input mesh
            mesh = self._read_mesh(input_file)
            if mesh is None:
                return False

            # Apply decimation
            decimated_mesh = self._decimate_mesh(mesh)
            if decimated_mesh is None:
                return False

            # Write the decimated mesh
            success = self._write_mesh(decimated_mesh, output_file)

            if success:
                original_cells = mesh.GetNumberOfCells()
                decimated_cells = decimated_mesh.GetNumberOfCells()
                reduction = (original_cells - decimated_cells) / original_cells
                print(
                    f"Decimated: {os.path.basename(input_file)} -> "
                    f"{os.path.basename(output_file)}")
                print(
                    f"  Reduction: {reduction:.1%} "
                    f"({original_cells} -> {decimated_cells} cells)")

            return success

        except Exception as e:
            print(f"Error decimating {input_file}: {e}")
            return False

    def _read_mesh(self, filepath: str):
        """Read a mesh file using appropriate VTK reader.

        Args:
            filepath: Path to the mesh file

        Returns:
            VTK PolyData object or None if reading failed
        """
        # Determine file type and use appropriate reader
        if filepath.lower().endswith('.vtp'):
            reader = vtk.vtkXMLPolyDataReader()
        elif filepath.lower().endswith('.stl'):
            reader = vtk.vtkSTLReader()
        elif filepath.lower().endswith('.obj'):
            reader = vtk.vtkOBJReader()
        else:
            print(f"Unsupported file format: {filepath}")
            return None

        reader.SetFileName(filepath)
        reader.Update()

        if reader.GetOutput().GetNumberOfCells() == 0:
            print(f"No mesh data found in {filepath}")
            return None

        return reader.GetOutput()

    def _decimate_mesh(self, mesh):
        """Apply decimation to the mesh.

        Args:
            mesh: VTK PolyData object

        Returns:
            Decimated VTK PolyData object or None if decimation failed
        """
        # Create decimation filter
        decimator = vtk.vtkDecimatePro()
        decimator.SetInputData(mesh)
        decimator.SetTargetReduction(self.target_reduction)
        decimator.SetPreserveTopology(self.preserve_topology)
        decimator.SetBoundaryVertexDeletion(False)
        decimator.SetFeatureEdgeSplitting(True)
        decimator.SetSplitting(True)
        decimator.SetErrorIsAbsolute(False)
        decimator.SetAbsoluteError(0.0)
        decimator.SetAccumulateError(True)
        decimator.SetMaximumError(0.01)
        decimator.Update()

        return decimator.GetOutput()

    def _write_mesh(self, mesh, output_file: str) -> bool:
        """Write mesh to file.

        Args:
            mesh: VTK PolyData object
            output_file: Path to output file

        Returns:
            True if writing was successful, False otherwise
        """
        # Determine output format and use appropriate writer
        if output_file.lower().endswith('.vtp'):
            writer = vtk.vtkXMLPolyDataWriter()
        elif output_file.lower().endswith('.stl'):
            writer = vtk.vtkSTLWriter()
        elif output_file.lower().endswith('.obj'):
            writer = vtk.vtkOBJWriter()
        else:
            print(f"Unsupported output format: {output_file}")
            return False

        writer.SetInputData(mesh)
        writer.SetFileName(output_file)
        return writer.Write() == 1

    def convert_directory(self, input_dir: str, output_dir: str) -> int:
        """Decimate all mesh files in a directory.

        Args:
            input_dir: Directory containing input mesh files
            output_dir: Directory to save decimated mesh files

        Returns:
            Number of successfully decimated files
        """
        # Override to support multiple input formats
        import os

        from ..core.file_utils import ensure_directory_exists

        ensure_directory_exists(output_dir)

        # Find all supported mesh files
        supported_extensions = ['.vtp', '.stl', '.obj']
        input_files = []
        for ext in supported_extensions:
            input_files.extend(self._get_files_with_extension(input_dir, ext))

        if not input_files:
            print(f"No supported mesh files found in {input_dir}")
            return 0

        success_count = 0
        print(f"Input directory: {input_dir}")
        print(f"Output directory: {output_dir}")
        print(f"Target reduction: {self.target_reduction:.1%}")

        for input_file in input_files:
            try:
                if self.convert_single_file(input_file, output_dir):
                    success_count += 1
                    print(f"✓ Decimated: {os.path.basename(input_file)}")
                else:
                    print(f"✗ Failed: {os.path.basename(input_file)}")
            except Exception as e:
                print(
                    f"✗ Error decimating {os.path.basename(input_file)}: {e}")

        print(
            f"Successfully decimated {success_count} out of {len(input_files)} files.")
        return success_count

    def _get_files_with_extension(self, directory_path: str, extension: str):
        """Get all files in a directory with a specific extension.

        Args:
            directory_path: Path to the directory to search
            extension: File extension to filter by

        Returns:
            List of file paths with the specified extension
        """
        if not os.path.isdir(directory_path):
            return []

        files = []
        for filename in os.listdir(directory_path):
            if filename.lower().endswith(extension.lower()):
                files.append(os.path.join(directory_path, filename))

        return files
