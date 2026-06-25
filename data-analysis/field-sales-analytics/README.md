# PharmaField-IQ: Territory Execution & Sales Effectiveness Analytics Pipeline

## End-to-End Healthcare Commercial Analytics Project Using Python, SQL & Excel

![Python](https://img.shields.io/badge/Python-Analytics-blue)
![SQL](https://img.shields.io/badge/SQL-SQLite-orange)
![Excel](https://img.shields.io/badge/Microsoft%20Excel-Dashboard-green)

---

## Project Overview

**PharmaField-IQ** is an end-to-end commercial analytics project designed to evaluate pharmaceutical field-force execution performance across multiple regions and territories.

The objective of this project is to simulate a real-world pharma sales analytics workflow where raw field execution data is transformed into validated business insights through:

- Data quality validation
- SQL-based aggregation
- KPI calculation
- Executive dashboard creation
- Business recommendation generation

This project was developed as a practical analytics portfolio project by studying existing financial and commercial performance dashboards, reviewing guided analytics projects, and following industry-style reporting templates to design a structured Excel output suitable for business stakeholders.

---

## Business Problem

Pharmaceutical organizations rely on field execution teams such as Medical Representatives to drive product adoption through physician engagement activities. However, commercial teams need visibility into:

- Which territories are missing sales targets?
- Are representatives efficiently converting field calls into sales?
- Are distributed samples translating into commercial impact?
- Which regions require intervention?

This project addresses these questions by creating an analytics pipeline that identifies underperforming territories and highlights potential execution bottlenecks.

---

## Project Workflow

Python Data Validation Pipeline
|
↓
SQLite Database Loading
|
↓
SQL Territory-Level Analytics
|
↓
Excel Executive Dashboard Creation
|
↓
Business Insights & Recommendations

---

## Repository Structure

```text
├── pharmafield_iq.py                      # Main Python analysis and automation script
├── Field_Execution_Performance_Report.xlsx # Auto-generated multi-sheet Excel report
├── dataset/
│   └── pharmafield_iq_dataset.csv         # Raw source dataset (KPIs, field metrics)
└── README.md                              # Project documentation
```

---

## Dataset Description

The dataset represents pharmaceutical field-force execution performance.

## Dataset Features

| Column | Description |
|---|---|
| Rep_ID | Unique representative identifier |
| Rep_Name | Medical representative name |
| Region | Geographic business region |
| Territory | Sales territory |
| Target_Value | Assigned sales target |
| Actual_Sales | Achieved sales |
| Calls_Made | Physician/customer engagement activity |
| Samples_Distributed | Product samples distributed |

Dataset Coverage:
- 200 medical representatives
- 5 regions
- 20 territories

---

## SQL Analytics

The SQL layer calculates territory-level KPIs:

### Metrics Generated
Target Achievement % = Actual Sales / Target Sales × 100
Sales Efficiency = Sales / Calls Made

### Additional Indicators

- Representative count
- Average samples distributed
- Territory performance ranking

The analysis identifies territories below:
90% Target Achievement Threshold

---

## Excel Dashboard Output

The final Excel report contains three structured worksheets:

1. Executive Dashboard
Contains:

- Territory performance summary
- Achievement %
- Sales per call
- Critical performance indicators

2. Analytics Data
Contains:
- SQL-generated territory analysis output

3. Validation Log
Contains:

- Data quality issues
- Remediation actions
- Validation status

---

## Key Business Insights Demonstrated

This project demonstrates how analytics can support:

### Field Performance Optimization - Identify territories requiring intervention.
### Sales Effectiveness Improvement - Evaluate whether field activities translate into revenue.
### Resource Allocation - Support regional manager decisions.
### Data Quality Governance - Ensure reporting accuracy before business decisions.

---

## Learning Approach

To create the final reporting structure, I analyzed multiple financial and commercial dashboard examples, practiced guided analytics projects, and studied commonly used business intelligence layouts.The final Excel output follows a stakeholder-focused reporting approach:

- Clear KPI visibility
- Executive-friendly formatting
- Action-oriented insights
- Data validation transparency

---




