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

def GetPointId(point,list):
    for i,pts in enumerate(list):
        if pts[0] == point[0] and pts[1] == point[1] and pts[2] == point[2] :
            #obj start to count at 1
            return i+1
    list.append(point)
    #obj start to count at 1
    return len(list)

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
        objfilename = filepath+".obj"
        
        pointList = []
        facetList = []

        # start reading the STL file
        stlfile = open(filepath, "r")
        line = stlfile.readline()
        line = stlfile.readline()
        lineNb = 1
        while line != "":
            tab = line.strip().split()       
            if len(tab) > 0:
                if "facet" in tab[0]:
                    vertices = []
                    normal = map(float,tab[2:])
                    while "endfacet" not in tab[0]:
                        if "vertex" in tab[0]:
                            pts = list(map(float,tab[1:]))
                            vertices.append(GetPointId(pts,pointList))
                        line = stlfile.readline()
                        lineNb = lineNb +1
                        tab = line.strip().split()        
                    if len(vertices) == 0:
                        print_error("Unvalid facet description at line ",lineNb)
                    facetList.append({"vertices":vertices, "normal": normal})

            line = stlfile.readline()
            lineNb = lineNb +1    

        stlfile.close()

        # Write the target file
        objfile = open(objfilename, "w")
        objfile.write("# File type: ASCII OBJ\n")
        objfile.write("# Generated from "+os.path.basename(filepath)+"\n")
        for pts in pointList:
            objfile.write("v "+" ".join(list(map(str,pts)))+"\n")

        for f in facetList:
            objfile.write("f "+" ".join(list(map(str,f["vertices"])))+"\n")

        objfile.close()
        return 1
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="STL to OBJ converter")
    parser.add_argument('indir', help="Path to input directory.")
    parser.add_argument('--outdir', '-o', default='output', help="Path to output directory.")
    parser.set_defaults(func=run)
    args = parser.parse_args()
    ret = args.func(args)