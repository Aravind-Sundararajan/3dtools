"""Command-line interface for VTP to STL conversion."""

import argparse
from ..converters import VTPToSTLConverter


def main():
    """Main CLI function for VTP to STL conversion."""
    parser = argparse.ArgumentParser(description="VTP to STL converter")
    parser.add_argument('indir', help="Path to input directory.")
    parser.add_argument('--outdir', '-o', default='output',
                        help="Path to output directory.")
    args = parser.parse_args()

    converter = VTPToSTLConverter()
    return converter.convert_directory(args.indir, args.outdir)


if __name__ == '__main__':
    main()
