"""
analytical_pipeline.py
------------------------
The core analytics engine for PharmaBrand-IQ.
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

INPUT_FILE = "physician_data.csv"
OUTPUT_FILE = "final_physician_insights.csv"

FEATURE_COLUMNS_FOR_CLUSTERING = [
    "Digital_Ads_Impressions",
    "Sales_Rep_Visits",
    "Samples_Dropped",
]


def load_data(path=INPUT_FILE):
    """Loads the physician dataset from a CSV file."""
    df = pd.read_csv(path)
    return df


# ---------------------------------------------------------------------------
# TASK A: PHYSICIAN SEGMENTATION
# ---------------------------------------------------------------------------

def run_segmentation(df):
    """
    Clusters physicians into 3 groups based on their marketing engagement
    (digital impressions, rep visits, and samples dropped).

    We scale the features first so that no single column (like digital
    impressions, which has large numbers) unfairly dominates the clustering.
    """
    features = df[FEATURE_COLUMNS_FOR_CLUSTERING]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(scaled_features)

    df = df.copy()
    df["Cluster"] = cluster_labels

    df["Segment"] = map_clusters_to_labels(df, kmeans)
    return df


def map_clusters_to_labels(df, kmeans_model):
    """
    KMeans only outputs numeric cluster IDs (0, 1, 2) with no inherent
    meaning. This function looks at the average marketing activity in
    each cluster and assigns a business-friendly label based on the
    pattern it sees:

    - High Sales Rep Visits & Samples  -> "High-Touch Advocates"
    - High Digital Impressions only    -> "Digital-First Responders"
    - Low activity across the board    -> "Low Engagement Profiles"
    """
    cluster_summary = df.groupby("Cluster")[FEATURE_COLUMNS_FOR_CLUSTERING].mean()

    # Rank clusters by their overall (total) marketing engagement
    cluster_summary["Total_Engagement"] = cluster_summary.sum(axis=1)

    cluster_summary["Personal_Touch_Score"] = (
        cluster_summary["Sales_Rep_Visits"] + cluster_summary["Samples_Dropped"]
    )
    cluster_summary["Digital_Share"] = (
        cluster_summary["Digital_Ads_Impressions"] / cluster_summary["Total_Engagement"]
    )

    low_engagement_cluster = cluster_summary["Total_Engagement"].idxmin()

    remaining = cluster_summary.drop(index=low_engagement_cluster)
    high_touch_cluster = remaining["Personal_Touch_Score"].idxmax()
    digital_first_cluster = remaining.drop(index=high_touch_cluster).index[0]

    label_map = {
        high_touch_cluster: "High-Touch Advocates",
        digital_first_cluster: "Digital-First Responders",
        low_engagement_cluster: "Low Engagement Profiles",
    }

    return df["Cluster"].map(label_map)


# ---------------------------------------------------------------------------
# TASK B: MARKETING MIX MODELING (MMM)
# ---------------------------------------------------------------------------

def run_marketing_mix_model(df):
    """
    Fits a linear regression model:

        Historical_Prescriptions ~ Digital_Ads_Impressions
                                  + Sales_Rep_Visits
                                  + Samples_Dropped

    The resulting coefficients tell us, on average, how many extra
    prescriptions we get per unit of each marketing channel. This is a
    simplified, transparent version of the Marketing Mix Models used
    across the pharma industry to plan commercial spend.
    """
    predictor_columns = [
        "Digital_Ads_Impressions",
        "Sales_Rep_Visits",
        "Samples_Dropped",
    ]

    X = df[predictor_columns]
    y = df["Historical_Prescriptions"]

    # statsmodels requires us to manually add an intercept term
    X_with_intercept = sm.add_constant(X)
    model = sm.OLS(y, X_with_intercept).fit()
    return model


def print_regression_summary(model):
    """Prints the regression results in a clean, business-friendly format."""
    print("\n" + "=" * 60)
    print("MARKETING MIX MODEL RESULTS")
    print("=" * 60)

    print(f"\nModel Fit (R-squared): {model.rsquared:.3f}")
    print("(This tells us what % of prescription variation is explained")
    print(" by our three marketing channels.)\n")

    print(f"{'Channel':<28}{'Coefficient':>15}{'P-Value':>12}")
    print("-" * 55)

    readable_names = {
        "const": "Baseline (Intercept)",
        "Digital_Ads_Impressions": "Digital Ads (per impression)",
        "Sales_Rep_Visits": "Sales Rep Visits (per visit)",
        "Samples_Dropped": "Samples Dropped (per sample)",
    }

    for variable_name, coefficient in model.params.items():
        p_value = model.pvalues[variable_name]
        label = readable_names.get(variable_name, variable_name)
        print(f"{label:<28}{coefficient:>15.4f}{p_value:>12.4f}")

    print("\nInterpretation:")
    print("- Each coefficient shows the estimated extra prescriptions (TRx)")
    print("  gained per one additional unit of that marketing channel,")
    print("  holding the other channels constant.")
    print("- A p-value below 0.05 suggests the channel's effect is")
    print("  statistically significant, not just due to random chance.")
    print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------

def main():
    print("Loading physician data...")
    df = load_data()

    print("Running Task A: Physician Segmentation (KMeans)...")
    segmented_df = run_segmentation(df)

    print("Running Task B: Marketing Mix Modeling (Linear Regression)...")
    model = run_marketing_mix_model(segmented_df)

    print_regression_summary(model)

    print("Segment breakdown:")
    print(segmented_df["Segment"].value_counts(), "\n")

    segmented_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Final insights exported to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
