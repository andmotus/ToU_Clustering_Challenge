# PROBLEM_DECOMPOSITION.md

## 1) Ultimate Sustainability Goal (Impact Statement)
Improve the sustainability and equity of urban mobility in Milan by enabling **more targeted, data-informed transport and public-space interventions** that reduce congestion and emissions while improving access and livability.

> Working backwards: a key prerequisite is understanding *how different parts of the city are used over time* (commuting, leisure, mixed-use), because one-size-fits-all mobility policies often miss local dynamics.

---

## 2) Decomposition into Sub-Problems (5W Framework)

Below are candidate sub-problems that collectively support the ultimate goal. Each sub-problem is framed using **Who / What / Where / When / Why**.

### Sub-problem A — Identify functional urban zone types (core clustering target)
- **Who:** Milan grid cells (spatial zones) as analytical units.
- **What:** Distinct temporal “rhythms” of activity (daily/weekly profiles) derived from anonymized telecom activity.
- **Where:** Across the city (grid-based spatial coverage).
- **When:** Short intervals aggregated over days/weeks (captures peaks, weekends, events).
- **Why:** Zone typologies inform where interventions differ (e.g., commuter corridors vs nightlife districts).

### Sub-problem B — Detect anomalous or event-driven zones (outliers / hotspots)
- **Who:** Grid cells with unusual activity dynamics.
- **What:** Spikes, irregular volatility, extreme day/night or weekday/weekend shifts.
- **Where:** Potential event venues, transport hubs, stadium areas, etc.
- **When:** Specific time windows or event periods.
- **Why:** Supports crowd/mobility management and resilience planning (capacity, safety, service provision).

### Sub-problem C — Characterize day vs night mobility intensity patterns
- **Who:** Grid cells and surrounding neighborhoods.
- **What:** Nighttime intensity, nightlife signatures, late-evening peaks.
- **Where:** Central vs peripheral differences.
- **When:** Evening/night periods, weekends.
- **Why:** Relevant for safety, service hours, and night transport provisioning.

### Sub-problem D — Compare weekday commuting vs weekend leisure structure
- **Who:** Grid cells grouped into functional types.
- **What:** Commuting peaks vs leisure-driven usage profiles.
- **Where:** Business districts vs residential vs leisure areas.
- **When:** Weekdays vs weekends; morning/evening rush hours.
- **Why:** Supports scheduling, pricing, and resource allocation decisions.

### Sub-problem E — Assess spatial coherence and mixed-use transition zones
- **Who:** Adjacent grid cells and cluster boundaries.
- **What:** Whether cluster assignments form contiguous regions or fragmented mosaics.
- **Where:** Edge zones between land-use types.
- **When:** Stable vs time-varying patterns.
- **Why:** Helps interpret mixed-use areas and informs “boundary” interventions (e.g., multimodal connectors).

---

## 3) Prioritization: Impact vs Feasibility Matrix

A qualitative 2×2 placement of candidate clustering objectives:

### High Impact + High Feasibility (Start Here)
1. **Cluster grid cells by temporal telecom activity signatures** to infer functional zone types (Sub-problem A).
2. **Weekday vs weekend pattern clustering** for commuting/leisure typologies (Sub-problem D).

### High Impact + Low Feasibility (Longer-term / Stretch)
3. **Event/anomaly discovery at scale** with robust validation against external event calendars or mobility ground truth (Sub-problem B).
4. **Mixed-use transition modeling** with temporal dynamics and spatial constraints (Sub-problem E).

### Low Impact + High Feasibility (Quick Wins / Supporting Analyses)
5. **Day vs night intensity segmentation** as a simple descriptive typology (Sub-problem C).

### Low Impact + Low Feasibility (Deprioritize)
6. Highly granular micro-timing segmentation without a clear decision link (risk of overfitting and weak actionability).

---

## 4) Selected Clustering Problems to Pursue (2–3 Objectives)

### Objective 1 (Primary): Functional Zone Typology
Cluster Milan grid cells into a small set of interpretable **urban activity types** using engineered temporal features from anonymized telecom activity.

### Objective 2 (Secondary): Commute vs Leisure Structure
Identify clusters driven specifically by **weekday commuting peaks** vs **weekend/leisure profiles**, and compare how cluster membership changes across these regimes.

### Objective 3 (Exploratory): Outliers / Anomalous Zones
Identify grid cells that do not fit stable clusters (potential **anomalies/hotspots**) and describe their temporal signatures.

---

## 5) SMART Objective for Top Priority

**Specific:**  
Cluster Milan grid cells using engineered weekly temporal activity features (calls/SMS/internet), aiming to identify a small set of functional zone types.

**Measurable:**  
- Produce **k = 4–8** clusters with:
  - reasonable internal validity (e.g., silhouette/Davies–Bouldin as supporting evidence), and  
  - clear interpretability via cluster-average temporal profiles.
- Provide cluster maps showing spatial distribution and qualitative coherence.

**Achievable:**  
Data are available as anonymized, spatially aggregated telecom activity. Feature engineering will reduce the raw high-frequency series into manageable per-cell representations (e.g., hourly averages, weekday/weekend ratios).

**Relevant:**  
Supports sustainability-focused mobility planning by highlighting where different zones likely require different interventions (service levels, infrastructure, demand management, safety planning).

**Time-bound:**  
Complete data preparation, feature engineering, baseline clustering, and first interpretation within the current course timeline (initial results in the next milestone; refinement and comparison later).

---

## 6) How the Chosen Objective Fits the Larger Sustainability Goal
The primary clustering objective (functional zone typology) provides a **city-wide behavioral map** of how different areas are used over time. This supports more targeted and equitable mobility interventions by shifting analysis from “average city behavior” to **place-specific patterns**, enabling planners to prioritize actions where they matter most (commuter corridors, mixed-use connectors, nightlife districts, etc.).