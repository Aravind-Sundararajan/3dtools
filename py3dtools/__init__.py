"""py3dtools - 3D file format conversion tools."""

__version__ = "0.0.4"

# Import converters for easy access
from .converters import (
    VTPToSTLConverter,
    STLToOBJConverter,
    OBJMirrorConverter,
    STLToVTPConverter,
    OBJToSTLConverter,
    OBJToVTPConverter,
    MeshDecimatorConverter,
)

# Import core utilities
from .core import BaseConverter, ensure_directory_exists, validate_file_extension

__all__ = [
    # Converters
    "VTPToSTLConverter",
    "STLToOBJConverter",
    "OBJMirrorConverter",
    "STLToVTPConverter",
    "OBJToSTLConverter",
    "OBJToVTPConverter",
    "MeshDecimatorConverter",
    # Core utilities
    "BaseConverter",
    "ensure_directory_exists",
    "validate_file_extension",
]
