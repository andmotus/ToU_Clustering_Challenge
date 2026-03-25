# DATA_FITNESS_ASSESSMENT.md

## Purpose
This document evaluates whether the processed Milan telecom dataset is fit for the project’s clustering objective:

**Objective:** cluster Milan grid cells (`square_id`) into interpretable *urban activity types* using temporal signatures derived from aggregated calls/SMS/internet activity.

**Dataset used:** `data/processed/milan_telecom_agg_all.parquet`  
(activities aggregated over `country_code`; NaNs treated as 0 during preprocessing)

---

## 1) Relevance Assessment (Data ↔ Objective)

### What the dataset captures (aligned with objective)
The dataset contains continuous numerical activity measures:
- `sms_in`, `sms_out`, `call_in`, `call_out`, `internet_traffic`

These features plausibly represent **urban intensity and temporal rhythms** (e.g., commuting peaks, daytime commercial activity, nighttime leisure activity) and therefore align with the goal of producing **functional zone typologies**.

### What the dataset does not capture (constraints)
The dataset does **not** include:
- origin–destination mobility flows,
- demographics or equity indicators,
- land use / POIs,
- transit supply or service quality metrics.

**Implication:** clusters should be interpreted as **activity-based functional profiles**, not direct measures of social need, accessibility, or vulnerability. Any sustainability/equity discussion must remain cautious and avoid overstating what telecom activity can represent.

---

## 2) Granularity Matching

### Spatial granularity
- **10,000 grid cells** (`Unique square_id: 10000`) provide fine spatial resolution suitable for zone-level typologies.

### Temporal granularity
- **8,928 unique time intervals** (`Unique time_interval: 8928`), consistent with 10-minute slots.
- This is sufficient to capture intra-day structure, weekday/weekend differences, and event-like spikes.

**Practical consideration:** 10-minute data is likely too granular/noisy for direct clustering. The planned approach remains:
> **temporal feature extraction (hourly/weekly profiles) → clustering on per-cell feature vectors**

---

## 3) Coverage Evaluation

### Overall time coverage
- Datetime range: **2013-10-31 23:00:00 → 2014-01-01 22:50:00**
- Daily interval counts:
  - Typical day: **144 intervals/day** (10-minute resolution across 24 hours)
  - Identified incomplete day: **2013-10-31 has only 6 intervals**
  - **2014-01-01 has 138 intervals** (slightly below full day but not flagged as incomplete by the 90% median rule)

### Coverage by grid cell
Intervals per `square_id`:
- count: 10,000
- mean: **8924.53**
- median (50%): **8928**
- max: **8928**
- min: **2883**

Most grid cells have full temporal coverage, but a small subset has substantially fewer intervals (e.g., min 2883). This indicates **uneven coverage** across space.

**Implication:** For clustering, we may need to:
- filter extremely low-coverage grid cells, or
- design features robust to missing intervals.

---

## 4) Quality Indicators

### Key integrity
- Duplicate rate on (`square_id`, `time_interval`): **0.000000** (no duplicates)
- Negative activity values: **0** across all activity columns

This suggests the aggregated dataset is structurally consistent and free from obvious integrity violations.

### Sparsity / zero structure
Fraction of zeros per channel:
- `call_in`: **0.1698**
- `call_out`: **0.1447**
- `sms_out`: **0.1023**
- `sms_in`: **0.0993**
- `internet_traffic`: **0.0013**

Fraction of rows where **all channels are zero**: **0.0**

**Interpretation:** the dataset is not dominated by complete inactivity, but call channels show meaningful sparsity. This matters for distance-based clustering and may influence scaling/transformation choices.

### Distribution shape (heavy tails)
All channels are strongly right-skewed:
- skew ranges roughly **7.38 to 10.15** across variables.

Extreme values are large relative to medians, for example:
- `internet_traffic` max ≈ **8044**
- `sms_in` max ≈ **1482**
- `sms_out` max ≈ **1079**
- `call_out` max ≈ **526**
- `call_in` max ≈ **413**

**Implication:** clustering on raw scales will likely be dominated by high-activity hotspots unless we apply:
- log / power transforms, and/or
- robust scaling, and/or
- winsorization/clipping for extreme outliers.

---

## 5) Temporal Alignment (Recency and Stability)

The dataset covers late 2013 to early 2014. This is suitable for methodological exploration and demonstrating the clustering workflow, but it limits external validity for *current* Milan mobility decisions.

**Mitigation:** frame results as:
- discovery of generalizable *urban activity typologies*, and
- a method that could be re-applied to more recent data if available.

---

## 6) Fitness Judgment and Constraints

### Fit-for-purpose conclusion
**Yes — fit for clustering functional activity rhythms of urban zones**, because:
- continuous activity measures exist across the full grid,
- temporal granularity supports meaningful rhythm extraction,
- data integrity checks pass (no duplicates/negative values),
- coverage is mostly complete for most grid cells.

### Key constraints to carry forward
- uneven coverage for a subset of grid cells (min intervals far below full coverage),
- heavy-tailed distributions and extreme spikes,
- no socioeconomic / land-use context for equity interpretation.

---

## 7) Recommended Mitigations (to be decided next)

Based on this assessment, the next preprocessing decisions should focus on:

1) **Coverage filtering rule**  
   Decide whether to drop low-coverage grid cells (and define a threshold).

2) **Handling incomplete dates**  
   Decide whether to exclude 2013-10-31 entirely and whether to treat 2014-01-01 as acceptable or partially incomplete.

3) **Transformations for heavy tails**  
   Decide between log-transform, robust scaling, and/or clipping to prevent clustering from being dominated by extreme hotspots.

4) **Temporal aggregation for feature engineering**  
   Decide which representation best supports interpretability (e.g., hourly mean profiles, weekday/weekend profiles, day/night ratios).