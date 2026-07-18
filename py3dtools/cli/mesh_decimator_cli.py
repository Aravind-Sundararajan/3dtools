"""Command-line interface for mesh decimation."""

import argparse
from ..converters import MeshDecimatorConverter


def main():
    """Main CLI function for mesh decimation."""
    parser = argparse.ArgumentParser(description="Mesh decimator")
    parser.add_argument("indir", help="Path to input directory.")
    parser.add_argument(
        "--outdir", "-o", default="output", help="Path to output directory."
    )
    parser.add_argument(
        "--reduction",
        "-r",
        type=float,
        default=0.5,
        help="Target reduction ratio (0.0 to 1.0, default: 0.5)",
    )
    parser.add_argument(
        "--preserve-topology",
        "-p",
        action="store_true",
        help="Preserve mesh topology during decimation",
    )
    args = parser.parse_args()

    converter = MeshDecimatorConverter(
        target_reduction=args.reduction, preserve_topology=args.preserve_topology
    )
    return converter.convert_directory(args.indir, args.outdir)


if __name__ == "__main__":
    main()
