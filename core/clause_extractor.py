import re
from typing import List, Dict


def extract_clauses(text: str) -> List[Dict]:
    """
    Very simple clause splitter: matches blocks starting with a number + dot (e.g., '1. Termination').
    Returns list of dicts: {'id': '1', 'text': 'Termination\nEither party...'}
    """
    pattern = r"(?m)^\s*(\d+)\.\s*(.+?)(?=\n\s*\d+\.|\Z)"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    clauses = []
    for num, body in matches:
        clauses.append({
            "id": num,
            "text": body.strip()
        })

    # Fallback: if no numbered clauses detected, treat whole text as single clause
    if not clauses and text.strip():
        clauses = [{"id": "1", "text": text.strip()}]

    return clauses
