"""
PharmaField-IQ: Territory Execution & Sales Effectiveness Pipeline
Senior Commercial Analytics Manager | End-to-End Automated Script
"""

import pandas as pd
import numpy as np
import sqlite3
import string

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 1 ── DATA VALIDATION SOP
# ─────────────────────────────────────────────────────────────────────────────

print("─" * 70)
print("[STAGE 2] Running Data Validation SOP...\n")

def validate_and_clean(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Quality-gate function for field-force data.
    Identifies discrepancies, logs findings, applies remediation, and
    returns a clean DataFrame ready for analytics ingestion.
    """
    df_check = dataframe.copy()
    issues_found = []

    # ── Check 1: Null / missing values ────────────────────────────────────
    null_mask = df_check[["Target_Value", "Actual_Sales",
                           "Calls_Made", "Samples_Distributed"]].isnull().any(axis=1)
    null_rows = df_check[null_mask]
    if not null_rows.empty:
        issues_found.append(("MISSING VALUES", null_rows))

    # ── Check 2: Negative numeric values ──────────────────────────────────
    neg_mask = (
        (df_check["Actual_Sales"]        < 0) |
        (df_check["Calls_Made"]          < 0) |
        (df_check["Samples_Distributed"] < 0) |
        (df_check["Target_Value"]        < 0)
    )
    neg_rows = df_check[neg_mask]
    if not neg_rows.empty:
        issues_found.append(("NEGATIVE VALUES", neg_rows))

    # ── Report discrepancies ───────────────────────────────────────────────
    if issues_found:
        print("DISCREPANCIES DETECTED:")
        for issue_type, rows in issues_found:
            print(f"\n {issue_type} ({len(rows)} row(s)) {'─'*35}")
            display_cols = ["Rep_ID", "Rep_Name", "Region",
                            "Target_Value", "Actual_Sales", "Calls_Made"]
            print(rows[display_cols].to_string(index=True, index_names=False))
    else:
        print("  ✔ No discrepancies found.")

    # ── Remediation ───────────────────────────────────────────────────────
    # Rule 1: Replace negative Actual_Sales with 0 (sale occurred but unverifiable)
    df_check.loc[df_check["Actual_Sales"] < 0, "Actual_Sales"] = 0

    # Rule 2: Impute null Calls_Made with regional median (preserves distribution)
    median_calls = df_check["Calls_Made"].median()
    df_check["Calls_Made"] = df_check["Calls_Made"].fillna(median_calls)

    # Rule 3: Drop rows where Target_Value is null (no KPI anchor → unusable)
    before = len(df_check)
    df_check = df_check.dropna(subset=["Target_Value"])
    dropped = before - len(df_check)

    df_check["Calls_Made"] = df_check["Calls_Made"].astype(int)

    # ── Validation success log ─────────────────────────────────────────────
    print("\n  ── REMEDIATION APPLIED ──────────────────────────────────────────")
    print("  ✔ Negative Actual_Sales → replaced with 0")
    print(f"  ✔ Null Calls_Made      → imputed with dataset median ({int(median_calls)})")
    print(f"  ✔ Null Target_Value    → {dropped} row(s) dropped (no KPI anchor)")
    print(f"\n  ✔ VALIDATION COMPLETE │ Clean dataset: {len(df_check)} rows "
          f"({before - len(df_check)} removed)\n")
    return df_check

df_clean = validate_and_clean(df)


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 2 ── SQL DATABASE & ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────

print("─" * 70)
print("[STAGE 3] Loading data into SQLite and running analytics query...\n")

con = sqlite3.connect(":memory:")
df_clean.to_sql("field_performance", con, index=False, if_exists="replace")

SQL = """
SELECT
    Region,
    Territory,
    COUNT(Rep_ID)                                          AS Rep_Count,
    ROUND(SUM(Target_Value), 0)                           AS Total_Target,
    ROUND(SUM(Actual_Sales), 0)                           AS Total_Actual_Sales,
    ROUND(SUM(Actual_Sales) * 100.0 / SUM(Target_Value), 2) AS Achievement_Pct,
    ROUND(SUM(Actual_Sales) / NULLIF(SUM(Calls_Made), 0), 2) AS Sales_Per_Call,
    ROUND(AVG(Samples_Distributed), 0)                   AS Avg_Samples
FROM field_performance
GROUP BY Region, Territory
HAVING Achievement_Pct < 90
ORDER BY Achievement_Pct ASC;
"""

results_df = pd.read_sql_query(SQL, con)
con.close()

print(f"  ✔ SQL executed successfully")
print(f"  ✔ Underperforming territories identified: {len(results_df)}")
print(results_df.to_string(index=False))
print()

