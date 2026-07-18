"""Command-line interface for OBJ mirroring."""

import argparse
from ..converters import OBJMirrorConverter


def main():
    """Main CLI function for OBJ mirroring."""
    parser = argparse.ArgumentParser(description="OBJ mirror")
    parser.add_argument("indir", help="Path to input directory.")
    parser.add_argument(
        "--outdir", "-o", default="output", help="Path to output directory."
    )
    parser.add_argument(
        "--axis", "-a", default="X", help="Axis to mirror along (X/Y/Z)"
    )
    args = parser.parse_args()

    converter = OBJMirrorConverter(mirror_axis=args.axis.upper())
    return converter.convert_directory(args.indir, args.outdir)


if __name__ == "__main__":
    main()
