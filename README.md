# 🛡️ OmniAudit NIM
### Autonomous Enterprise Financial Forensics & Cost Anomaly Detection Engine

OmniAudit NIM is an autonomous agentic auditing framework designed to detect invoice fraud, phantom shell companies, and price gouging in enterprise supply chains. It unifies **agentic LLM reasoning**, **deterministic statistical regression (R² = 96.99%)**, and **real-time entity search grounding** into a unified verification engine with Explainable AI (XAI) risk attribution.

## ⚡ Key Capabilities
* **Multivariate Regression Grounding:** Benchmarks billed freight charges against a calibrated route-weight model (R² = 96.99%).
* **Real-Time Entity Radar:** Queries corporate registers, public debarment lists, and regulatory warnings via Tavily in parallel.
* **Explainable AI (XAI) Attribution:** Breaks down a composite 0–100 forensic risk score into discrete mathematical penalty components.
* **Enterprise Batch Triage:** Ingests multi-invoice CSV batches to separate clean disbursements from high-risk anomalies.
* **Auditor Action Directives:** Emits structured decisions (APPROVED, CONDITIONAL APPROVAL, FLAGGED FOR AUDIT).

## 🚀 Quickstart
1. Clone & Set Up Environment:
   git clone [https://github.com/alimurtaza9dev-ctrl/omniaudit-nim.git](https://github.com/alimurtaza9dev-ctrl/omniaudit-nim.git)
   cd omniaudit-nim
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt

2. Run Streamlit Dashboard:
   streamlit run app.py