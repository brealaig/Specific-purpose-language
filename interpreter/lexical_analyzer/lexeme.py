import re

TOKEN_PATTERNS = [
    ("COMMENT", re.compile(r"//.*")),
    ("WHITESPACE", re.compile(r"\s+")),
    ("KEYWORD", re.compile(r"\b(recipe|input|output|tool_required|quantity|func|if|else|while|for|craft|log|int|float|char|return)\b")),
    ("NUMBER", re.compile(r"(?<!\d)-?\d+(\.\d+)?\b")),  # Ajustado para evitar capturar '-' en expresiones sin espacio
    ("STRING", re.compile(r'\"[^\"]*\"')),
    ("IDENTIFIER", re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b")),
    ("SYMBOL", re.compile(r"[{}\[\]:,;()]")),
    ("OPERATOR", re.compile(r"[=+*/<>!%\-]{1,2}")),
]

