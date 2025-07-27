"""Command-line interface for STL to OBJ conversion."""

import argparse
from ..converters import STLToOBJConverter


def main():
    """Main CLI function for STL to OBJ conversion."""
    parser = argparse.ArgumentParser(description="STL to OBJ converter")
    parser.add_argument("indir", help="Path to input directory.")
    parser.add_argument(
        "--outdir", "-o", default="output", help="Path to output directory."
    )
    args = parser.parse_args()

    converter = STLToOBJConverter()
    return converter.convert_directory(args.indir, args.outdir)


if __name__ == '__main__':
    main()
