#!/usr/bin/env python
import os
import vtk
import argparse

def convert_file(filepath, outdir):
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

def convert_files(indir, outdir):
    files = [os.path.join(indir, f) for f in os.listdir(indir) if f.endswith('.vtp')]
    success_count = 0
    print(f"In: {indir}")
    print(f"Out: {outdir}")
    for f in files:
        success_count += convert_file(f, outdir)
    print(f"Successfully converted {success_count} out of {len(files)} files.")

def run(args):
    convert_files(args.indir, args.outdir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="VTP to STL converter")
    parser.add_argument('indir', help="Path to input directory.")
    parser.add_argument('--outdir', '-o', default='output', help="Path to output directory.")
    parser.set_defaults(func=run)
    args = parser.parse_args()
    ret = args.func(args)
