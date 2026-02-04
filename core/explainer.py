def explain_clause(text):
    text = text.lower()

    if "indemnify" in text:
        return "You may be responsible for paying losses or damages, even if the issue is not fully your fault."

    if "terminate" in text:
        return "This clause explains when and how the contract can be ended."

    if "non-compete" in text:
        return "This may restrict you from doing similar business after the contract ends."

    if "jurisdiction" in text:
        return "This decides which location’s courts or laws will handle disputes."

    return "This clause defines standard responsibilities under the contract."


def suggest_alternative(text):
    text = text.lower()

    if "indemnify" in text:
        return "Consider limiting liability to the total contract value instead of unlimited responsibility."

    if "termination" in text:
        return "Ensure both parties have equal termination rights with reasonable notice."

    if "non-compete" in text:
        return "Limit the non-compete period and scope to what is strictly necessary."

    return "No alternative needed for this clause."
