"""
data_generator.py
------------------
Generates a synthetic dataset of 1,000 physicians for the PharmaBrand-IQ
project. The dataset simulates commercial marketing metrics that a
pharmaceutical brand team would track for each physician (also known as
a Health Care Professional, or HCP).

Run this script directly to create 'physician_data.csv' in the same folder.
"""

import numpy as np
import pandas as pd

# Setting a seed keeps the "random" numbers the same every time we run this
# script, so results are reproducible for anyone cloning the repo.
np.random.seed(42)

NUM_PHYSICIANS = 1000

SPECIALTIES = ["Oncology", "Cardiology", "GP"]
REGIONS = ["Northeast", "Midwest", "South", "West"]


def generate_physician_ids(n):
    """Creates simple, readable IDs like PHY-00001, PHY-00002, etc."""
    return [f"PHY-{i:05d}" for i in range(1, n + 1)]


def generate_categorical_columns(n):
    """Randomly assigns each physician a specialty and a region."""
    specialty = np.random.choice(SPECIALTIES, size=n, p=[0.25, 0.35, 0.40])
    region = np.random.choice(REGIONS, size=n)
    return specialty, region


def generate_marketing_activity(n):
    """
    Creates the marketing input columns:
    - Digital_Ads_Impressions: how many times a physician saw a digital ad
    - Sales_Rep_Visits: how many times a sales rep visited in the last year
    - Samples_Dropped: how many free drug samples were left with the physician

    These are drawn from simple distributions to mimic real-world variation:
    some physicians are heavily targeted, others are barely reached.
    """
    digital_impressions = np.random.gamma(shape=2.0, scale=800, size=n).astype(int)
    sales_rep_visits = np.random.poisson(lam=6, size=n)
    samples_dropped = np.random.poisson(lam=15, size=n)

    return digital_impressions, sales_rep_visits, samples_dropped


def generate_trx(digital_impressions, sales_rep_visits, samples_dropped, specialty):
    """
    Builds Historical_Prescriptions (TRx - Total Prescriptions) so that it
    is *loosely* driven by marketing activity, plus some realistic noise.

    We intentionally make Sales_Rep_Visits and Samples_Dropped stronger
    drivers of TRx than Digital_Ads_Impressions, since in most real-world
    pharma studies, face-to-face engagement tends to move prescribing
    behavior more than passive digital exposure alone.
    """
    n = len(digital_impressions)

    # Base prescription volume that every physician has regardless of marketing
    base_trx = np.random.normal(loc=40, scale=10, size=n)

    # Specialty effect: oncologists and cardiologists typically prescribe
    # more of the relevant specialty drug than general practitioners
    specialty_effect = pd.Series(specialty).map(
        {"Oncology": 25, "Cardiology": 15, "GP": 0}
    ).values

    # Marketing effect: scaled contributions from each channel
    digital_effect = digital_impressions * 0.01
    rep_visit_effect = sales_rep_visits * 3.0
    sample_effect = samples_dropped * 1.2

    # Random noise so the relationship is realistic, not a perfect formula
    noise = np.random.normal(loc=0, scale=8, size=n)

    trx = (
        base_trx
        + specialty_effect
        + digital_effect
        + rep_visit_effect
        + sample_effect
        + noise
    )

    # Prescriptions can't be negative, and we round to whole numbers
    trx = np.clip(trx, a_min=0, a_max=None).round().astype(int)
    return trx


def generate_physician_dataset(n=NUM_PHYSICIANS):
    """Assembles all columns into a single pandas DataFrame."""
    physician_ids = generate_physician_ids(n)
    specialty, region = generate_categorical_columns(n)
    digital_impressions, sales_rep_visits, samples_dropped = generate_marketing_activity(n)
    trx = generate_trx(digital_impressions, sales_rep_visits, samples_dropped, specialty)

    df = pd.DataFrame({
        "Physician_ID": physician_ids,
        "Specialty": specialty,
        "Historical_Prescriptions": trx,
        "Digital_Ads_Impressions": digital_impressions,
        "Sales_Rep_Visits": sales_rep_visits,
        "Samples_Dropped": samples_dropped,
        "Region": region,
    })

    return df


if __name__ == "__main__":
    physician_df = generate_physician_dataset()
    output_path = "C:/Users/srinithya/Downloads/analytics-projects-main/pharmasales/physician_data.csv"
    physician_df.to_csv(output_path, index=False)

    print(f"Generated {len(physician_df)} physician records.")
    print(f"Saved to: {output_path}")
    print("\nPreview:")
    print(physician_df.head())
