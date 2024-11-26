import sys
import os.path
import argparse


def convert_file(filepath, outdir, mirror_axis) -> bool:
    """
    Converts a single OBJ file by mirroring it along the specified axis and
    writes the result to a new file in the specified output directory.

    Args:
        filepath: The path to the input OBJ file.
        outdir: The directory where the output file should be written.
        mirror_axis: The axis along which the file should be mirrored (either
        "X", "Y", or "Z").

    Returns:
        True if the file was successfully converted and written to disk, False otherwise.
    """
    if not os.path.isfile(filepath):
        print(f"ERROR: The file {filepath} doesn't exist.")
        return False
    if not filepath.endswith('.obj'):
        print(f"ERROR: {filepath} is not an OBJ file.")
        return False

    # By default, the output filename is the input filename with "_Mirror" appended
    objfilename = os.path.basename(filepath).replace(".obj", "_Mirror.obj")
    outpath = os.path.join(outdir, objfilename)

    # Read the input file
    vertices = []
    faces = []
    with open(filepath, "r") as f:
        for line in f:
            tokens = line.strip().split()
            if len(tokens) == 0:
                continue
            if tokens[0] == "v":
                vertices.append([float(x) for x in tokens[1:]])
            elif tokens[0] == "f":
                faces.append([int(x.split("/")[0]) for x in tokens[1:]])

    # Mirror the vertices along the specified axis
    mirror_sign = [-1 if axis == mirror_axis.upper() else 1 for axis in "XYZ"]
    mirrored_vertices = [[mirror_sign[i] * v[i]
                          for i in range(3)] for v in vertices]

    # Write the output file
    with open(outpath, "w") as f:
        f.write("# File type: ASCII OBJ\n")
        f.write("# Generated from " + os.path.basename(filepath) + "\n")
        for v in mirrored_vertices:
            f.write("v " + " ".join(str(x) for x in v) + "\n")
        for face in faces:
            f.write("f " + " ".join(str(x) for x in face) + "\n")

    return True


def convert_files(indir, outdir, mirror_axis) -> int:
    """
    Converts all OBJ files in a specified directory by mirroring it along the specified axis and
    writes the result to a new file in the specified output directory.

    Args:
        indir: the directory where the input files are read.
        outdir: The directory where the output file should be written.
        mirror_axis: The axis along which the file should be mirrored (either
        "X", "Y", or "Z").

    Returns:
        1 if the file was successfully converted and written to disk, 0 otherwise.
    """
    if not os.path.isdir(indir):
        print(f"ERROR: The input directory {indir} doesn't exist.")
        return 0

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    count = 0
    for filename in os.listdir(indir):
        if filename.endswith('_Mirror.obj'):
            continue
        if not filename.endswith('.obj'):
            continue
        filepath = os.path.join(indir, filename)
        if convert_file(filepath, outdir, mirror_axis):
            count += 1

    print(
        f"Successfully mirrored {count} out of {len(os.listdir(indir))} files.")
    return count


def main():
    parser = argparse.ArgumentParser(description="OBJ mirror")
    parser.add_argument('indir', help="Path to input directory.")
    parser.add_argument('--outdir', '-o', default='output',
                        help="Path to output directory.")
    parser.add_argument('--axis', '-a', default='none', help="axis (X/Y/Z)")
    args = parser.parse_args()
    convert_files(args.indir, args.outdir, args.axis.upper())


if __name__ == '__main__':
    main()
