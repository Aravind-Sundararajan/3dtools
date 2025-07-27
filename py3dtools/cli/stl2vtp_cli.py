"""Command-line interface for STL to VTP conversion."""

import argparse
from ..converters import STLToVTPConverter


def main():
    """Main CLI function for STL to VTP conversion."""
    parser = argparse.ArgumentParser(description="STL to VTP converter")
    parser.add_argument('indir', help="Path to input directory.")
    parser.add_argument('--outdir', '-o', default='output',
                        help="Path to output directory.")
    args = parser.parse_args()

    converter = STLToVTPConverter()
    return converter.convert_directory(args.indir, args.outdir)


if __name__ == '__main__':
    main()
