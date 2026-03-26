# TEMPORAL_CLUSTERING_STRATEGY.md

## Purpose
This document describes how temporal information in the Milan telecom dataset is incorporated into the clustering pipeline. The goal is to preserve mobility-relevant rhythms (commuting peaks, daytime activity, nighttime leisure) while producing interpretable, clustering-ready features.

---

## 1) Temporal Data Context
The raw dataset records telecom activity (SMS/calls/internet) for Milan grid cells in short time intervals. Each grid cell therefore has a high-frequency time series rather than a single static observation.

Key challenge: raw 10-minute intervals are too granular and noisy for direct clustering and would create extremely high-dimensional representations. A temporal strategy is needed to reduce dimensionality while preserving meaningful patterns.

---

## 2) Clustering Unit and Time Scale
### Clustering unit
- **Entity clustered:** Milan grid cell (`square_id`)
- Each cluster should represent a *type of urban zone* (functional activity profile).

### Time scale used for patterns
- **Primary temporal scale:** within-day cycles (hour-of-day)
- **Secondary temporal regime:** weekday vs weekend

Rationale: for urban mobility and activity patterns, the largest and most interpretable differences are typically expressed through:
- morning/evening peaks (commuting),
- daytime vs nighttime intensity (work vs leisure),
- weekday vs weekend regime shifts.

---

## 3) Chosen Temporal Approach
### Approach selected: Temporal aggregation + temporal feature engineering
Instead of full time-series clustering (e.g., DTW on raw sequences), the project uses **temporal feature engineering**:

1. derive time features (`hour`, `weekday`, `is_weekend`) from timestamps,
2. aggregate 10-minute observations into **hourly bins**,
3. compute mean activity per hour separately for weekdays and weekends,
4. flatten these profiles into a per-cell feature vector for clustering.

This approach is preferred because:
- it reduces noise and dimensionality,
- it is easier to validate and explain to stakeholders,
- it preserves interpretable rhythm structure,
- it supports clear cluster profiling (average curves).

---

## 4) Feature Representation (Final)
For each `square_id`, we compute:

- **5 activity channels**: `sms_in`, `sms_out`, `call_in`, `call_out`, `internet_traffic`
- **24 hourly bins**: `00`–`23`
- **2 regimes**: `weekday` and `weekend`

Feature example:
- `weekday_hour_08_call_out_mean`
- `weekend_hour_22_internet_traffic_mean`

Total features:
- 5 × 24 × 2 = **240 features** per grid cell (+ `square_id` identifier)

Artifact:
- `results/preprocessing/features_hourly_weekday_weekend_mean_FULL.parquet`

---

## 5) Treatment of Missingness and Coverage
- Raw missing activity values were treated as “no recorded activity” during preprocessing and replaced with 0 before aggregation.
- The hourly aggregation step produced **no missing values** in the final feature matrix.

Temporal coverage notes (from EDA):
- Most days have full 144 ten-minute intervals.
- One partial day exists (2013-10-31), but the strategy retains it because it is small relative to the total period and does not introduce missingness in the engineered features.

---

## 6) Temporal Stability and Validation Plan
Because temporal patterns may vary across weeks or special periods, the project will assess stability through:

- **Split-half stability tests** on grid cells (train vs holdout squares)
- Sensitivity to number of clusters (k)
- Consistency of cluster-average temporal profiles (do profiles remain interpretable across runs?)

Optionally (if time allows):
- compare profiles computed over subsets of time (e.g., early vs late period) to assess whether zone types are stable across the dataset window.

---

## 7) Relationship to Spatial Interpretation
Spatial coordinates (derived from grid indexing) are used for:
- mapping cluster assignments for interpretability and plausibility checks,
- diagnosing whether clusters are spatially coherent or fragmented.

Spatial coordinates are **not** used as clustering features unless explicitly decided later, because the primary goal is similarity in temporal behavior, not geographic contiguity.

---

## 8) Preprocessing Note (Scaling / Transformations)
Scaling and potential transformations (e.g., log1p) are handled in the preprocessing pipeline and documented separately. These steps adjust feature distributions but do not change the temporal representation strategy described here.

---

## Summary
The project uses an interpretable temporal feature engineering strategy: **hour-of-day profiles split by weekday/weekend**, aggregated as mean activity per grid cell. This representation preserves key urban rhythm structure while reducing noise and dimensionality, enabling standard clustering methods and stakeholder-friendly interpretation through profile plots and spatial maps.