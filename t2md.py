#!/usr/bin/env python3
"""T2MD — Command-line entry point."""

import sys
import argparse
import os
from engine import convert, convert_batch   # ← 新增 convert_batch


def main():
    parser = argparse.ArgumentParser(
        description="T2MD — Text to Markdown Converter",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("src", help="输入文件或目录路径")
    parser.add_argument("dst", nargs="?", default="output",
                        help="输出目录 (默认: output)")
    
    # 批量模式参数
    parser.add_argument("--batch", "-b", action="store_true",
                        help="启用批量处理模式（支持10万份文件）")
    parser.add_argument("--workers", "-w", type=int, default=None,
                        help="并行工作进程数（默认：CPU核心数的一半）")
    parser.add_argument("--recursive", "-r", action="store_true", default=True,
                        help="递归处理子目录（批量模式默认开启）")

    args = parser.parse_args()

    print("=" * 50)
    print("[T2MD] 🚀 T2MD — Text to Markdown Converter")
    print("=" * 50)

    try:
        if args.batch:
            # 批量模式
            print(f"[T2MD] Batch mode enabled (workers: {args.workers or 'auto'})")
            result = convert_batch(
                src_path=args.src,
                output_dir=args.dst,
                max_workers=args.workers,
                recursive=args.recursive
            )
            print(f"[T2MD] ✅ Batch completed! Total: {result['total']:,} | "
                  f"Success: {result['success']:,} | Failed: {result['failed']:,}")
        else:
            # 单文件 / 普通模式
            if not os.path.exists(args.src):
                print(f"[T2MD] ❌ Error: file or directory not found -> {args.src}")
                sys.exit(1)

            markdown = convert(args.src, args.dst)
            print(f"[T2MD] ✅ Done ✓  (output saved to {args.dst})")

    except Exception as e:
        print(f"[T2MD] ❌ Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
