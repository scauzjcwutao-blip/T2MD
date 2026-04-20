"""T2MD — Command-line entry point."""

import sys
import os
from engine.pipeline import convert


def main():
    if len(sys.argv) < 2:
        print("Usage: python t2md.py <file_path> [output_dir]")
        print()
        print("Examples:")
        print("  python t2md.py input/notes.txt")
        print("  python t2md.py input/paper.pdf output/")
        print("  python t2md.py input/report.docx")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"

    if not os.path.exists(input_path):
        print(f"Error: file not found -> {input_path}")
        sys.exit(1)

    print("=" * 40)
    print("  T2MD — Text to Markdown Converter")
    print("=" * 40)

    convert(input_path, output_dir)

    print("=" * 40)
    print("Done ✓")


if __name__ == "__main__":
    main()
