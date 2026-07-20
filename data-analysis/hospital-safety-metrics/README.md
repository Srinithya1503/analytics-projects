# HospSafe-Analytics: CMS Patient Safety & Quality Performance Tracker

A portfolio data-engineering & analytics project that models a corporate healthcare workflow end-to-end: **MySQL → Excel → Python
(Pandas)**. It simulates the kind of pipeline a healthcare payer, health system, or health-tech vendor analyst might
build to monitor CMS-style hospital patient-safety and quality performance.

---

## Project Overview

Hospitals in the U.S. are publicly scored by CMS across several quality domains, including patient-safety indicators and 30-day
readmission measures. This project builds a **relational database** that mirrors the structure of that public reporting, populates it with
a 220-facility synthetic dataset, and layers on a Python analytics pass that computes a custom **Composite Risk Penalty Index** to flag
hospitals whose safety and readmission performance is trending worse than their national benchmark.

---

## **Tech stack:**

| Layer | Tool | Role |
|---|---|---|
| Database | **MySQL 8.0+** | Relational schema, mock data, analytical JOIN/window-function query |
| Data hand-off | **Microsoft Excel (.xlsx)** | Export target for the SQL query; input format for the Python layer |
| Analytics | **Python (Pandas, NumPy, Matplotlib, Seaborn)** | Cleaning, index calculation, outlier segmentation, visualization |

---

## Data Engineering Workflow

```
 ┌────────────────┐     ┌──────────────────┐     ┌───────────────────┐     
 │   1. MySQL      │     │   2. Excel        │     │   3. Python         │    
 │  schema.sql     │ --> │  cms_hospital_    │ --> │  analysis,ipynb     │  
 │  (build + load  │     │  safety_export    │     │  (Pandas only)      │              
 │  + JOIN query)  │     │  .xlsx            │     │                     │  
 └────────────────┘     └──────────────────┘     └───────────────────┘     
```

1. **MySQL (`schema.sql`)** — Build the `hospitals` and `safety_metrics`
   tables, bulk-load 220 mock facility records, then run the final
   analytical `SELECT`.
2. **Excel output** — Run the query in MySQL Workbench 
   then use **Table Data Export Wizard → Export to Excel**
   (or copy/paste the results grid) to save the result set as
   `cms_hospital_safety_export.xlsx`. 
3. **Python (`analysis.ipynb`)** — Load the `.xlsx` file, clean
   and flag unrated facilities, compute the **Composite
   Risk Penalty Index**, segment outliers by State and Hospital
   Ownership, and render Seaborn/Matplotlib visualizations.

---

## Repository Contents

| File | Description |
|---|---|
| `schema.sql` | MySQL DDL, 220-row mock data load, and the final analytical export query |
| `analysis.ipynb` | Jupyter-cell-formatted Pandas analysis (open in VS Code/Jupyter or convert with `jupytext`) |
| `README.md` | This file |
---

## Reproducibility Walkthrough

### 1. Stand up the database

```bash
mysql -u root -p < schema.sql
```

This creates the `hospsafe_analytics` database, both tables, loads all
220 hospital rows + their paired `safety_metrics` rows, and prints the
final analytical result set to the console.

### 2. Export to Excel

In MySQL Workbench, run just the final `SELECT` block at the bottom of
`schema.sql`, then:
`Results grid → right-click → Export → cms_hospital_safety_export.xlsx`

Place the resulting file in the same directory as
`analysis.ipynb`.

### 3. Run the notebook

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

```bash
python analysis.ipynb
```

Running all cells will print summary statistics, render the two visualizations, and write `outlier_worklist.xlsx` — the prioritized list of highest-risk facilities.


---

## Official Data Attribution & Reference Framework

This project's schema and metric fields are **not sourced from a live CMS data pull or a downloaded CMS file**. Instead, the table structure
and variable names were engineered by studying and cross-referencing the publicly documented field layouts of the **Centers for Medicare &
Medicaid Services (CMS) Provider Data Catalog**, specifically the **"Hospital General Information"** dataset available at
[data.cms.gov](https://data.cms.gov). Fields such as `facility_id`, `facility_name`, `hospital_type`, `hospital_ownership`, `overall_rating`, and the safety/readmission "better / no different / worse" measure-group counts are modeled directly on the naming conventions and category values used in that public dataset.

**All 220 hospital records and their associated safety metrics in `schema.sql` are synthetic mock data**, generated with a fixed random seed for reproducibility.  The goal was to engineer a realistic *database footprint* — matching the shape, categories, and rough statistical baselines seen in the real government dataset — for safe,
freely shareable portfolio use.

---
