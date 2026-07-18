"""Basic tests to verify the project setup."""

import vtk


def test_vtk_import():
    """Test that VTK can be imported."""
    assert vtk is not None


def test_vtp2stl_converter_import():
    """Test that VTPToSTLConverter can be imported."""
    from py3dtools.converters import VTPToSTLConverter

    assert VTPToSTLConverter is not None


def test_stl2obj_converter_import():
    """Test that STLToOBJConverter can be imported."""
    from py3dtools.converters import STLToOBJConverter

    assert STLToOBJConverter is not None


def test_mirrorobj_converter_import():
    """Test that OBJMirrorConverter can be imported."""
    from py3dtools.converters import OBJMirrorConverter

    assert OBJMirrorConverter is not None


def test_stl2vtp_converter_import():
    """Test that STLToVTPConverter can be imported."""
    from py3dtools.converters import STLToVTPConverter

    assert STLToVTPConverter is not None


def test_obj2stl_converter_import():
    """Test that OBJToSTLConverter can be imported."""
    from py3dtools.converters import OBJToSTLConverter

    assert OBJToSTLConverter is not None


def test_obj2vtp_converter_import():
    """Test that OBJToVTPConverter can be imported."""
    from py3dtools.converters import OBJToVTPConverter

    assert OBJToVTPConverter is not None


def test_mesh_decimator_converter_import():
    """Test that MeshDecimatorConverter can be imported."""
    from py3dtools.converters import MeshDecimatorConverter

    assert MeshDecimatorConverter is not None


def test_base_converter_import():
    """Test that BaseConverter can be imported."""
    from py3dtools.core import BaseConverter

    assert BaseConverter is not None


def test_converter_instantiation():
    """Test that converters can be instantiated."""
    from py3dtools.converters import (
        VTPToSTLConverter,
        STLToOBJConverter,
        OBJMirrorConverter,
        STLToVTPConverter,
        OBJToSTLConverter,
        OBJToVTPConverter,
        MeshDecimatorConverter,
    )

    vtp_converter = VTPToSTLConverter()
    assert vtp_converter.input_extension == ".vtp"
    assert vtp_converter.output_extension == ".stl"

    stl_converter = STLToOBJConverter()
    assert stl_converter.input_extension == ".stl"
    assert stl_converter.output_extension == ".obj"

    mirror_converter = OBJMirrorConverter()
    assert mirror_converter.input_extension == ".obj"
    assert mirror_converter.output_extension == "_mirror.obj"

    stl2vtp_converter = STLToVTPConverter()
    assert stl2vtp_converter.input_extension == ".stl"
    assert stl2vtp_converter.output_extension == ".vtp"

    obj2stl_converter = OBJToSTLConverter()
    assert obj2stl_converter.input_extension == ".obj"
    assert obj2stl_converter.output_extension == ".stl"

    obj2vtp_converter = OBJToVTPConverter()
    assert obj2vtp_converter.input_extension == ".obj"
    assert obj2vtp_converter.output_extension == ".vtp"

    decimator = MeshDecimatorConverter()
    assert decimator.input_extension == ".vtp"
    assert decimator.output_extension == "_decimated.vtp"
    assert decimator.target_reduction == 0.5
