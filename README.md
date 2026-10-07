# 🛡️ OmniAudit NIM
### Autonomous Enterprise Financial Forensics & Cost Anomaly Detection Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://omniaudit-nim-ysnpjrzlrcepxmappexyypy.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Model Accuracy](https://img.shields.io/badge/R%C2%B2%20Baseline-96.99%25-brightgreen.svg)](#-quantitative-grounding--regression-baseline)
[![Devpost](https://img.shields.io/badge/Devpost-Submission-003E54.svg)](https://devpost.com/software/omniaudit-nim)

OmniAudit NIM is an autonomous agentic auditing framework built for the **Nebius x NVIDIA Global AI Hackathon**. It detects invoice fraud, phantom shell companies, and price gouging across enterprise supply chains.

Traditional ERP rule engines are too rigid to detect adaptive fraud schemes, while standalone LLMs cannot be trusted with raw financial calculations due to numerical hallucinations. OmniAudit NIM bridges this divide by coupling **agentic LLM reasoning** with **deterministic multivariate regression ($R^2 = 96.99\%$)** and **real-time entity search grounding** into an explainable verification pipeline.

---

## 🎥 Video Demonstration

Watch the complete forensic audit, Explainable AI breakdown, and batch CSV triage queue in action:

[![OmniAudit NIM Video Walkthrough](https://img.youtube.com/vi/MgNxqO9XXJ8/maxresdefault.jpg)](https://youtu.be/MgNxqO9XXJ8)

> **[▶ Click here to watch the full demo on YouTube](https://youtu.be/MgNxqO9XXJ8)**

---

## ⚡ Key Capabilities

* **Multivariate Regression Grounding ($R^2 = 96.99\%$):** Benchmarks billed freight charges against a calibrated route-distance and cargo-weight regression model to eliminate LLM arithmetic hallucinations.
* **Real-Time Entity Radar:** Simultaneously queries corporate registries, public debarment lists, and fraud databases via the Tavily Search API using multithreaded concurrency.
* **Explainable AI (XAI) Attribution:** Replaces arbitrary black-box scores with a transparent, point-by-point penalty attribution breakdown ($0–100$).
* **Enterprise Batch Triage:** Ingests multi-transaction CSV disbursement queues to automatically approve compliant suppliers while isolating fraudulent outliers.
* **Actionable Directives:** Emits concrete procedural recommendations (`APPROVED FOR DISBURSEMENT` vs. `FLAGGED FOR AUDIT: HOLD DISBURSEMENT`).
* **Resilient Model Cascade:** Architected with automatic fallback tiers across inference engines to guarantee zero-downtime reliability in high-throughput enterprise environments.

---

## 🏗️ System Architecture

```text
                     [ Enterprise Accounts Payable Queue ]
                                       │
                         [ Streamlit Dark-Mode UI ]
                                       │
                ┌──────────────────────┴──────────────────────┐
                │                                             │
      [ 1. Deterministic Grounding ]               [ 2. Entity Radar Layer ]
      Scikit-Learn Multivariate Model              Tavily Web Intelligence
         (Distance, Weight Baselines)             (Registries, Debarment Lists)
                │                                             │
                └──────────────────────┬──────────────────────┘
                                       │
                      [ 3. Explainable AI (XAI) Engine ]
                         Point Penalty Matrix (0–100)
                                       │
                      [ 4. Synthesis & Fallback Cascade ]
                            NVIDIA NIM / GenAI SDK
                                       │
                      [ Actionable Payment Directive ]
                        (Hold vs. Approve Payout)

## 📊 Quantitative Grounding & Regression Baseline

To eliminate numerical hallucinations, billed amounts are strictly benchmarked against an empirical multivariate regression baseline before entering the reasoning loop:

$$\text{Expected Freight Cost} = \beta_0 + \beta_1(\text{Distance in Miles}) + \beta_2(\text{Weight in Lbs}) + \epsilon$$

* **Baseline Performance:** $R^2 = 96.99\%$ predictive accuracy on logistics distributions.
* **Variance Trigger:** Transactions showing $+50\%$ or greater variance against the expected cost baseline automatically trigger high-severity penalty deductions.

---

## 📂 Sample Batch CSV Format

To test the **Batch Ingestion & Triage** tab, format your CSV file with the following headers:

```csv
invoice_number,vendor_name,tax_id,distance_miles,weight_lbs,billed_amount,payment_terms_days
INV-2026-9041,Phantom Swift Logistics LLC,EIN-00-9988112,320.0,1500.0,3150.00,5
INV-2026-1022,Reliable Logistics Partners Inc,EIN-88-2910492,850.0,3200.0,1850.00,30
INV-2026-4421,TransNational Overland Corp,EIN-23-4019283,450.0,1800.0,1420.00,15
INV-2026-5590,Ghost Haulage Enterprises,EIN-11-0022991,210.0,900.0,2400.00,3
```

---

## 🚀 Quickstart & Local Installation

### Prerequisites
* Python 3.10+
* Tavily API Key
* NVIDIA NIM / LLM API Key

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/alimurtaza9dev-ctrl/omniaudit-nim.git
cd omniaudit-nim
python -m venv venv
```

**Activate the virtual environment:**

* **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
* **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials

Create a `.env` file in the root directory:

```env
TAVILY_API_KEY="your-tavily-api-key"
NVIDIA_API_KEY="your-nvidia-api-key"
```

### 4. Launch the Streamlit Dashboard

```bash
streamlit run app.py
```

The application will launch locally at `http://localhost:8501`.

---

## 🛠️ Tech Stack

* **Framework & Frontend:** Streamlit, Pandas, NumPy
* **Machine Learning:** Scikit-Learn (Multivariate Linear Regression)
* **Real-Time Web Intelligence:** Tavily Search API
* **Concurrency:** Python `concurrent.futures.ThreadPoolExecutor`
* **Agentic Synthesis:** NVIDIA NIM Microservices, Google GenAI SDK

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
