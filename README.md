# t2md — Text-to-Markdown Converter & Data Classifier

A Python CLI tool that converts various document formats into clean
Markdown files, with automatic content classification and structured output.

## Features

- **Multi-format support**: PDF, DOCX, TXT, CSV, XLSX, HTML, PPTX, JSON, XML, RTF
- **Automatic classification**: Categorizes content into predefined categories
- **Table extraction**: Detects and converts tables to Markdown format
- **Batch processing**: Process entire directories at once
- **Metadata extraction**: Extracts author, date, title when available
- **Watch mode**: Monitor a directory and convert new files automatically
- **Bilingual UI**: English and German interface
- **UTF-8 / CJK support**: Full support for Chinese, Japanese, Korean text

## Project Structure
```text
t2md/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── t2md.py
├── t2md_gui.py
├── engine/
│   ├── __init__.py
│   ├── lang.py
│   ├── pipeline.py
│   └── classifier.py
├── output/
│   └── .gitkeep
└── input/
    └── .gitkeep
```
## Installation

```bash
git clone https://github.com/yourusername/t2md.git
cd t2md
pip install -e .
```
## Usage

### CLI

```bash
t2md --src ./input --dst ./output
t2md --src ./input --dst ./output --lang de --recursive
t2md --src ./input --dst ./output --watch
t2md --help
``` 
### GUI
```bash
t2md-gui
```
## Demo

https://github.com/user-attachments/assets/8ce75598-cf4c-46b9-acdb-d735b3fe7dec
```
