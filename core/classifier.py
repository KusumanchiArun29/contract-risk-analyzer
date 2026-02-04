def classify_contract(text):
    text = text.lower()

    if "employee" in text or "salary" in text:
        return "Employment Agreement"
    elif "lease" in text or "rent" in text:
        return "Lease Agreement"
    elif "vendor" in text or "services" in text:
        return "Service / Vendor Contract"
    elif "partnership" in text:
        return "Partnership Deed"
    else:
        return "General Contract"
