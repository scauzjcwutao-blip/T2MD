"""Simple keyword-based content classifier."""

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
    """Return the best-matching category for *text*, or 'general'."""
    text_lower = text.lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        score = sum(text_lower.count(kw.lower()) for kw in keywords)
        scores[category] = score

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else DEFAULT_CATEGORY
