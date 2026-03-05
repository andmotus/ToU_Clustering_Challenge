# DATA_METHOD_ALIGNMENT.md

## Purpose
This document explains how the **characteristics of the Milan telecom dataset** align with different clustering approaches. The goal is to justify, at a preliminary level, which methods are most appropriate and what preprocessing choices will likely be required. This rationale will guide later decisions on feature engineering, algorithm selection, and evaluation.

---

## 1) Data Characteristics of the Project

The project uses anonymized, spatially aggregated telecom activity from Milan. At a conceptual level, the data combine several important characteristics:

- **Continuous numerical data**  
  Activity variables such as SMS, call, and internet traffic are numerical and can be aggregated into continuous feature representations.

- **Temporal data / time series structure**  
  Activity is recorded in short time intervals, so each grid cell has a temporal signature rather than a single static value.

- **Spatial data**  
  Observations correspond to grid cells in Milan, meaning that geographic context matters for interpretation, even if clustering is performed primarily in feature space.

- **Potentially high-dimensional data after feature engineering**  
  If each grid cell is represented by many hourly, daily, or channel-specific variables, the final feature space may become moderately or highly dimensional.

This means the project is **not a purely spatial clustering problem** and not a purely static numerical one. Instead, it is best understood as a **temporal-behavior clustering problem with spatial interpretation**.

---

## 2) Primary Data–Method Alignment

### A) Continuous Numerical Features → Partitional / Hierarchical / Model-Based Methods

After preprocessing, each grid cell will likely be represented as a vector of engineered numerical features, such as:

- mean hourly activity,
- weekday vs weekend ratios,
- day vs night intensity,
- variability measures,
- channel-specific usage summaries.

This makes the core analysis well suited to clustering methods designed for **continuous numerical data**, especially:

- **K-means**
- **Hierarchical clustering**
- **Gaussian Mixture Models (GMMs)**

### Why this alignment makes sense
- These methods work naturally on standardized numerical feature vectors.
- Cluster centers or component means can be interpreted as **typical urban activity profiles**.
- This supports the project goal of identifying interpretable zone types such as residential, business, leisure, or transport-oriented areas.

### Likely preprocessing needs
- **Feature scaling / standardization**
- **Outlier detection or robust handling**
- Possible transformation of highly skewed activity variables

---

## 3) Temporal Data Alignment

The raw dataset has a clear **time-series structure**, since activity is observed repeatedly over short time intervals.

### Relevant methodological implication
For temporal data, two broad options exist:

1. **Use raw/semi-raw time series directly** with time-series clustering approaches.
2. **Extract summary features** from the time series and then apply standard clustering.

### Preliminary choice for this project
The second option is more appropriate:

- engineer meaningful temporal features first,
- then apply standard clustering methods.

### Why
- It is more interpretable for an urban sustainability use case.
- It reduces noise and dimensionality.
- It is easier to explain and validate in a master’s-level project.
- It aligns better with the impact objective of producing actionable zone typologies rather than purely algorithmic sequence groupings.

So although the data are temporal, the likely working approach is:

**temporal feature extraction → clustering in feature space**

rather than full DTW-based time-series clustering.

---

## 4) Spatial Data Alignment

The data are spatial because each record belongs to a grid cell in Milan. However, the main analytical goal is not simply to group nearby locations, but to group locations with **similar temporal activity behavior**.

### Implication
Spatial information matters primarily for:
- **interpreting cluster outputs** on a map,
- checking whether clusters are geographically plausible,
- potentially adding spatial coherence as a secondary consideration.

### Methods potentially relevant
- **DBSCAN** could be useful if spatially irregular hotspot-like patterns are important.
- **Spatially constrained clustering** could be considered later if geographic contiguity becomes essential.

### Preliminary conclusion
Spatial structure is important, but it is **secondary to temporal-behavior similarity** in the current project design. Therefore, purely spatial clustering methods are not the main starting point.

---

## 5) High-Dimensionality Considerations

If many temporal features are created per grid cell, the dataset may become moderately high-dimensional. For example:

- 24 hourly averages,
- separate features for calls, SMS, and internet,
- weekday/weekend splits,
- variability measures.

This can lead to:
- redundancy among features,
- correlation structure,
- reduced performance of distance-based clustering.

### Methodological implications
If dimensionality becomes too high, the project may benefit from:
- **feature selection** based on domain relevance,
- **PCA** for dimensionality reduction before clustering,
- visualization in reduced space for interpretation.

### Preliminary stance
Dimensionality reduction is not the primary method family, but it may become an important **preprocessing step** before applying K-means, hierarchical clustering, or GMMs.

---

## 6) Mixed Data and Network Data Relevance

### Mixed data
At present, the core dataset is mainly numerical after preprocessing, so mixed-data clustering is **not central** to the initial analysis. Mixed methods would become more relevant only if external categorical attributes were added later (e.g., land-use labels, administrative classes, event types).

### Network / graph data
The current project is not framed as a graph clustering problem. If later extensions model flows or interactions between zones, network-based methods could become relevant. For now, this is outside the primary scope.

---

## 7) Preliminary Method Recommendation

Based on the data characteristics, the strongest alignment is:

### Best-fitting main approach
**Engineered temporal numerical features + standard clustering methods**

This suggests the following progression:

1. **Preprocess and aggregate raw telecom activity**
2. **Engineer interpretable temporal features per grid cell**
3. **Scale features**
4. Optionally apply **PCA** if dimensionality is too high
5. Compare clustering methods suited to continuous numerical data:
   - **K-means** as baseline
   - **Hierarchical clustering** for structure exploration
   - **Gaussian Mixture Models** if soft assignments and overlap appear important

---

## 8) Implications for Later Milestones

This alignment suggests the following preprocessing and modeling priorities for the next stages:

### Preprocessing priorities
- aggregate over time and possibly country code as needed,
- construct grid-cell feature vectors,
- standardize numerical variables,
- inspect skewness and outliers,
- reduce dimensionality if necessary.

### Algorithm selection priorities
- start with **K-means** for scalability and interpretability,
- use **hierarchical clustering** to inspect possible cluster structures,
- consider **GMMs** if mixed-use or overlapping zone identities appear plausible,
- treat **DBSCAN** as exploratory rather than primary.

---

## Summary
The Milan telecom dataset is best treated as a **temporal numerical dataset with spatial interpretation**. This makes **feature-based clustering on engineered continuous variables** the most suitable strategy. Standard methods such as **K-means, hierarchical clustering, and potentially GMMs** are well aligned with the data and the project’s impact goal of identifying interpretable urban zone types for sustainable mobility planning.