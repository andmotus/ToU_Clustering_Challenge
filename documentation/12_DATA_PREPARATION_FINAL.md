# DATA_PREPARATION_FINAL.md

## Purpose
This document summarizes the final datasets produced for clustering and reporting, including the final chosen model configuration and where to find all artifacts needed to reproduce results.

---

## 1) Raw data (source)
- Original telecom activity files in `data/raw/` (daily `.txt` files)
- Raw fields included (before aggregation): grid cell, timestamp, country_code, and activity measures.

Note: raw data are not used directly in clustering; they are processed into aggregated and feature-engineered representations.

---

## 2) Processed dataset (analysis base)
### File
- `data/processed/milan_telecom_agg_all.parquet`

### Description
- Unit of observation: (`square_id`, `time_interval`)
- `country_code` aggregated away (summed across country codes)
- Activity columns: `sms_in`, `sms_out`, `call_in`, `call_out`, `internet_traffic`
- Missing activity entries treated as “no recorded activity” and filled with 0 prior to aggregation.
- `datetime` created from epoch milliseconds.
- Grid coordinate mapping (`x`, `y`) derived from `square_id` for visualization (not used as clustering input).

Time coverage (from EDA):
- 2013-10-31 23:00:00 → 2014-01-01 22:50:00
- One partial day exists (2013-10-31), retained.

---

## 3) Clustering feature matrix (final representation)
### Feature representation (temporal strategy)
- Hour-of-day profiles split by weekday/weekend, aggregated using mean.

### File
- `results/preprocessing/features_hourly_weekday_weekend_mean_FULL.parquet`

### Dimensions
- Rows: 10,000 grid cells (`square_id`)
- Features: 240 (5 channels × 24 hours × 2 regimes)
- Missingness: none in final engineered matrix

Feature naming pattern:
- `<regime>_hour_<HH>_<channel>_mean`, e.g. `weekday_hour_08_call_out_mean`

---

## 4) Preprocessing variants created (for evaluation)
To avoid assuming a single “correct” preprocessing approach, two variants were created and compared in modeling:

### Variant A (baseline)
- Transformation: StandardScaler applied to the 240 features
- Dataset:
  - `results/preprocessing/features_FULL_standardscaled.parquet`
- Scaler:
  - `results/preprocessing/scaler_variant_A_standard.joblib`

### Variant B (selected)
- Transformation: log1p applied to all 240 features, then StandardScaler
- Dataset:
  - `results/preprocessing/features_FULL_log1p_standardscaled.parquet`
- Scaler:
  - `results/preprocessing/scaler_variant_B_log1p_standard.joblib`

Selection rationale:
- Variant B showed stronger stability across train/holdout splits for k in the main candidate range (4–6).

---

## 5) Final model selection (chosen configuration)
### Chosen model
- Algorithm: KMeans
- k: 4
- Preprocessing: Variant B (log1p + StandardScaler)

### Model artifacts
- Model object:
  - `models/kmeans_k4_variantB.joblib`
- Model card:
  - `models/model_card_k4.json`

### Cluster assignments
- `models/cluster_assignments_k4.parquet`
- `models/cluster_assignments_k4.csv`

Cluster labels used (human-readable):
- 0: Low activity / peripheral
- 1: Urban mixed-use
- 2: Moderate activity
- 3: High-activity core

---

## 6) Validation and sanity checks (summary)
- Key integrity: no duplicates on (`square_id`, `time_interval`) after aggregation; no negative activity values.
- Distributions: activity measures are heavy-tailed; log1p improves behavior for clustering geometry.
- Clusterability: Hopkins validation confirms strong cluster tendency in the engineered feature space.
- Stability: train→holdout agreement (ARI) supported using Variant B and focusing on k=4–6; k=4 chosen for interpretability and spatial plausibility.

---

## 7) How to reproduce the final dataset and model
1) Run `preprocessing_pipeline.py` to rebuild:
   - feature matrices and scalers in `results/preprocessing/`
2) Run `04_model_building.ipynb` to:
   - compare variants,
   - fit k=4 KMeans (Variant B),
   - generate plots and assignments,
   - save model and model card in `models/`

---

## Notes and limitations
- Data represent aggregated telecom activity, not exact trips or demographics.
- The dataset covers late 2013–early 2014; results should be framed as methodological/illustrative unless validated against newer data.
- Cluster labels are functional and non-stigmatizing; interpretation should avoid deterministic claims about communities.