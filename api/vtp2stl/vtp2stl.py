import os
import vtk
import argparse

import os
import vtk


def convert_file(filepath, outdir) -> bool:
    """
    Converts a VTK XML file to an STL file and saves it to a specified directory.

    Args:
    filepath (str): The path to the VTK XML file to convert.
    outdir (str): The path to the directory where the converted STL file should be saved.

    Returns:
    bool: True if the conversion and saving were successful, False otherwise.
    """
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    if os.path.isfile(filepath):
        basename = os.path.basename(filepath)
        print(f"Copying file: {basename}")
        basename = os.path.splitext(basename)[0]
        outfile = os.path.join(outdir, f"{basename}.stl")
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(filepath)
        reader.Update()
        writer = vtk.vtkSTLWriter()
        writer.SetInputConnection(reader.GetOutputPort())
        writer.SetFileName(outfile)
        return writer.Write() == 1
    return False


def convert_files(indir, outdir) -> int:
    """
    Converts all VTK XML files in a directory to STL files and saves them to a specified directory.

    Args:
    indir (str): The path to the directory containing the VTK XML files to convert.
    outdir (str): The path to the directory where the converted STL files should be saved.

    Returns:
    True when the conversion and saving are successful.
    """
    files = [os.path.join(indir, f)
             for f in os.listdir(indir) if f.endswith('.vtp')]
    success_count = 0
    print(f"In: {indir}")
    print(f"Out: {outdir}")
    for f in files:
        success_count += convert_file(f, outdir)
    print(f"Successfully converted {success_count} out of {len(files)} files.")
    return success_count


def run(args):
    convert_files(args.indir, args.outdir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="VTP to STL converter")
    parser.add_argument('indir', help="Path to input directory.")
    parser.add_argument('--outdir', '-o', default='output',
                        help="Path to output directory.")
    parser.set_defaults(func=run)
    args = parser.parse_args()
    ret = args.func(args)
