# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-04-20

### Added
- Dual-engine architecture: Docling + rules-based converter
- Document classifier (`classifier.py`) — routes files to the correct engine
- Language detection (`lang.py`)
- Rules engine (`rules.py`) — plain text to Markdown
- Docling engine (`docling_converter.py`) — PDF/Word/HTML to Markdown
- Conversion pipeline (`pipeline.py`)
- CLI entry point (`t2md.py`)
- GUI entry point (`t2md_gui.py`) — placeholder
- Test suite (`tests/`)
