# PharmaBrand-IQ: Multi-Channel Marketing Mix Modeling & Physician Segmentation

A commercial analytics project that helps pharmaceutical brand teams understand **which physicians to target, how to segment them, and which 
marketing channels actually drive prescriptions.**

---

## Project Overview

Pharmaceutical brand teams invest across multiple channels — sales rep visits, digital advertising, and product samples — to influence physician
prescribing behavior. The challenge is knowing **which physicians deserve which type of engagement**, and **which channel is actually worth the
investment**.
PharmaBrand-IQ addresses this with two connected analyses:

1. **Physician Segmentation** — clusters physicians into distinct engagement profiles (`High-Touch Advocates`, `Digital-First Responders`,
    `Low Engagement Profiles`) so marketing teams can tailor their approach to each group.
3. **Marketing Mix Modeling (MMM)** — quantifies the relationship between marketing activity (digital ads, rep visits, samples) and prescription
   volume (TRx), producing interpretable coefficients that show the estimated ROI of each channel.

The result is a single, exportable insights file that a brand or field team can use directly to plan targeting and budget allocation.

---

## Project Structure

```
PharmaBrand-IQ/
│
├── data_generator.py              # Builds the physician-level dataset
├── analytical_pipeline.py         # Segmentation + Marketing Mix Model
├── final_physician_insights.csv   # Model output: segments + raw data
├── interpretation_results.md      # Plain-language breakdown of results
└── README.md                      # Project documentation (this file)
```
---

## Core Features

- **Physician Segmentation Engine** — KMeans clustering (scikit-learn) automatically groups physicians into three readable, business-friendly
  segments based on their marketing engagement patterns.
- **Marketing Mix Model (MMM)** — an OLS regression (statsmodels) quantifies the incremental prescription impact of each marketing
  channel, complete with coefficients, p-values, and model fit (R²).
- **Business-Ready Reporting** — results are exported to a clean CSV and summarized in plain-language markdown, so non-technical stakeholders
  (brand managers, sales leadership) can act on the findings without needing to interpret raw statistical output.
- **Modular, Readable Codebase** — each analytical step lives in its own function, making the pipeline easy to extend (e.g. adding new channels,
  swapping in a different clustering algorithm, or testing new features).

---

## Technical Stack

| Category | Tools / Libraries |
|---|---|
| Language | Python 3 |
| Data Handling | pandas, numpy |
| Machine Learning | scikit-learn (KMeans, StandardScaler) |
| Statistical Modeling | statsmodels (OLS Regression) |
| Output Formats | CSV (data), Markdown (reporting) |

---

