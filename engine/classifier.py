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
        engine = "rules"  # default fallback for unknown extensions

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
        # Chinese
        "收入", "利润", "亏损", "预算", "税收", "投资", "资产", "负债",
        "现金流", "财务", "会计", "银行", "贷款", "利率", "股票", "债券",
    ],
    "technology": [
        "software", "hardware", "algorithm", "database", "api",
        "server", "cloud", "programming", "code", "developer",
        "machine learning", "artificial intelligence", "neural",
        "python", "javascript", "framework", "deployment",
        # German
        "Algorithmus", "Datenbank", "Programmierung", "Entwickler",
        # Chinese / Japanese / Korean common terms
        "软件", "硬件", "算法", "数据库", "服务器", "云计算",
        "编程", "代码", "人工智能", "机器学习", "神经网络",
        "ソフト", "ハードウェア", "アルゴリズム", "データベース",
    ],
    "legal": [
        "contract", "agreement", "clause", "liability", "compliance",
        "regulation", "law", "court", "plaintiff", "defendant",
        "attorney", "legal", "jurisdiction", "statute", "legislation",
        # German
        "Vertrag", "Vereinbarung", "Gesetz", "Gericht", "Recht",
        # Chinese
        "合同", "协议", "条款", "责任", "合规", "法规", "法律",
        "法院", "原告", "被告", "律师", "管辖权",
    ],
    "medical": [
        "patient", "diagnosis", "treatment", "symptom", "disease",
        "hospital", "doctor", "medicine", "clinical", "therapy",
        "surgery", "prescription", "health", "medical", "pharmaceutical",
        # German
        "Patient", "Diagnose", "Behandlung", "Krankenhaus", "Arzt",
        # Chinese
        "患者", "诊断", "治疗", "症状", "疾病", "医院", "医生",
        "药物", "临床", "手术", "处方", "健康",
    ],
    "education": [
        "student", "teacher", "curriculum", "course", "lecture",
        "university", "school", "education", "exam", "grade",
        "research", "academic", "study", "learning", "training",
        # German
        "Schüler", "Lehrer", "Universität", "Schule", "Bildung",
        # Chinese
        "学生", "教师", "课程", "大学", "学校", "教育", "考试",
        "研究", "学术", "学习",
    ],
    "marketing": [
        "campaign", "brand", "customer", "market", "advertising",
        "promotion", "sales", "target audience", "conversion",
        "engagement", "social media", "seo", "content marketing",
        # German
        "Kampagne", "Marke", "Kunde", "Werbung", "Verkauf",
        # Chinese
        "营销", "品牌", "客户", "市场", "广告", "推广", "销售",
        "社交媒体", "内容营销",
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
