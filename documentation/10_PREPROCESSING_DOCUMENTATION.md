# PREPROCESSING_DOCUMENTATION.md

## Purpose
This document describes the preprocessing pipeline used to transform the Milan telecom dataset into clustering-ready feature matrices. The pipeline is designed to be:

- **reproducible** (saved artifacts + saved transformation objects),
- **comparable** (two preprocessing variants saved for later evaluation),
- **aligned with project objectives** (preserve interpretable temporal rhythms for urban zone typologies).

---

## Inputs

### Source dataset
- `data/processed/milan_telecom_agg_all.parquet`

This dataset is already cleaned/structured:
- aggregated over `country_code` (one row per `square_id` × `time_interval`)
- activity NaNs handled as “no activity” during earlier steps
- includes `datetime` and (optionally) derived grid coordinates `x`, `y` for visualization

### Activity channels used
- `sms_in`, `sms_out`, `call_in`, `call_out`, `internet_traffic`

---

## Step 1 — Temporal feature engineering (clustering representation)
**Chosen strategy:** hour-of-day profiles split by weekday/weekend, using mean aggregation.

For each grid cell (`square_id`), we compute:
- mean activity for each hour `00–23`
- separately for `weekday` and `weekend`

This yields:
- 5 channels × 24 hours × 2 regimes = **240 features**
- feature naming example: `weekday_hour_08_call_out_mean`

Output artifact:
- `results/preprocessing/features_hourly_weekday_weekend_mean_FULL.parquet`  
  (shape: 10,000 rows × 241 columns including `square_id`)

Rationale:
- preserves interpretable mobility rhythms (commuting, daytime vs nighttime, weekday/weekend regime shifts)
- reduces noise relative to raw 10-minute time steps
- supports clear cluster profiling and stakeholder-friendly narratives

(See also: `TEMPORAL_CLUSTERING_STRATEGY.md`.)

---

## Step 2 — Feature selection
Variance screening found no near-constant features; correlation filtering was tested but rejected because it removed daytime coverage and eliminated internet features. The final decision was to retain the full 240-feature representation.

Documentation:
- `FEATURE_SELECTION.md`

---

## Step 3 — Preprocessing variants for clustering (best-practice comparison)
Because preprocessing can change clustering geometry, two defensible variants were created and saved for later comparison in modeling:

### Variant A (baseline): StandardScaler on raw feature matrix
- Input: 240 engineered features (nonnegative means)
- Transformation: `StandardScaler()` fit on the full dataset
- Output artifact:
  - `results/preprocessing/features_FULL_standardscaled.parquet`
- Saved transformer:
  - `results/preprocessing/scaler_variant_A_standard.joblib`

### Variant B (skew-robust): log1p + StandardScaler
- Input: same 240 engineered features
- Transformation:
  1) apply `log1p` to all feature values
  2) fit `StandardScaler()` on the transformed matrix
- Output artifact:
  - `results/preprocessing/features_FULL_log1p_standardscaled.parquet`
- Saved transformer:
  - `results/preprocessing/scaler_variant_B_log1p_standard.joblib`

Sanity check results:
- both transformed matrices have mean ~0 and std ~1 (averaged across columns), confirming consistent scaling.

---

## Reproducibility artifacts
The following files enable exact reproduction:

- Feature matrix:
  - `results/preprocessing/features_hourly_weekday_weekend_mean_FULL.parquet`
- Preprocessing variants:
  - `results/preprocessing/features_FULL_standardscaled.parquet`
  - `results/preprocessing/features_FULL_log1p_standardscaled.parquet`
- Scalers:
  - `results/preprocessing/scaler_variant_A_standard.joblib`
  - `results/preprocessing/scaler_variant_B_log1p_standard.joblib`
- Square holdout split for stability testing:
  - `results/preprocessing/square_id_split.npz`

---

## Intended use in modeling
`04_model_building.ipynb` will load and compare Variant A vs Variant B using:
- internal clustering metrics (e.g., silhouette),
- stability checks across train/holdout squares,
- interpretability of cluster-average temporal profiles,
- spatial plausibility via maps (using `x,y` for visualization only).

The chosen variant will be the one that best balances:
- stability,
- interpretability,
- alignment with the sustainability/mobility use case.