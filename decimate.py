import argparse
import os
import trimesh

def decimate_meshes(directory, max_vertices):
    for filename in os.listdir(directory):
        if filename.endswith('.obj') and 'decimated' not in filename:
            print("converting " + filename)
            # Load the original mesh
            mesh = trimesh.load(os.path.join(directory, filename))
            # Decimate the mesh to have fewer than max_vertices vertices
            mesh_decimated = mesh.simplify_quadric_decimation(max_vertices)
            # Save the decimated mesh with a new filename
            new_filename = os.path.splitext(filename)[0] + '_decimated.obj'
            mesh_decimated.export(os.path.join(directory, new_filename))
            print(os.path.join(directory, new_filename))

if __name__ == '__main__':
    # Define command-line arguments
    parser = argparse.ArgumentParser(description='Decimate OBJ meshes in a directory')
    parser.add_argument('directory', type=str, help='The directory containing the meshes to decimate')
    parser.add_argument('max_vertices', type=int, help='The maximum number of vertices to allow in the decimated meshes')

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the decimate_meshes function with the parsed arguments
    decimate_meshes(args.directory, args.max_vertices)
