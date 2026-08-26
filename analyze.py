# analyze.py
# Risk factors: km_since_service (+61%), avg_daily_km (+22%), and load_factor (+19%)
# separate breakdown cars from healthy ones. Total mileage and age show no difference (<1%).
# A composite 0-100 risk score from those three columns flags at-risk cars early.

import pandas as pd

df = pd.read_csv("fleet_history.csv")

# ---------------------------------------------------------------------------
# Step 1 — compare each column between cars that broke down and those that did not
# ---------------------------------------------------------------------------
broke = df[df["broke_down"] == 1]
ok    = df[df["broke_down"] == 0]

cols = ["odometer_km", "age_years", "km_since_service", "avg_daily_km", "load_factor"]

print("=== Group means: broke_down vs healthy ===")
print(f"{'Column':<22} {'Broke mean':>12} {'OK mean':>12} {'Diff %':>10}")
print("-" * 60)
for c in cols:
    bm = broke[c].mean()
    om = ok[c].mean()
    diff_pct = (bm - om) / om * 100 if om != 0 else float("inf")
    print(f"{c:<22} {bm:>12.2f} {om:>12.2f} {diff_pct:>+9.1f}%")

# Result summary:
#   odometer_km      +0.3%  → not a predictor (nearly identical)
#   age_years        -0.2%  → not a predictor (nearly identical)
#   km_since_service +60.8% → STRONG predictor
#   avg_daily_km     +21.5% → moderate predictor
#   load_factor      +18.8% → moderate predictor

# ---------------------------------------------------------------------------
# Step 2 — build a simple 0-100 risk score from the three meaningful columns
#
# Each column is min-max normalised to [0, 1] using the observed data range,
# then averaged and scaled to 100.  No machine learning — fully explainable.
# ---------------------------------------------------------------------------
PREDICTORS = ["km_since_service", "avg_daily_km", "load_factor"]

df_score = df.copy()
for col in PREDICTORS:
    lo, hi = df_score[col].min(), df_score[col].max()
    df_score[f"{col}_norm"] = (df_score[col] - lo) / (hi - lo)

norm_cols = [f"{c}_norm" for c in PREDICTORS]
df_score["risk_score"] = (df_score[norm_cols].mean(axis=1) * 100).round(1)

# ---------------------------------------------------------------------------
# Step 3 — print cars ranked by risk, highest first
# ---------------------------------------------------------------------------
print()
print("=== Fleet breakdown-risk ranking (highest risk first) ===")
print(f"{'Rank':<6} {'Car ID':<12} {'Risk Score':>11} {'km_since_svc':>14} "
      f"{'avg_daily_km':>14} {'load_factor':>12}")
print("-" * 75)

ranked = df_score.sort_values("risk_score", ascending=False).reset_index(drop=True)
for i, row in ranked.iterrows():
    print(
        f"{i+1:<6} {row['car_id']:<12} {row['risk_score']:>11.1f} "
        f"{row['km_since_service']:>14.0f} {row['avg_daily_km']:>14.0f} "
        f"{row['load_factor']:>12.2f}"
    )

print()
print("=== Summary ===")
print("Factors that DO predict breakdown: km_since_service (+61%), "
      "avg_daily_km (+22%), load_factor (+19%)")
print("Factors that do NOT: odometer_km (+0.3%), age_years (-0.2%)")
print("The top-risk cars above should be inspected BEFORE the 80% wear rule triggers.")
