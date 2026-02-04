"""app.py — Streamlit demo entrypoint for Contract Risk Bot

Run: streamlit run app.py
"""

import streamlit as st
from core.loader import load_contract
from core.classifier import classify_contract
from core.clause_extractor import extract_clauses
from core.risk_engine import assess_risk, calculate_overall_risk
from core.explainer import explain_clause, suggest_alternative

def business_impact(risk):
    if risk == "HIGH":
        return "Very High Impact on Business"
    elif risk == "MEDIUM":
        return "Moderate Business Impact"
    else:
        return "Low Business Impact"

st.set_page_config(page_title="Contract Risk Bot")
st.title("📄 Contract Analysis & Risk Assessment Bot")

with st.expander("❓ Help & Documentation"):
    st.markdown("""
### How to Use This Tool
1. Upload a contract (PDF, DOCX, or TXT)
2. Review the overall risk score
3. Focus on the **Top Business Risks**
4. Read plain-English explanations
5. Use safer alternatives during negotiation

### Supported Contract Types
- Employment Agreements  
- Vendor / Service Contracts  
- Lease Agreements  
- NDAs & Confidentiality Agreements  

### Risk Levels Explained
- 🔴 **HIGH** – Critical business or legal risk  
- 🟡 **MEDIUM** – Needs attention before signing  
- 🟢 **LOW** – Standard or acceptable clause  

### Disclaimer
This tool provides **risk insights only** and does not replace professional legal advice.
""")

with st.expander("⚙️ Preferences"):
    risk_mode = st.radio(
        "Risk Sensitivity",
        ["Conservative", "Balanced", "Aggressive"],
        index=1
    )

file = st.file_uploader("Upload contract", type=["pdf", "docx", "txt"])

if file:
    text = load_contract(file)

    st.subheader("Contract Type")
    st.success(classify_contract(text))

    st.subheader("Clause Risk Analysis")
    clauses = extract_clauses(text)

    analyzed_clauses = []
    for clause in clauses:
        risk = assess_risk(clause["text"], risk_mode)
        analyzed_clauses.append({
            "id": clause["id"],
            "text": clause["text"],
            "risk": risk
        })

    score, level = calculate_overall_risk(analyzed_clauses)

    st.subheader("📊 Overall Contract Risk")
    st.metric("Risk Score", f"{score} / 100", level)

    st.subheader("🚨 Top Business Risks (Priority Order)")

    priority = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_clauses = sorted(
        analyzed_clauses,
        key=lambda x: priority[x["risk"]]
    )

    for clause in sorted_clauses[:5]:
        if clause["risk"] == "HIGH":
            st.error(f"{clause['id']} — HIGH RISK")
        elif clause["risk"] == "MEDIUM":
            st.warning(f"{clause['id']} — MEDIUM RISK")
        else:
            st.success(f"{clause['id']} — LOW RISK")

        with st.expander(f"{clause['id']} — {clause['risk']} risk"):
            st.write("📜 **Clause Text:**")
            st.write(clause["text"])

            st.write("🧠 **What this means:**")
            st.info(explain_clause(clause["text"]))

            st.write("📊 **Business Impact:**")
            st.info(business_impact(clause["risk"]))

            if clause["risk"] != "LOW":
                st.write("🛠️ **Safer Alternative Suggestion:**")
                st.warning(suggest_alternative(clause["text"]))

        st.divider()

    st.subheader("📝 Negotiation Checklist")
    for clause in sorted_clauses:
        if clause["risk"] == "HIGH":
            st.checkbox(
                f"Fix HIGH risk clause: {clause['id']}",
                value=False
            )

    if st.button("📥 Download Summary"):
        summary = f"Risk Score: {score}/100\nOverall Level: {level}\n\n"
        checklist_items = []
        for c in sorted_clauses[:5]:
            summary += f"{c['id']} - {c['risk']}\n"
            summary += f"Text: {c['text']}\n"
            summary += f"Business Impact: {business_impact(c['risk'])}\n"
            if c['risk'] != 'LOW':
                suggestion = suggest_alternative(c['text'])
                summary += f"Suggestion: {suggestion}\n"
            if c['risk'] == 'HIGH':
                checklist_items.append(f"Fix HIGH risk clause: {c['id']}")
            summary += "\n"

        if checklist_items:
            summary += "Negotiation Checklist:\n"
            for item in checklist_items:
                summary += f"- {item}\n"

        st.download_button(
            "Download Report",
            summary,
            file_name="contract_risk_summary.txt"
        )

