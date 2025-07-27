"""OBJ file mirroring converter."""

import os
from typing import List, Tuple

from ..core.converters import BaseConverter
from ..core.file_utils import create_output_filename


class OBJMirrorConverter(BaseConverter):
    """Mirrors OBJ files along specified axes."""

    def __init__(self, mirror_axis: str = 'X'):
        """Initialize the OBJ mirror converter.

        Args:
            mirror_axis: Axis to mirror along ('X', 'Y', or 'Z')
        """
        super().__init__('.obj', '_mirror.obj')
        self.mirror_axis = mirror_axis.upper()

        if self.mirror_axis not in ['X', 'Y', 'Z']:
            raise ValueError("mirror_axis must be 'X', 'Y', or 'Z'")

    def convert_single_file(self, input_file: str, output_dir: str) -> bool:
        """Mirror a single OBJ file along the specified axis.

        Args:
            input_file: Path to the input OBJ file
            output_dir: Directory to save the mirrored OBJ file

        Returns:
            True if mirroring was successful, False otherwise
        """
        try:
            self.validate_input_file(input_file)

            # Skip files that are already mirrored
            if '_mirror.obj' in input_file.lower():
                return False

            output_file = create_output_filename(
                input_file, output_dir, '_mirror.obj')

            # Parse OBJ file
            vertices, faces = self._parse_obj_file(input_file)

            # Mirror vertices
            mirrored_vertices = self._mirror_vertices(vertices)

            # Write mirrored OBJ file
            self._write_obj_file(
                output_file, mirrored_vertices, faces, input_file)

            print(
                f"Mirrored: {os.path.basename(input_file)} -> "
                f"{os.path.basename(output_file)}")
            return True

        except Exception as e:
            print(f"Error mirroring {input_file}: {e}")
            return False

    def _parse_obj_file(self, filepath: str) -> Tuple[List[List[float]], List[List[int]]]:
        """Parse an OBJ file and extract vertices and faces.

        Args:
            filepath: Path to the OBJ file

        Returns:
            Tuple of (vertices, faces) where vertices are 3D coordinates and faces are vertex indices
        """
        vertices = []
        faces = []

        with open(filepath, "r") as f:
            for line in f:
                tokens = line.strip().split()
                if len(tokens) == 0:
                    continue

                if tokens[0] == "v":
                    # Vertex line: v x y z
                    vertex = [float(x) for x in tokens[1:4]]
                    vertices.append(vertex)
                elif tokens[0] == "f":
                    # Face line: f v1 v2 v3 ...
                    face = [int(x.split("/")[0]) for x in tokens[1:]]
                    faces.append(face)

        return vertices, faces

    def _mirror_vertices(self, vertices: List[List[float]]) -> List[List[float]]:
        """Mirror vertices along the specified axis.

        Args:
            vertices: List of 3D vertex coordinates

        Returns:
            List of mirrored 3D vertex coordinates
        """
        # Create mirror transformation
        mirror_sign = [-1 if axis == self.mirror_axis else 1 for axis in "XYZ"]

        # Apply mirroring to each vertex
        mirrored_vertices = []
        for vertex in vertices:
            mirrored_vertex = [mirror_sign[i] * vertex[i] for i in range(3)]
            mirrored_vertices.append(mirrored_vertex)

        return mirrored_vertices

    def _write_obj_file(self, output_file: str, vertices: List[List[float]],
                        faces: List[List[int]], source_file: str) -> None:
        """Write vertices and faces to an OBJ file.

        Args:
            output_file: Path to the output OBJ file
            vertices: List of 3D vertex coordinates
            faces: List of face vertex indices
            source_file: Original OBJ file name for header
        """
        with open(output_file, "w") as f:
            f.write("# File type: ASCII OBJ\n")
            f.write(f"# Generated from {os.path.basename(source_file)}\n")

            # Write vertices
            for vertex in vertices:
                f.write(f"v {' '.join(str(x) for x in vertex)}\n")

            # Write faces
            for face in faces:
                f.write(f"f {' '.join(str(x) for x in face)}\n")
