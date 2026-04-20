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
