import streamlit as st
import pandas as pd
import io
from agent import execute_audit

st.set_page_config(
    page_title="OmniAudit NIM — Autonomous Forensic Agent",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ OmniAudit NIM")
st.markdown("**Autonomous Financial Forensics & Cost Anomaly Detection Engine** | *NVIDIA NIM / Agentic AI Architecture*")

tab_single, tab_batch, tab_arch = st.tabs(["🔍 Single Invoice Audit", "📑 Batch Ingestion & Triage", "📐 System Architecture"])

# ==============================
# TAB 1: SINGLE INVOICE AUDIT
# ==============================
with tab_single:
    with st.sidebar:
        st.header("⚡ Audit Presets")
        scenario = st.selectbox(
            "Load Preset Scenario:",
            [
                "High-Risk Outlier: Gouged Freight & Phantom Vendor",
                "Legitimate Corporate Invoice (Clean)",
                "Borderline Variance: Elevated Fuel Surcharge"
            ]
        )

        if scenario == "High-Risk Outlier: Gouged Freight & Phantom Vendor":
            v_name, v_tax, v_inv = "Phantom Swift Logistics LLC", "EIN-00-9988112", "INV-2026-9041"
            v_dist, v_wt, v_cost, v_days = 320.0, 1500.0, 3150.00, 5
        elif scenario == "Legitimate Corporate Invoice (Clean)":
            v_name, v_tax, v_inv = "Maersk Integrated Logistics Inc", "EIN-44-1294801", "INV-2026-1182"
            v_dist, v_wt, v_cost, v_days = 600.0, 2800.0, 1380.00, 30
        else:
            v_name, v_tax, v_inv = "TransNational Overland Corp", "EIN-23-4019283", "INV-2026-4421"
            v_dist, v_wt, v_cost, v_days = 450.0, 1800.0, 1420.00, 15

    st.markdown("### 📝 Invoice Ingestion Parameters")
    col1, col2, col3 = st.columns(3)

    with col1:
        vendor = st.text_input("Vendor Legal Name", value=v_name)
        tax_id = st.text_input("Tax / EIN ID", value=v_tax)
        invoice_no = st.text_input("Invoice Number", value=v_inv)

    with col2:
        dist = st.number_input("Transit Route Distance (Miles)", min_value=1.0, value=v_dist, step=10.0)
        weight = st.number_input("Cargo Weight (lbs)", min_value=1.0, value=v_wt, step=50.0)

    with col3:
        billed = st.number_input("Billed Freight Amount ($)", min_value=1.0, value=v_cost, step=50.0)
        terms = st.number_input("Payment Terms (Days)", min_value=1, value=v_days, step=5)

    if st.button("🚀 Run Autonomous Forensic Audit", type="primary", use_container_width=True):
        payload = {
            "vendor_name": vendor,
            "tax_id": tax_id,
            "invoice_no": invoice_no,
            "distance_miles": dist,
            "weight_lbs": weight,
            "billed_amount": billed,
            "days_to_pay": terms
        }

        with st.spinner("Dispatching parallel radar queries & statistical regression analysis..."):
            report, traces, bench_data, risk_score, xai_breakdown = execute_audit(payload)

        st.markdown("---")

        # KPI Metric Bar
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Forensic Risk Score", f"{risk_score} / 100", delta="- High Risk" if risk_score > 60 else "Normal", delta_color="inverse")
        m2.metric("Billed Amount", f"${billed:,.2f}")
        m3.metric("Regression Baseline", f"${bench_data.get('expected_baseline_usd', 0):,.2f}")
        var_pct = bench_data.get('variance_percent', 0.0)
        m4.metric("Variance", f"{var_pct:+.1f}%", delta=f"{var_pct:+.1f}%", delta_color="inverse")

        st.markdown("---")

        left_col, right_col = st.columns([1, 1.2])

        with left_col:
            st.subheader("📊 Explainable AI (XAI) Attribution")
            xai_df = pd.DataFrame(list(xai_breakdown.items()), columns=["Risk Factor", "Points Allocated"])
            st.table(xai_df)

            st.subheader("📈 Cost Variance vs Baseline")
            base_val = bench_data.get('expected_baseline_usd', 0)
            ratio = min(billed / max(base_val, 1), 2.0) / 2.0
            st.progress(ratio, text=f"Billing Ratio vs Baseline: {billed/max(base_val, 1):.2f}x")

            comp_df = pd.DataFrame([
                {"Parameter": "Expected Baseline (96.99% R²)", "Value": f"${base_val:,.2f}"},
                {"Parameter": "Billed Invoice Freight", "Value": f"${billed:,.2f}"},
                {"Parameter": "Net Variance", "Value": f"${bench_data.get('variance_usd', 0):+,.2f}"}
            ])
            st.table(comp_df)

            st.subheader("🛠️ Agent Execution Logs")
            for idx, trace in enumerate(traces, 1):
                with st.expander(f"Step {idx}: `{trace['tool']}`", expanded=False):
                    st.caption("Input Parameters:")
                    st.json(trace["input"])
                    st.caption("Observed Output:")
                    st.json(trace["output"])

        with right_col:
            st.subheader("📑 Forensic Audit Dossier")
            st.markdown(report)

            st.download_button(
                label="📥 Download Audit Dossier (.txt)",
                data=f"OMNIAUDIT FORENSIC DOSSIER\nInvoice: {invoice_no}\nVendor: {vendor}\nRisk Score: {risk_score}\n\n{report}",
                file_name=f"audit_dossier_{invoice_no}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ==============================
# TAB 2: BATCH INGESTION & TRIAGE
# ==============================
with tab_batch:
    st.subheader("📑 Enterprise Batch Ingestion & Triage")
    st.markdown("Upload a CSV batch of pending invoices to automatically audit and triage transactions.")

    # Generate sample template
    sample_csv = pd.DataFrame([
        {"vendor_name": "Apex Freight Logistics", "tax_id": "EIN-11-209384", "invoice_no": "INV-1001", "distance_miles": 400.0, "weight_lbs": 2000.0, "billed_amount": 1050.00, "days_to_pay": 30},
        {"vendor_name": "Phantom Swift Logistics LLC", "tax_id": "EIN-00-9988112", "invoice_no": "INV-1002", "distance_miles": 320.0, "weight_lbs": 1500.0, "billed_amount": 3150.00, "days_to_pay": 5},
        {"vendor_name": "Maersk Integrated Logistics", "tax_id": "EIN-44-1294801", "invoice_no": "INV-1003", "distance_miles": 600.0, "weight_lbs": 2800.0, "billed_amount": 1380.00, "days_to_pay": 30},
        {"vendor_name": "Ghost Haulage Co", "tax_id": "EIN-99-4441110", "invoice_no": "INV-1004", "distance_miles": 200.0, "weight_lbs": 800.0, "billed_amount": 2200.00, "days_to_pay": 3}
    ])
    
    st.download_button(
        label="📥 Download Sample Batch Template (.csv)",
        data=sample_csv.to_csv(index=False),
        file_name="sample_invoices_batch.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader("Upload Invoices CSV", type=["csv"])
    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        st.dataframe(batch_df)

        if st.button("⚡ Run Batch Audit Triage", type="primary"):
            results = []
            progress_bar = st.progress(0)
            total = len(batch_df)

            for idx, row in batch_df.iterrows():
                row_dict = row.to_dict()
                _, _, bench, r_score, _ = execute_audit(row_dict)
                status = "🚨 FLAGGED" if r_score > 60 else ("⚠️ REVIEW" if r_score > 30 else "✅ APPROVED")
                results.append({
                    "Invoice #": row_dict["invoice_no"],
                    "Vendor": row_dict["vendor_name"],
                    "Billed ($)": f"${row_dict['billed_amount']:,.2f}",
                    "Baseline ($)": f"${bench.get('expected_baseline_usd', 0):,.2f}",
                    "Variance (%)": f"{bench.get('variance_percent', 0):+.1f}%",
                    "Risk Score": f"{r_score}/100",
                    "Status": status
                })
                progress_bar.progress((idx + 1) / total)

            st.success("Batch Audit Processing Complete!")
            res_df = pd.DataFrame(results)
            st.dataframe(res_df, use_container_width=True)

# ==============================
# TAB 3: SYSTEM ARCHITECTURE
# ==============================
with tab_arch:
    st.subheader("📐 OmniAudit NIM Architecture")
    st.markdown("""
    OmniAudit NIM operates on an **Agentic Defense Architecture** that combines deterministic machine learning models with live search intelligence and large language models:

    1. **Quantitative Grounding Layer:** A multivariate regression baseline ($R^2 = 96.99\%$) calibrated across logistics parameters to eliminate hallucinations in freight pricing.
    2. **Real-Time Entity Radar Layer:** Tavily Search queries public corporate registers, debarment records, and scam databases in parallel.
    3. **Explainable AI (XAI) Engine:** Mathematical risk score attribution assigning point values across structural criteria.
    4. **Synthesis Agent:** Multi-candidate LLM fallback cascade (Gemini / NVIDIA Nemotron API) to produce audit dossiers for enterprise Accounts Payable teams.
    """)