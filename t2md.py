#!/usr/bin/env python3
"""t2md — CLI entry point."""

import os
import sys
import time
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table as RichTable
from rich.progress import track
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from engine.pipeline import convert_file, SUPPORTED_EXTENSIONS
from engine.lang import get_text

console = Console()


class NewFileHandler(FileSystemEventHandler):
    """Watches a directory and converts new files automatically."""

    def __init__(self, output_dir, lang):
        self.output_dir = output_dir
        self.lang = lang

    def on_created(self, event):
        if event.is_directory:
            return
        ext = Path(event.src_path).suffix.lower()
        if ext in SUPPORTED_EXTENSIONS:
            console.print(
                f"[cyan]{get_text('processing', self.lang)}:[/] {event.src_path}"
            )
            try:
                result = convert_file(event.src_path, self.output_dir, self.lang)
                if result:
                    console.print(
                        f"[green]{get_text('converted', self.lang)}:[/] {result}"
                    )
                else:
                    console.print(
                        f"[yellow]{get_text('skipped', self.lang)}:[/] {event.src_path}"
                    )
            except Exception as e:
                console.print(
                    f"[red]{get_text('error', self.lang)}:[/] {e}"
                )


def collect_files(src_path, recursive=False):
    """Collect all supported files from a path."""
    path = Path(src_path)
    files = []

    if path.is_file():
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    elif path.is_dir():
        pattern = "**/*" if recursive else "*"
        for ext in SUPPORTED_EXTENSIONS:
            files.extend(path.glob(f"{pattern}{ext}"))

    return sorted(set(files))


@click.command()
@click.option("--src", required=True, help="Source file or directory")
@click.option("--dst", default="./output", help="Destination directory")
@click.option(
    "--lang",
    default="en",
    type=click.Choice(["en", "de"]),
    help="Interface language",
)
@click.option("--recursive", is_flag=True, help="Process subdirectories")
@click.option(
    "--watch", is_flag=True, help="Watch mode — monitor directory for new files"
)
def main(src, dst, lang, recursive, watch):
    """t2md — Convert documents to Markdown with automatic classification."""

    os.makedirs(dst, exist_ok=True)

    # ── Watch mode ──────────────────────────────────────────────
    if watch:
        if not Path(src).is_dir():
            console.print(
                f"[red]{get_text('error', lang)}:[/] --watch requires a directory as --src"
            )
            sys.exit(1)

        console.print(f"[bold cyan]{get_text('watching', lang)}:[/] {src}")
        console.print("Press Ctrl+C to stop.\n")

        handler = NewFileHandler(dst, lang)
        observer = Observer()
        observer.schedule(handler, src, recursive=recursive)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        return

    # ── Batch mode ──────────────────────────────────────────────
    files = collect_files(src, recursive)

    if not files:
        console.print(f"[yellow]{get_text('no_files', lang)}[/]")
        return

    results = RichTable(title="t2md")
    results.add_column("File", style="cyan")
    results.add_column("Status", style="green")
    results.add_column("Output", style="dim")

    success = 0
    errors = 0

    for f in track(files, description=get_text("processing", lang)):
        try:
            result = convert_file(str(f), dst, lang)
            if result:
                results.add_row(f.name, f"✅ {get_text('done', lang)}", result)
                success += 1
            else:
                results.add_row(f.name, f"⏭️  {get_text('skipped', lang)}", "—")
        except Exception as e:
            results.add_row(f.name, f"❌ {get_text('error', lang)}", str(e))
            errors += 1

    console.print()
    console.print(results)
    console.print(
        f"\n[bold green]{success}[/] {get_text('files_processed', lang)}", end=""
    )
    if errors:
        console.print(f" | [bold red]{errors}[/] {get_text('error', lang)}")
    else:
        console.print()


if __name__ == "__main__":
    main()
