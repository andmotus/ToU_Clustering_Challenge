# DOCUMENTATION_STANDARDS.md

## Purpose
This document defines documentation and reproducibility standards for this clustering project. The goal is to ensure that all results can be reproduced, reviewed, and communicated clearly to both technical and non-technical audiences.

---

## Repository structure (source of truth)

### Notebooks
Notebooks are organized as a linear pipeline:

- `notebooks/01_load_data.ipynb`  
  Download/ingestion, parsing, data cleaning decisions, saving processed datasets.

- `notebooks/02_EDA.ipynb`  
  Data fitness checks, data adequacy analysis, exploratory plots (saved to `results/eda/`).

- `notebooks/03_preprocessing.ipynb`  
  Feature engineering, feature selection decisions, preprocessing variants, saving artifacts needed for modeling.

- `notebooks/04_model_building.ipynb`  
  Clustering baselines, stability checks, selection of final model (k, preprocessing variant), saving model artifacts.

- `notebooks/05_reporting.ipynb`  
  Final narrative, visualizations, and outputs used for submission/reporting.

### Data folders
- `data/raw/`  
  Raw downloaded telecom files (immutable; never edited).
- `data/processed/`  
  Cleaned and aggregated dataset(s) used as inputs for analysis.

### Results folders
- `results/eda/`  
  All plots and tables produced during EDA and data adequacy checks.
- `results/preprocessing/`  
  Feature matrices, drop lists, scalers, and preprocessing artifacts.
- `results/models/` *(optional; depending on project setup)*  
  Intermediate modeling plots (profiles/maps) and exported tables.

### Model artifacts folder
- `models/`  
  Final model objects and model “cards” used to reproduce the chosen clustering solution.

---

## Naming conventions

### Figures
- All figures must be saved as PNG with meaningful, stable names:
  - EDA figures: `results/eda/<topic>_<detail>.png`
  - Modeling figures: `results/models/profile_k4_internet_traffic_weekday.png`, `gridmap_k4.png`, etc.

### Datasets and feature tables
- Use descriptive names that encode representation and preprocessing:
  - `features_hourly_weekday_weekend_mean_FULL.parquet`
  - `features_FULL_standardscaled.parquet`
  - `features_FULL_log1p_standardscaled.parquet`

### Models
- Model filenames should include key config:
  - `models/kmeans_k4_variantB.joblib`
  - `models/model_card_k4.json`

---

## Reproducibility requirements

### Determinism
- All code that uses randomness must set `random_state` (or a global seed) explicitly.
- KMeans must specify `random_state` and `n_init`.

### Artifact-first workflow
- Downstream notebooks should load from saved artifacts rather than recompute earlier steps.
- Every major step should produce an artifact:
  - processed dataset → feature matrix → scaled variants → chosen model → assignments table.

### Environment management
- Dependencies should be installable from `requirements.txt` (or equivalent).
- If key dependencies change (e.g., `pyarrow`), document it in commits or a short changelog note.

---

## Documentation requirements for decisions
For any decision that affects results, document:

1) **What was done** (exact settings / parameters)  
2) **Why it was done** (objective alignment, evidence from EDA)  
3) **Where it is saved** (path to artifact)  

Examples:
- “Chose log1p + StandardScaler because heavy tails; saved to `results/preprocessing/features_FULL_log1p_standardscaled.parquet`.”
- “Selected k=4 because interpretability + spatial coherence; saved model and assignments in `models/`.”

---

## Required project documentation files (MD)
This project maintains the following decision docs:

- `PROJECT_CHARTER.md`
- `PROBLEM_DECOMPOSITION.md`
- `DATA_METHOD_ALIGNMENT.md`
- `DATA_FITNESS_ASSESSMENT.md`
- `BENEFICIARY_IMPACT.md`
- `STAKEHOLDER_ENGAGEMENT.md`
- `ETHICS_FRAMEWORK.md`
- `TEMPORAL_CLUSTERING_STRATEGY.md`
- `FEATURE_SELECTION.md`
- `PREPROCESSING_DOCUMENTATION.md`
- `DATA_QUALITY_REPORT.md` *(if completed as part of coursework)*
- `DATA_PREPARATION_FINAL.md` *(final dataset summary)*

Each file should contain enough detail for an external reviewer to understand the rationale without reading code.

---

## Output standards for reporting
Final reporting outputs should include:
- a single “primary model” (k + preprocessing variant),
- a cluster summary table (sizes + key metrics),
- cluster-average temporal profiles,
- a Milan grid cluster map,
- clear limitations and ethical caveats.