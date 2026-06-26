"""
PharmaField-IQ
Python Data Analytics Pipeline
Purpose:
- Load pharmaceutical field execution dataset
- Perform data validation
- Conduct exploratory analysis
- Generate KPI summaries
- Prepare data for SQL analytics
"""

# ============================================================
# IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np

# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "pharmafield_iq_dataset.xlsx"
df = pd.read_excel(DATA_PATH)
print("="*60)
print("PHARMAFIELD-IQ DATA ANALYTICS PIPELINE")
print("="*60)
print("\nDataset Shape:")
print(df.shape)

# ============================================================
# BASIC EXPLORATION
# ============================================================

print("\nDataset Information")
print(df.info())
print("\nFirst Five Records")
print(df.head())
print("\nSummary Statistics")
print(df[[ "Target_Value", "Actual_Sales", "Calls_Made", "Samples_Distributed"]].describe())

# ============================================================
# DATA QUALITY CHECKS
# ============================================================
print("\nMissing Values")
print(df.isnull().sum())
print("\nDuplicate Records")
print(df.duplicated().sum())

# Negative value validation
numeric_columns = ["Target_Value", "Actual_Sales", "Calls_Made", "Samples_Distributed"]
print("\nNegative Value Check")
for col in numeric_columns:
  count = (df[col] < 0).sum()
  print(f"{col}: {count}")

# ============================================================
# DATA CLEANING
# ============================================================

clean_df = df.copy()
# Replace invalid sales values
clean_df.loc[clean_df["Actual_Sales"] < 0, "Actual_Sales"] = 0
# Missing call values
clean_df["Calls_Made"] = (clean_df["Calls_Made"].fillna(clean_df["Calls_Made"].median()))
# Remove records without target
clean_df = (clean_df.dropna(subset=["Target_Value"]))
print("\nClean Dataset Shape")
print(clean_df.shape)

# ============================================================
# KPI CREATION
# ============================================================

clean_df["Achievement_Percentage"] = (clean_df["Actual_Sales"]/clean_df["Target_Value"]) * 100
clean_df["Sales_Per_Call"] = (clean_df["Actual_Sales"]/clean_df["Calls_Made"])

# ============================================================
# TERRITORY ANALYSIS
# ============================================================
territory_summary = (clean_df.groupby(["Region","Territory"]).agg(Rep_Count=("Rep_ID","count"),
Total_Target=("Target_Value","sum"),Total_Sales=("Actual_Sales","sum"),Avg_Calls=("Calls_Made","mean"),
Avg_Samples=("Samples_Distributed","mean")).reset_index())

territory_summary["Achievement_Percentage"] = (territory_summary["Total_Sales"]/territory_summary["Total_Target"])*100
territory_summary["Sales_Per_Call"] = (territory_summary["Total_Sales"]/territory_summary["Avg_Calls"])

print("\nTerritory Performance")
print(territory_summary.head())

# ============================================================
# IDENTIFY UNDERPERFORMING TERRITORIES
# ============================================================
underperforming = (territory_summary[territory_summary["Achievement_Percentage"]<90])
print("\nUnderperforming Territories")
print(underperforming)

# ============================================================
# EXPORT CLEAN DATA
# ============================================================
clean_df.to_excel("pharmafield_clean_dataset.excel", index=False)
territory_summary.to_excel("territory_kpi_summary.excel", index=False)
print("\nAnalytics Completed Successfully")
