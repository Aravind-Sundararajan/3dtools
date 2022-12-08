import sys      
import string   
import os.path  
import getopt
import argparse

def convertFiles(indir, outdir):
    files = os.listdir(indir)
    files = [ os.path.join(indir,f) for f in files if f.endswith('.stl') ]
    ret = 0
    print("In:", indir)
    print("Out:", outdir)
    for f in files:
        print(f)
        ret += convertFile(f, outdir)
    print("Successfully converted %d out of %d files." % (ret, len(files)))

def run(args):
    convertFiles(args.indir, args.outdir)

def print_help():
    print("Usage: "+os.path.basename(sys.argv[0])+" [OPTIONS] filein.stl")
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

def convertFile(filepath, outdir):
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    if os.path.isfile(filepath):

        # verify the argument is an stl file
        if ".stl" not in filepath:
            print_error(filepath,": The file is not an .stl file.")
        if not os.path.exists(filepath):
            print_error(filepath,": The file doesn't exist.")

        # By default the output is the stl filename followed by '.obj'
        objfilename = filepath.replace(".stl",".obj")
        
        points = []
        facets = []
        normals = []

        # start reading the STL file
        stlfile = open(filepath, "r")
        line = stlfile.readline()
        line = stlfile.readline()
        lineNb = 1
        while line != "":
            vertices = []
            tab = line.strip().split()       
            if len(tab) > 0:
                if "facet" in tab[0]:
                    normal = tuple(map(float,tab[2:]))
                    normals.append(normal)
                    while "endfacet" not in tab[0]:
                        if "vertex" in tab[0]:
                            v = tuple(map(float,tab[1:]))
                            points.append(v)
                            vertices.append(v)
                        line = stlfile.readline()
                        lineNb = lineNb +1
                        tab = line.strip().split()     
                    facets.append(vertices)
            line = stlfile.readline()
            lineNb = lineNb +1    

        stlfile.close()
        setpts = list(set(points))
        sp = setpts
        #sp = [pt for pt in points if pt in setpts]
        facet_map = [list(map(lambda v: sp.index(v) + 1, f)) for f in facets]
        # Write the target file
        objfile = open(objfilename, "w")
        objfile.write("# File type: ASCII OBJ\n")
        objfile.write("# Generated from "+os.path.basename(filepath)+"\n")
        for pts in sp:
            objfile.write("v "+" ".join(list(map(str,pts)))+"\n")

        for facet in facet_map:
            objfile.write("f "+" ".join(list(map(str,facet)))+"\n")

        objfile.close()
        return 1
    return False

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="STL to OBJ converter")
    # parser.add_argument('indir', help="Path to input directory.")
    # parser.add_argument('--outdir', '-o', default='output', help="Path to output directory.")
    # parser.set_defaults(func=run)
    # args = parser.parse_args()
    # ret = args.func(args)
    convertFiles("./.", "./.")