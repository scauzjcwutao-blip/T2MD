"""Bilingual UI strings (English / German)."""

TEXTS = {
    "en": {
        "author": "Author",
        "date": "Date",
        "category": "Category",
        "source": "Source",
        "processing": "Processing",
        "done": "Done",
        "error": "Error",
        "skipped": "Skipped",
        "watching": "Watching directory",
        "no_files": "No supported files found",
        "converted": "Converted",
        "files_processed": "files processed",
        "output_dir": "Output directory",
        "select_src": "Select Source",
        "select_dst": "Select Destination",
        "start": "Start Conversion",
        "language": "Language",
        "recursive": "Include subdirectories",
        "status": "Status",
        "ready": "Ready",
        "converting": "Converting…",
        "complete": "Conversion complete",
    },
    "de": {
        "author": "Autor",
        "date": "Datum",
        "category": "Kategorie",
        "source": "Quelle",
        "processing": "Verarbeitung",
        "done": "Fertig",
        "error": "Fehler",
        "skipped": "Übersprungen",
        "watching": "Verzeichnis wird überwacht",
        "no_files": "Keine unterstützten Dateien gefunden",
        "converted": "Konvertiert",
        "files_processed": "Dateien verarbeitet",
        "output_dir": "Ausgabeverzeichnis",
        "select_src": "Quelle wählen",
        "select_dst": "Ziel wählen",
        "start": "Konvertierung starten",
        "language": "Sprache",
        "recursive": "Unterverzeichnisse einbeziehen",
        "status": "Status",
        "ready": "Bereit",
        "converting": "Konvertiere…",
        "complete": "Konvertierung abgeschlossen",
    },
}


def get_text(key: str, lang: str = "en") -> str:
    """Return a UI string for *key* in the given language."""
    return TEXTS.get(lang, TEXTS["en"]).get(key, key)
