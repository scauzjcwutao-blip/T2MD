"""Document classifier — keyword-based content classification + file-type routing."""

import os

# ──────────────────────────────────────────────
# Part 1: File-type classification (engine routing)
# ──────────────────────────────────────────────

DOCLING_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".pptx",
    ".html", ".htm", ".png", ".jpg", ".jpeg",
}

RULES_EXTENSIONS = {
    ".txt", ".text", ".log", ".rst",
}

TABLE_EXTENSIONS = {
    ".csv", ".xlsx", ".xls",
}

DATA_EXTENSIONS = {
    ".json", ".xml",
}

RTF_EXTENSIONS = {
    ".rtf",
}


def classify(file_path: str) -> dict:
    """
    Classify a file and decide which conversion engine to use.

    Returns:
        {
            "engine": "docling" | "rules" | "table" | "data" | "rtf",
            "ext": ".pdf",
            "filename": "example.pdf"
        }
    """
    ext = os.path.splitext(file_path)[1].lower()
    filename = os.path.basename(file_path)

    if ext in DOCLING_EXTENSIONS:
        engine = "docling"
    elif ext in TABLE_EXTENSIONS:
        engine = "table"
    elif ext in DATA_EXTENSIONS:
        engine = "data"
    elif ext in RTF_EXTENSIONS:
        engine = "rtf"
    elif ext in RULES_EXTENSIONS or ext == "":
        engine = "rules"
    else:
        engine = "rules"  # default fallback

    return {
        "engine": engine,
        "ext": ext,
        "filename": filename,
    }


# ──────────────────────────────────────────────
# Part 2: Keyword-based content classification
# ──────────────────────────────────────────────

CATEGORIES = {
    "finance": [
        "revenue", "profit", "loss", "income", "expense", "budget",
        "tax", "investment", "dividend", "asset", "liability",
        "balance sheet", "cash flow", "financial", "accounting",
        "bank", "loan", "interest rate", "stock", "bond",
        # German
        "Umsatz", "Gewinn", "Verlust", "Einkommen", "Ausgabe",
        "Steuer", "Investition", "Bilanz", "Finanzen",
    ],
    "technology": [
        "software", "hardware", "algorithm", "database", "api",
        "server", "cloud", "programming", "code", "developer",
        "machine learning", "artificial intelligence", "neural",
        "python", "javascript", "framework", "deployment",
        "Algorithmus", "Datenbank", "Programmierung", "Entwickler",
    ],
    "legal": [
        "contract", "agreement", "clause", "liability", "compliance",
        "regulation", "law", "court", "plaintiff", "defendant",
        "attorney", "legal", "jurisdiction", "statute", "legislation",
        "Vertrag", "Vereinbarung", "Gesetz", "Gericht", "Recht",
    ],
    "medical": [
        "patient", "diagnosis", "treatment", "symptom", "disease",
        "hospital", "doctor", "medicine", "clinical", "therapy",
        "surgery", "prescription", "health", "medical", "pharmaceutical",
        "Patient", "Diagnose", "Behandlung", "Krankenhaus", "Arzt",
    ],
    "education": [
        "student", "teacher", "curriculum", "course", "lecture",
        "university", "school", "education", "exam", "grade",
        "research", "academic", "study", "learning", "training",
        "Schüler", "Lehrer", "Universität", "Schule", "Bildung",
    ],
    "marketing": [
        "campaign", "brand", "customer", "market", "advertising",
        "promotion", "sales", "target audience", "conversion",
        "engagement", "social media", "seo", "content marketing",
        "Kampagne", "Marke", "Kunde", "Werbung", "Verkauf",
    ],
}

DEFAULT_CATEGORY = "general"


def classify_content(text: str) -> str:
    """
    Return the best-matching category for the given text.

    Returns:
        Category string (e.g. 'finance', 'technology', 'general').
    """
    if not text or not text.strip():
        return DEFAULT_CATEGORY

    text_lower = text.lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        score = sum(text_lower.count(kw.lower()) for kw in keywords)
        scores[category] = score

    # Find the highest score
    best = max(scores, key=scores.get)

    # Only return a category if there is at least one keyword match
    if scores[best] > 0:
        return best

    return DEFAULT_CATEGORY
