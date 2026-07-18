"""STL to OBJ file format converter."""

import os

from ..core.converters import BaseConverter
from ..core.file_utils import create_output_filename


class STLToOBJConverter(BaseConverter):
    """Converts STL files to OBJ format."""

    def __init__(self):
        """Initialize the STL to OBJ converter."""
        super().__init__(".stl", ".obj")

    def convert_single_file(self, input_file: str, output_dir: str) -> bool:
        """Convert a single STL file to OBJ format.

        Args:
            input_file: Path to the input STL file
            output_dir: Directory to save the output OBJ file

        Returns:
            True if conversion was successful, False otherwise
        """
        try:
            self.validate_input_file(input_file)

            output_file = create_output_filename(input_file, output_dir, ".obj")

            # Parse STL file
            vertices, faces = self._parse_stl_file(input_file)

            # Write OBJ file
            self._write_obj_file(output_file, vertices, faces, input_file)

            print(
                f"Converted: {os.path.basename(input_file)} -> "
                f"{os.path.basename(output_file)}"
            )
            return True

        except Exception as e:
            print(f"Error converting {input_file}: {e}")
            return False

    def _parse_stl_file(
        self, filepath: str
    ) -> tuple[list[tuple[float, float, float]], list[list[int]]]:
        """Parse an STL file and extract vertices and faces.

        Args:
            filepath: Path to the STL file

        Returns:
            Tuple of (vertices, faces) where vertices are 3D coordinates and faces are vertex indices
        """
        points = []
        facets = []

        with open(filepath) as stlfile:
            # Skip header lines
            stlfile.readline()  # solid name
            stlfile.readline()  # facet normal

            line = stlfile.readline()
            while line:
                vertices = []
                tab = line.strip().split()

                if len(tab) > 0 and "facet" in tab[0]:
                    # Read facet data
                    while line and "endfacet" not in tab[0]:
                        if "vertex" in tab[0]:
                            vertex = (float(tab[1]), float(tab[2]), float(tab[3]))
                            points.append(vertex)
                            vertices.append(vertex)

                        line = stlfile.readline()
                        tab = line.strip().split() if line else []

                    if vertices:
                        facets.append(vertices)

                line = stlfile.readline()

        # Deduplicate vertices and create face indices
        unique_vertices = list(set(points))
        vertex_map = {vertex: idx + 1 for idx, vertex in enumerate(unique_vertices)}

        faces = []
        for facet in facets:
            face_indices = [vertex_map[vertex] for vertex in facet]
            faces.append(face_indices)

        return unique_vertices, faces

    def _write_obj_file(
        self,
        output_file: str,
        vertices: list[tuple[float, float, float]],
        faces: list[list[int]],
        source_file: str,
    ) -> None:
        """Write vertices and faces to an OBJ file.

        Args:
            output_file: Path to the output OBJ file
            vertices: List of 3D vertex coordinates
            faces: List of face vertex indices
            source_file: Original STL file name for header
        """
        with open(output_file, "w") as objfile:
            objfile.write("# File type: ASCII OBJ\n")
            objfile.write(f"# Generated from {os.path.basename(source_file)}\n")

            # Write vertices
            for vertex in vertices:
                objfile.write(f"v {' '.join(map(str, vertex))}\n")

            # Write faces
            for face in faces:
                objfile.write(f"f {' '.join(map(str, face))}\n")
