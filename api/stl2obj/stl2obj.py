import argparse
import os


def convert_files(indir: str, outdir: str) -> bool:
    """
    Converts all STL files in a directory to OBJ files and saves them to a specified directory.

    Args:
    indir (str): The path to the directory containing the STL files to convert.
    outdir (str): The path to the directory where the converted OBJ files should be saved.

    Returns:
    True when the conversion and saving are successful.
    """
    stl_files = [f for f in os.listdir(indir) if f.endswith(".stl")]
    print("In:", indir)
    print("Out:", outdir)
    num_converted_files = 0
    for file in stl_files:
        stl_file_path = os.path.join(indir, file)
        obj_file_path = os.path.join(outdir, file.replace(".stl", ".obj"))
        if os.path.isfile(stl_file_path):
            if not os.path.isdir(outdir):
                os.makedirs(outdir)
            if ".stl" not in file:
                print(stl_file_path, ": The file is not an .stl file.")
                continue
            if not os.path.exists(stl_file_path):
                print(stl_file_path, ": The file doesn't exist.")
                continue
            if os.path.exists(obj_file_path):
                print(
                    f"{obj_file_path} already exists, skipping conversion of {stl_file_path}")
                continue
            convert_file(stl_file_path, obj_file_path)
            num_converted_files += 1
    print(
        f"Successfully converted {num_converted_files} out of {len(stl_files)} files.")
    return True


def convert_file(stl_file_path: str, obj_file_path: str) -> bool:
    """
    Converts an STL file to an OBJ file.

    Args:
    stl_file_path (str): The path to the STL file to convert.
    obj_file_path (str): The path to the OBJ file where the converted file should be saved.

    Returns:
    True if the conversion and saving were successful.
    """
    points = []
    facets = []
    normals = []

    with open(stl_file_path, "r") as stl_file:
        for line in stl_file:
            tokens = line.strip().split()
            if not tokens:
                continue
            if tokens[0] == "facet":
                normal = tuple(map(float, tokens[2:]))
                normals.append(normal)
                vertices = []
                while True:
                    line = stl_file.readline().strip().split()
                    if not line:
                        continue
                    if line[0] == "endfacet":
                        break
                    if line[0] == "vertex":
                        vertex = tuple(map(float, line[1:]))
                        points.append(vertex)
                        vertices.append(vertex)
                facets.append(vertices)

    with open(obj_file_path, "w") as obj_file:
        obj_file.write("# File type: ASCII OBJ\n")
        obj_file.write(f"# Generated from {stl_file_path}\n")
        for pt in set(points):
            obj_file.write(f"v {' '.join(map(str, pt))}\n")
        for facet in facets:
            indices = []
            for pt in facet:
                index = points.index(pt) + 1
                indices.append(str(index))
            obj_file.write(f"f {' '.join(indices)}\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="STL to OBJ converter")
    parser.add_argument("indir", help="Path to input directory.")
    parser.add_argument(
        "--outdir", "-o", default="output", help="Path to output directory."
    )
    args = parser.parse_args()
    convert_files(args.indir, args.outdir)


if __name__ == "__main__":
    main()
