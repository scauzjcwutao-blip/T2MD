"""Docling engine — convert PDF/Word/HTML/images to Markdown."""

from docling.document_converter import DocumentConverter


def convert_by_docling(file_path: str) -> str:
    """
    Convert a document to Markdown using Docling.

    Supports: PDF, DOCX, PPTX, HTML, images.
    """
    try:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        markdown = result.document.export_to_markdown()
        return markdown
    except Exception as e:
        return f"<!-- Docling conversion failed: {e} -->\n"
