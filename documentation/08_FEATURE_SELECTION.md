# FEATURE_SELECTION.md

## Purpose
This document describes the feature selection process for clustering Milan grid cells using temporal telecom activity profiles. Because clustering has no target variable, feature selection is guided by:

- preserving **interpretability** for stakeholders (urban zone “rhythms”),
- avoiding preprocessing that removes meaningful structure (e.g., daytime commuting patterns),
- managing dimensionality without sacrificing the project’s core objective.

## Project objective context
**Goal:** cluster Milan grid cells (`square_id`) into interpretable urban activity types (e.g., residential, business, nightlife, transit-oriented) based on **temporal activity signatures**.

This requires features that preserve:
- **hour-of-day patterns**, and
- **weekday vs weekend differences**, since these capture commuting vs leisure regimes.

---

## Starting feature set (candidate for clustering)
**Representation:** Hour-of-day profiles split by weekday/weekend, using mean aggregation.

**Construction:**
- 5 activity channels: `sms_in`, `sms_out`, `call_in`, `call_out`, `internet_traffic`
- 24 hourly bins
- 2 regimes: weekday vs weekend
- Feature definition example: `weekday_hour_08_call_out_mean`

**Dimensionality:**
- 5 channels × 24 hours × 2 regimes = **240 features**
- Plus identifier: `square_id`
- Resulting matrix shape: **(10,000, 241)**

**Missingness:**
- No missing values in the engineered feature matrix (0% missing across features).

**Artifact saved:**
- `results/preprocessing/features_hourly_weekday_weekend_mean.parquet`

---

## Step 1 — Variance-based screening
### Goal
Remove near-constant features that contribute little to clustering.

### Method
Compute feature variances across the 10,000 grid cells and flag features with extremely low variance.

### Results
- Number of features evaluated: **240**
- Min variance: **0.022515547885826965**
- Median variance: **35.919179388631285**
- Low-variance features (var < 1e-6): **0**

### Decision
No features were removed based on variance. All hourly-profile features show meaningful variability across grid cells.

---

## Step 2 — Correlation-based filtering (attempted, then rejected)
### Goal
Remove highly redundant features that increase dimensionality without adding information.

### Attempt A: Global correlation filtering (|r| ≥ 0.95)
**Outcome**
- Features before: 240
- Features removed: 208
- Features retained: 32

**Issue**
The retained features were heavily skewed toward **night/early-morning hours** and entirely dropped key content:
- daytime hours were poorly represented,
- `internet_traffic` features were eliminated (0 retained).

This undermined the project objective because **daily rhythm shape** (commuting/daytime vs leisure/night) is the key clustering signal.

**Artifacts (for traceability)**
- Drop list: `results/preprocessing/correlated_features_to_drop_thr_0.95.csv`

### Attempt B: Correlation filtering within each (regime × channel) group
**Outcome**
Even with a stricter threshold (e.g., 0.975), the retained features still underrepresented daytime hours and retained almost no `internet_traffic` features.

**Issue**
Although this approach avoided some cross-channel conflation, it still collapsed the temporal structure in a way that harms interpretability and the stated use case.

### Decision
Correlation-based filtering was **not used** in the final preprocessing pipeline because it removed the exact structure we aim to cluster: interpretable daily/weekly activity rhythms.

---

## Final decision: Retain the full 240-feature temporal profile
### Rationale
Given:
- the project’s primary signal is *shape over time* (hourly rhythm),
- our sample size is strong (10,000 observations),
- and correlation filtering repeatedly removed key time-of-day coverage,

we retain the full hourly weekday/weekend feature set as the clustering input.

This preserves:
- commuting signatures (morning/evening peaks),
- daytime business activity patterns,
- nighttime/leisure signatures,
- weekday vs weekend contrasts,
- all activity channels, including `internet_traffic`.

### Final artifacts
- Final feature matrix (no correlation dropping):
  - `results/preprocessing/features_hourly_weekday_weekend_mean_FULL.parquet`
- Decision note (short justification):
  - `results/preprocessing/feature_selection_decision.txt`

---

## Notes on interpretability
The retained features map directly to stakeholder-understandable concepts:
- “weekday vs weekend” regimes,
- “hour-of-day” activity rhythms,
- channel-specific intensity differences (calls vs SMS vs internet).

This supports clear cluster profiling and visualization later (e.g., cluster-average hourly curves and spatial maps over the Milan grid).

---

## Next steps (linked to preprocessing pipeline)
Feature selection is complete at this stage. Remaining preprocessing decisions (documented elsewhere) include:
- whether to apply `log1p` and/or robust scaling to handle heavy tails,
- pipeline reproducibility (saving transformations),
- stability testing across preprocessing configurations.