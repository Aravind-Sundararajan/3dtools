import sys      
import string   
import os.path  
import getopt
import argparse

def convertFiles(indir, outdir, mirdir):

    M = [1, 1, 1]
    if mirdir == "X":
        M[0] = -1
    elif mirdir == "Y":
        M[1] = -1
    elif mirdir == "Z":
        M[2] = -1
    else:
        pass
        
    files = os.listdir(indir)
    files = [ os.path.join(indir,f) for f in files if f.endswith('.obj') ]
    ret = 0
    print("In:", indir)
    print("Out:", outdir)
    for f in files:
        print(f)
        ret += convertFile(f, outdir, M)
    print("Successfully mirrored %d out of %d files." % (ret, len(files)))

def run(args):
    convertFiles(args.indir, args.outdir, args.axis)

def print_help():
    print("Usage: "+os.path.basename(sys.argv[0])+" [OPTIONS] filein.obj")
    print("   Options: -o OUTDIR")
    print("               Write the output mesh in OUTPUT_FILE")
    print("               , create 3 points per facet)")
    sys.exit()

def print_error(*str):
    print("ERROR: "),
    for i in str:
        print(i),
    print("\n")
    sys.exit()

def GetPointId(point,pl):
    for i,pts in enumerate(pl):
        if pts == point :
            #obj start to count at 1
            return i+1
    pl.append(point)
    #obj start to count at 1
    return len(pl)

def convertFile(filepath, outdir, M):
    
    
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    if os.path.isfile(filepath):

        # verify the argument is an stl file
        if ".obj" not in filepath:
            print_error(filepath,": The file is not an .obj file.")
        if not os.path.exists(filepath):
            print_error(filepath,": The file doesn't exist.")

        # By default the output is the stl filename followed by '.obj'
        objfilename = filepath.replace(".obj","_Mirror.obj")
        
        facets = []
        vertices = []

        # start reading the STL file
        objfile = open(filepath, "r")
        line = objfile.readline()
        line = objfile.readline()
        lineNb = 1
        while line != "":
            tab = line.strip().split()       
            if len(tab) > 0:
                if "v" in tab[0]:
                    V = tuple(map(float,tab[1:]))
                    v_mir = [v*m for v,m in zip(V,M)]
                    vertices.append(v_mir)
                elif "f" in tab[0]:
                    facets.append(tuple(map(int,tab[1:])))
            line = objfile.readline()

        objfile.close()
        # Write the target file
        objfile = open(objfilename, "w")
        objfile.write("# File type: ASCII OBJ\n")
        objfile.write("# Generated from "+os.path.basename(filepath)+"\n")
        for pts in vertices:
            objfile.write("v "+" ".join(list(map(str,pts)))+"\n")

        for facet in facets:
            objfile.write("f "+" ".join(list(map(str,facet)))+"\n")

        objfile.close()
        return 1
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="OBJ mirror")
    parser.add_argument('indir', help="Path to input directory.")
    parser.add_argument('--outdir', '-o', default='output', help="Path to output directory.")
    parser.add_argument('--axis', '-a', default='none', help="axis (X/Y/Z)")
    parser.set_defaults(func=run)
    args = parser.parse_args()
    ret = args.func(args)
    #convertFiles("./.", "./.")