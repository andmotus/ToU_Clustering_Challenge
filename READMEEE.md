# Milan Urban Activity Clustering (Telecom Activity Data)

## Overview
This project clusters urban grid cells in **Milan** into interpretable **urban activity types** using anonymized, spatially aggregated telecom activity (calls, SMS, internet traffic). The goal is to uncover functional zone typologies (e.g., high-activity core vs peripheral zones) from **temporal activity signatures**, supporting sustainability-relevant urban mobility insights.

The workflow is designed to be:
- **Reproducible** (saved artifacts, fixed random seeds, pipeline script),
- **Interpretable** (hourly weekday/weekend profiles, clear visualizations),
- **Documented** (project charter, ethics, stakeholder pathway, data fitness, etc.).

---

## Key Results (Final Model)
- **Algorithm:** KMeans  
- **Selected k:** 4  
- **Preprocessing:** **Variant B** (log1p + StandardScaler)  
- **Features:** 240 per grid cell = 5 channels × 24 hours × (weekday/weekend)

Final cluster labels:
- **High-activity core**
- **Urban mixed-use**
- **Moderate activity**
- **Low activity / peripheral**

Artifacts:
- Model: `models/kmeans_k4_variantB.joblib`
- Assignments: `models/cluster_assignments_k4.parquet` / `models/cluster_assignments_k4.csv`
- Model summary: `models/model_card_k4.json`
- Final figures: `results/final/`

---

## Repository Structure
```
.
├── data/
│   ├── raw/                     # raw telecom files (immutable)
│   └── processed/               # cleaned/aggregated datasets
├── notebooks/
│   ├── 01_load_data.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_preprocessing.ipynb
│   ├── 04_model_building.ipynb
│   └── 05_reporting.ipynb
├── results/
│   ├── eda/                     # EDA plots
│   ├── preprocessing/           # feature matrices + scalers + splits
│   └── final/                   # final reporting figures + tables
├── models/                      # final model + assignments + model card
├── preprocessing_pipeline.py    # reproducible preprocessing script
├── *.md                         # documentation files (charter, ethics, etc.)
└── requirements.txt
```

---

## Data
**Dataset:** anonymized, spatially aggregated telecom activity for Milan grid cells.  
Raw files are stored in `data/raw/`. The processed base table is stored as:

- `data/processed/milan_telecom_agg_all.parquet`

**Important:** This dataset provides **activity proxies**, not individual trajectories or demographics. Clusters should be interpreted as **functional activity profiles**, not measures of social need or value.

---

## Method Summary

### Feature Engineering (Temporal Strategy)
Each grid cell (`square_id`) is represented by mean activity profiles:
- **hour-of-day (0–23)**
- split by **weekday vs weekend**
- across five activity channels

This yields **240 interpretable features per grid cell**.

See: `TEMPORAL_CLUSTERING_STRATEGY.md`

### Preprocessing Variants
To avoid assuming one “correct” preprocessing choice, two variants were created and compared:

- **Variant A:** StandardScaler on raw feature matrix  
  `results/preprocessing/features_FULL_standardscaled.parquet`

- **Variant B (selected):** log1p + StandardScaler  
  `results/preprocessing/features_FULL_log1p_standardscaled.parquet`

See: `PREPROCESSING_DOCUMENTATION.md`

### Clustering & Selection
We evaluated k in a small range and selected:
- **k=4** for interpretability + spatial plausibility  
- **Variant B** for stability

See: `05_reporting.ipynb` and the saved `models/model_card_k4.json`.

---

## How to Run

### 1) Create environment & install dependencies
Using an existing venv (recommended):
```bash
pip install -r requirements.txt
```

### 2) Run preprocessing (reproducible pipeline)
This rebuilds:
- feature matrix
- scaled variants
- scalers
- train/holdout split

```bash
python preprocessing_pipeline.py
```

Outputs land in: `results/preprocessing/`

### 3) Run notebooks (recommended order)
1. `01_load_data.ipynb` — ingest + processed dataset  
2. `02_EDA.ipynb` — data fitness and adequacy checks  
3. `03_preprocessing.ipynb` — feature engineering + preprocessing variants  
4. `04_model_building.ipynb` — KMeans comparison + select k  
5. `05_reporting.ipynb` — final figures + summary tables

---

## Outputs
Final deliverables are in:
- `results/final/` (figures + tables)
- `models/` (final model + assignments)

---

## Documentation (Decision Records)
This repo includes structured documentation files that capture rationale and ethical safeguards:

- `PROJECT_CHARTER.md`
- `PROBLEM_DECOMPOSITION.md`
- `DATA_METHOD_ALIGNMENT.md`
- `DATA_FITNESS_ASSESSMENT.md`
- `FEATURE_SELECTION.md`
- `TEMPORAL_CLUSTERING_STRATEGY.md`
- `PREPROCESSING_DOCUMENTATION.md`
- `BENEFICIARY_IMPACT.md`
- `STAKEHOLDER_ENGAGEMENT.md`
- `ETHICS_FRAMEWORK.md`
- `DATA_PREPARATION_FINAL.md`
- `DOCUMENTATION_STANDARDS.md`

---

## Ethics & Limitations (Quick Notes)
- Data are aggregated/anonymized, but results can still influence perceptions of neighborhoods.
- Labels are functional and **non-stigmatizing**.
- Telecom activity is a proxy for urban intensity, not a direct measure of mobility flows or social outcomes.
- Dataset timeframe (2013–2014) limits modern policy generalization without validation.

See: `ETHICS_FRAMEWORK.md`

---

## License
Add a license if required by your course or if you plan to publish the repo. If unsure, leave this section as “TBD”.

---

## Contact / Author
- Author: <YOUR NAME>
- Program: MSc Data Science
- Course: Clustering
