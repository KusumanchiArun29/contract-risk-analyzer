import json

with open("rules/risk_rules.json") as f:
    RULES = json.load(f)

RISK_SCORES = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}

def assess_risk(text, mode="Balanced"):
    text = text.lower()

    high_hits = sum(1 for w in RULES["high"] if w in text)
    medium_hits = sum(1 for w in RULES["medium"] if w in text)

    if mode == "Conservative":
        if high_hits >= 1 or medium_hits >= 1:
            return "HIGH"
    elif mode == "Aggressive":
        if high_hits >= 2:
            return "HIGH"
    else:  # Balanced
        if high_hits >= 1:
            return "HIGH"
        if medium_hits >= 1:
            return "MEDIUM"

    return "LOW"


def calculate_overall_risk(clauses):
    total = 0
    for c in clauses:
        total += RISK_SCORES[c["risk"]]

    max_score = len(clauses) * 3
    percentage = int((total / max_score) * 100) if clauses else 0

    if percentage >= 65:
        level = "HIGH"
    elif percentage >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return percentage, level
