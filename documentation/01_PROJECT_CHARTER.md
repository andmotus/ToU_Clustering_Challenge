# PROJECT_CHARTER.md

## Project: Clustering Urban Zones in Milan from Anonymized Telecom Activity

### Purpose and Impact Objective
This project aims to uncover **latent urban zone types** in Milan by clustering spatial grid cells based on their **temporal telecom activity signatures** (calls, SMS, and internet activity aggregated in short time intervals). The intended outcome is an interpretable typology (e.g., residential, business, nightlife, transit-oriented areas) that can support **sustainable mobility planning**, such as targeted service improvements, better infrastructure prioritization, and monitoring of how urban activity patterns change over time.

---

## Anticipated Clustering Families and Rationale

### 1) Partitional Clustering (Primary Family: K-Means as a Baseline)

**Why this family fits the data and objectives**
- **Scale and efficiency:** The dataset can produce many observations once all grid cells and time periods are represented through engineered features. Partitional methods are computationally efficient and suitable for large datasets.
- **Interpretability:** Cluster centroids provide clear “prototype” temporal profiles, which aligns well with the project goal of generating **actionable urban zone categories**.
- **Practical baseline:** K-means provides a strong first benchmark for later comparison with more flexible families.

**Anticipated limitations**
- Assumes relatively **compact / spherical clusters** in feature space.
- Requires pre-specifying **k**.
- Sensitive to outliers and initialization.

**Expected role in this project**
- First-pass clustering on standardized features such as hourly activity profiles, weekday/weekend ratios, and day/night intensity patterns.
- Baseline for computational feasibility and interpretability.

---

### 2) Hierarchical Clustering (Secondary Family: Agglomerative, Ward’s Linkage)

**Why this family is relevant**
- **No need to choose k upfront:** The dendrogram makes it possible to inspect several plausible cluster resolutions.
- **Nested structure:** Urban zones may have hierarchical relationships, for example a broad “commercial” cluster splitting into office-heavy and retail-heavy subtypes.
- **Interpretive value:** Hierarchical results can support explanation and justification of cluster choices in the notebook/report.

**Anticipated limitations**
- Computationally expensive for larger datasets.
- Sensitive to noise and linkage choice.

**Expected role in this project**
- Use **Ward’s linkage** as the main hierarchical option, since it tends to favor compact, variance-minimizing clusters.
- Apply it to engineered grid-cell features rather than the full raw time series.
- Use dendrograms to compare with K-means solutions and support selection of a reasonable number of clusters.

---

## Preliminary Assessment of Additional Clustering Families

### 3) Density-Based Clustering (Exploratory / Conditional Relevance)

**Could arbitrary cluster shapes matter here?**  
Possibly, but not as the main assumption.

The clustering will likely be performed on **engineered temporal feature vectors**, not directly on geographic coordinates. In that feature space, the goal is to find groups of grid cells with similar temporal rhythms. These groups may not necessarily form highly irregular density-connected shapes in the way spatial hotspot data often do.

**Why density-based methods may still be useful**
- They can identify **outlier grid cells** with unusual activity patterns, such as event venues, stadium areas, or highly atypical transport hubs.
- They do not require pre-specifying the number of clusters.
- They can capture **non-spherical groupings** if the feature space turns out to be irregular.

**Why they are not my primary choice**
- DBSCAN is sensitive to parameter tuning (`eps`, `min_samples`).
- It can struggle if the dataset contains clusters with **different densities**, which is plausible here because some Milan zones may have consistently high activity while others are much quieter.
- Performance becomes less reliable in higher-dimensional feature spaces, especially if many temporal profile features are used.

**Preliminary conclusion**  
Density-based methods are likely best treated as an **exploratory complement**, especially for outlier detection or checking whether a few unusual urban zones should be separated from the main cluster structure. They are not currently the leading family for the main analysis.

---

### 4) Model-Based Clustering (Promising Secondary/Comparative Family)

**Could uncertainty in assignments matter here?**  
Yes, quite possibly.

Urban zones are often **mixed-use** rather than purely residential, commercial, or leisure-oriented. That means some grid cells may plausibly belong partly to more than one functional type. In this context, **soft cluster assignments** are conceptually attractive.

**Why model-based methods may be helpful**
- Gaussian Mixture Models (GMMs) provide **probabilistic assignments**, which is useful when boundaries between urban functions are not sharp.
- They can model clusters with **different sizes, orientations, and elliptical shapes**, which may better reflect the geometry of engineered telecom activity features.
- They offer a principled framework for selecting the number of components using **AIC/BIC**.

**Potential limitations**
- More computationally expensive than K-means.
- Depend on distributional assumptions that may not fully match the data.
- Can be sensitive to initialization.

**Preliminary conclusion**  
Model-based clustering appears to be the **most plausible extension beyond partitional/hierarchical methods**, because uncertainty and overlap are realistic features of urban activity patterns. A GMM comparison would be especially valuable if K-means produces clusters that are interpretable but appear to overlap substantially.

---

## Overall Preliminary Position

At this stage, the problem appears to fit **standard assumptions reasonably well as a starting point**, especially after transforming raw telecom observations into aggregated temporal features per grid cell. Therefore:

- **Primary approach:**  
  Partitional clustering (**K-means**) for scalability and clear centroid-based interpretation.

- **Secondary approach:**  
  Hierarchical clustering (**Ward’s linkage**) to inspect nested structure and support selection of the number of clusters.

- **Most promising advanced extension:**  
  **Model-based clustering (GMM)**, because urban zones may exhibit **overlapping functional identities** and uncertain membership.

- **Exploratory alternative:**  
  **Density-based clustering (e.g., DBSCAN)**, mainly to detect unusual or anomalous urban zones rather than as the core method.

---

## Summary
This project will begin with **partitional and hierarchical clustering**, since these methods align well with the current problem framing, dataset size, and interpretability goals. However, the sustainability context also suggests that **mixed-use and ambiguous urban zones** may benefit from model-based methods with soft assignments, while density-based methods may help identify outlier or irregular zones. These considerations will guide detailed algorithm selection and comparison in later project stages.