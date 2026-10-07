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
