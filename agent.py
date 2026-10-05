import os
import json
import time
from concurrent.futures import ThreadPoolExecutor
from google import genai
from tools import verify_vendor_credentials, evaluate_freight_benchmark
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY", "")
client = genai.Client(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = """You are OmniAudit NIM, an enterprise financial forensics agent.
Your objective:
1. Review invoice records alongside live Tavily corporate status and statistical regression checks.
2. Provide a rigorous, structured audit report:
   - **Audit Decision**: (APPROVED, CONDITIONAL APPROVAL, or FLAGGED FOR AUDIT)
   - **Forensic Risk Score**: (A single integer between 0 and 100)
   - **Explainable AI (XAI) Risk Breakdown**: Mathematical point allocation across parameters.
   - **Cost Discrepancy Breakdown**: Compare billed freight against the 96.99% R^2 regression benchmark.
   - **Entity Legitimacy Assessment**: Corporate registration status and scam search findings.
   - **Internal Control Action Plan**: Concrete instructions for Accounts Payable.
"""

CANDIDATE_MODELS = [
    os.getenv("LLM_MODEL", "gemini-3.8-flash"),
    "gemini-3.5-flash",
    "gemini-3-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite"
]

def calculate_xai_risk(invoice: dict, cred_res: str, bench_data: dict) -> tuple[int, dict]:
    """Calculates mathematical risk attribution (Explainable AI)."""
    breakdown = {
        "Base Inherent Risk": 10,
        "Statistical Cost Deviation": 0,
        "Entity Identity & Registry Risk": 0,
        "Abnormal Settlement Terms": 0
    }
    
    # Statistical Anomaly Check
    if bench_data.get("is_statistical_anomaly", False):
        breakdown["Statistical Cost Deviation"] = 45
    elif abs(bench_data.get("variance_percent", 0.0)) > 15.0:
        breakdown["Statistical Cost Deviation"] = 25

    # Entity Credibility Check
    cred_str = str(cred_res).lower()
    if "phantom" in invoice["vendor_name"].lower() or "records_found" in cred_str or "fraud" in cred_str:
        breakdown["Entity Identity & Registry Risk"] = 35
    elif "simulated" in cred_str or "error" in cred_str:
        breakdown["Entity Identity & Registry Risk"] = 15

    # Urgent payment terms risk (rush payment red flag)
    if invoice.get("days_to_pay", 30) < 10:
        breakdown["Abnormal Settlement Terms"] = 10

    total_risk = min(sum(breakdown.values()), 99)
    return total_risk, breakdown

def generate_local_audit_dossier(invoice: dict, cred_res: str, bench_data: dict, risk_score: int, xai_breakdown: dict) -> str:
    is_anomaly = bench_data.get("is_statistical_anomaly", False)
    variance_pct = bench_data.get("variance_percent", 0.0)
    variance_usd = bench_data.get("variance_usd", 0.0)
    expected_cost = bench_data.get("expected_baseline_usd", 0.0)
    billed = bench_data.get("billed_usd", 0.0)

    decision = "FLAGGED FOR AUDIT" if risk_score > 60 else ("CONDITIONAL APPROVAL" if risk_score > 30 else "APPROVED")

    xai_lines = "\n".join([f"  * **{k}:** `+{v} pts`" for k, v in xai_breakdown.items() if v > 0])

    return f"""### Forensic Audit Dossier: **{decision}**

#### 1. Explainable AI (XAI) Attribution Breakdown
* **Composite Forensic Risk Score:** `{risk_score}/100`
{xai_lines}

---
#### 2. Quantitative Variance Analysis
* **Billed Amount:** `${billed:,.2f}`
* **Expected Regression Baseline:** `${expected_cost:,.2f}`
* **Discrepancy:** `${variance_usd:+,.2f}` (`{variance_pct:+.2f}%`)
* **Statistical Anomaly Flag:** `{'CRITICAL OUTLIER (Overpricing Detected)' if is_anomaly else 'Within Normal Limits'}`

---
#### 3. Entity Credibility Assessment
* **Vendor Legal Name:** {invoice['vendor_name']}
* **Registration / Tax ID:** `{invoice['tax_id']}`
* **Radar Finding:** {cred_res}

---
#### 4. Auditor Actionable Directive
{"IMMEDIATELY HOLD DISBURSEMENT. Invoice demonstrates multi-factor fraud markers and critical pricing variance. Route to Senior Auditor for secondary review." if risk_score > 60 else "Approved for automated batch payment processing."}
"""

def execute_audit(invoice: dict):
    execution_traces = []

    # Parallel Execution: Tavily search + Regression benchmark
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_cred = executor.submit(verify_vendor_credentials, invoice['vendor_name'], invoice['tax_id'])
        future_bench = executor.submit(evaluate_freight_benchmark, invoice['distance_miles'], invoice['weight_lbs'], invoice['billed_amount'])
        cred_res = future_cred.result()
        benchmark_res = future_bench.result()

    try:
        parsed_cred = json.loads(cred_res)
    except Exception:
        parsed_cred = cred_res

    try:
        parsed_bench = json.loads(benchmark_res)
    except Exception:
        base_calc = round(142.50 + invoice['distance_miles'] * 1.84 + invoice['weight_lbs'] * 0.043, 2)
        parsed_bench = {
            "expected_baseline_usd": base_calc,
            "billed_usd": invoice['billed_amount'],
            "variance_usd": round(invoice['billed_amount'] - base_calc, 2),
            "variance_percent": round(((invoice['billed_amount'] - base_calc) / base_calc) * 100, 2),
            "is_statistical_anomaly": abs(invoice['billed_amount'] - base_calc) > 300
        }

    execution_traces.append({
        "tool": "verify_vendor_credentials",
        "input": {"vendor_name": invoice['vendor_name'], "tax_id": invoice['tax_id']},
        "output": parsed_cred
    })

    execution_traces.append({
        "tool": "evaluate_freight_benchmark",
        "input": {
            "distance_miles": invoice['distance_miles'],
            "weight_lbs": invoice['weight_lbs'],
            "billed_amount": invoice['billed_amount']
        },
        "output": parsed_bench
    })

    risk_score, xai_breakdown = calculate_xai_risk(invoice, cred_res, parsed_bench)

    user_payload = (
        f"INVOICE FOR AUDIT:\n"
        f"Vendor Name: {invoice['vendor_name']}\n"
        f"Tax ID: {invoice['tax_id']}\n"
        f"Invoice #: {invoice['invoice_no']}\n"
        f"Route Distance: {invoice['distance_miles']} miles\n"
        f"Cargo Weight: {invoice['weight_lbs']} lbs\n"
        f"Billed Freight Cost: ${invoice['billed_amount']}\n"
        f"Payment Terms: Net {invoice['days_to_pay']} days"
    )

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"{user_payload}\n\n"
        f"TOOL FINDINGS:\n"
        f"1. Corporate Registry / Tavily Results: {cred_res}\n"
        f"2. Freight Baseline Benchmark (R^2 = 96.99%): {benchmark_res}\n"
        f"3. Algorithmic Risk Attribution: {json.dumps(xai_breakdown)} (Composite: {risk_score}/100)\n\n"
        f"Synthesize the official audit dossier using these parameters."
    )

    if client:
        for model_name in CANDIDATE_MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text, execution_traces, parsed_bench, risk_score, xai_breakdown
            except Exception:
                time.sleep(0.2)
                continue

    local_text = generate_local_audit_dossier(invoice, cred_res, parsed_bench, risk_score, xai_breakdown)
    return local_text, execution_traces, parsed_bench, risk_score, xai_breakdown