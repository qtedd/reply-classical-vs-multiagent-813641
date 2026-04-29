## Introduction

This project focuses on anomaly detection in passenger transit data for border control operations. 
The objective is to identify suspicious patterns in transit flows using both a classical machine learning pipeline and a multi-agent system.

The classical approach combines statistical models and rule-based logic, while the multi-agent system introduces modular and adaptive components. The goal is to compare these approaches in terms of performance, interpretability, and operational suitability.

## Classical
### Data Preparation
#### Passenger Dataset `TIPOLOGIA_VIAGGIATORE`

Several preprocessing steps were applied to ensure consistency and data quality:

- Standardized inconsistent categorical columns (e.g., nationality, document type, airline)
- Converted `DATA_PARTENZA` into a proper datetime format
- Standardized country codes to 3-letter ISO format
- Replaced placeholder values (e.g., `N.D.`) with null values
- Removed duplicate rows
- Standardized airport codes (uppercase formatting)

Logical constraints were enforced:
- `ENTRATI ≥ INVESTIGATI ≥ ALLARMATI`

Violations were corrected using rule-based adjustments. Rows that remained inconsistent were removed.

Additionally:
- Extreme outliers in `ENTRATI` were removed using a conservative upper bound based on realistic aircraft capacity

---

#### Cases Dataset `ALLARMI`

The cases dataset was cleaned with similar principles:

- Removed redundant or low-information columns
- Standardized `DATA_PARTENZA`
- Cleaned and standardized `tot voli`
- Removed duplicate rows
- Replaced placeholder values (`???`, `N/C`, etc.) with `UNKNOWN`
- Standardized categorical values (countries, zones, airport descriptions)
- Fixed logical inconsistencies in region assignments

All columns were translated into English for consistency.

---

### Feature Engineering

#### Analytical Grain

The dataset is aggregated at:

**`date × route_airport`**

This grain was selected because:
- it guarantees uniqueness
- it aligns best with operational behavior
- it provides the most precise level for anomaly detection

`route_city` and `route_country` are retained for interpretability.

---

#### Base Features

Core operational features:

- `entries`
- `investigated`
- `flagged`
- `investigation_rate`
- `flag_rate`
- `flag_given_investigated`

These capture:
- passenger volume
- control intensity
- flagged outcomes

---

#### Calendar Features

Derived from date:

- `year`, `month`, `day`
- `weekday`
- `is_weekend`

These enable detection of:
- temporal patterns
- weekday/weekend effects
- periodic trends

---

#### Segment-Level Features

Aggregated features were created for:

- nationality
- document type
- airline
- control result

For each segment, we compute:

- count (diversity)
- average values
- maximum values
- average and maximum flag rates

This captures:
- passenger heterogeneity
- concentration effects
- segment-level behavioral patterns

---

#### Case-Based Features

Cases data was aggregated and merged using:

**`date + route_airport`**

Features include:

- `has_case_match`
- `case_records`
- `total_flights`
- `unique_alarm_reasons`
- `unique_event_types`
- `alarm_density_per_entry`

Important:

- `has_case_match` is created before filling missing values
- unmatched rows are explicitly preserved
- case features are treated as contextual signals

Case coverage:
- ~34.6% of rows have matching case data

---

#### Temporal Change Features

Time-based features were created per `route_airport`:

- `lag1` → previous value
- `diff1` → absolute change
- `pct_change1` → relative change

Applied to:

- `entries`
- `investigated`
- `flagged`
- `investigation_rate`
- `flag_rate`

These capture:
- trend changes
- sudden increases/decreases
- behavioral shifts

Note:
- Missing values are expected when no previous observation exists
- `pct_change` is undefined when the previous value is zero

---

#### Low-Volume Indicators

Due to strong skewness in traffic:

- ~70% of rows have fewer than 10 entries

Two features were added:

- `is_low_volume`
- `is_low_volume_50`

These preserve information without discarding low-volume observations.

---
Some features were excluded due to:

- high sparsity
- instability (e.g., division by zero issues)

Examples:
- `alarm_density_per_flight`
- some percentage-change variables

The final output provides:

- operational activity signals
- behavioral indicators
- temporal dynamics
- contextual case information

---

### Data Preparation

After feature engineering, two types of historical baselines were added to capture what "normal" looks like for each route:

#### Rolling Averages

Observation-based windows (not calendar-based) were computed per `route_airport` over:

- `entries`, `flag_rate`, `investigation_rate`

For each metric, three columns were created:

- 7-observation rolling mean (`min_periods=3`)
- 30-observation rolling mean (`min_periods=7`)
- Deviation ratio: current value divided by 7-obs rolling mean

Why observation-based windows: the dataset is irregular (median 3-day gap between consecutive observations on the same route, some routes with month-long gaps). A calendar-based 7-day window would often contain only 1-2 data points, making the average unreliable.

#### Monthly Seasonal Baselines

Standard `seasonal_decompose` requires regularly-spaced daily data, which our dataset doesn't provide. We replaced it with a monthly baseline: for each `route_airport × month`, the average entries are computed and used as a reference. Two derived columns capture deviation:

- `entries_residual` — absolute deviation from the monthly baseline
- `entries_residual_z` — z-score normalized per route

A static route-level mean (`entries_route_mean`) is also added as a stable reference, especially useful for routes with too few observations to support rolling windows.

#### Missing Value Handling

A column-group-specific strategy was applied:

- `lag/diff/pct_change` columns: filled with 0 (first observation per route has no previous value)
- `flag_given_investigated`: filled with 0 (undefined when `investigated = 0`)
- Rate columns: filled with 0 (undefined when `entries = 0`)
- Rolling features: filled with column median (routes with too few observations)
- Seasonal features: filled with 0 (single-observation months produce undefined std)

---

### Anomaly Detection

No ground-truth anomaly labels are available in the dataset. 
As a result, the evaluation focuses on relative and operational criteria 
(e.g., consistency, interpretability, and usefulness of detected patterns) 
rather than supervised metrics such as precision or recall.

Three complementary unsupervised methods were applied with `contamination=0.05`:

- **Isolation Forest** — global outliers in high-dimensional space
- **Local Outlier Factor** — local density anomalies
- **Multivariate Z-score** — extreme single-feature outliers

A consensus flag was built through majority voting: an observation is flagged when at least 2 out of 3 methods agree. Fixing `contamination=0.05` ensures comparable detection rates across methods, isolating the value of consensus to *which* rows each model flags rather than how many.

Feature importance was extracted from the Isolation Forest. The deviation ratios, monthly z-score and route mean dominate the ranking — confirming that the Data Preparation step drives most of the detection.

---

### Post-Processing

Four business rules were applied on top of the model output in the initial phase:

- `flag_rate_dev_ratio7 > 3` — flag rate exceeded 3× recent baseline
- `entries_dev_ratio7 > 3` — passenger volume exceeded 3× recent baseline
- `abs(entries_residual_z) > 2` — entries deviate more than 2σ from the monthly norm
- `alarm_density_per_entry > 95th percentile` — disproportionate alarm cases

The final anomaly label combined model consensus and business rules:

`final_anomaly = consensus_anomaly OR rule_any`

This initial approach captured both statistically unusual observations and operational signals. 
However, some rule-based features (e.g., alarm-related variables) relied on post-event information 
and therefore introduced leakage into the detection process.

---

Rule-based logic was subsequently simplified to focus strictly on traffic behavior:

- `entries_dev_ratio7 > threshold` — significant deviation from recent baseline  
- `abs(entries_residual_z) > threshold` — strong deviation from seasonal norm  

Rules based on alarm or investigation activity were removed.

The revised approach ensures that all rule-based signals are derived from pre-intervention data, 
making the detection layer fully causal while preserving interpretability.



## Multi-Agent System

### System Overview

In addition to the classical pipeline, a multi-agent architecture was introduced to improve modularity, flexibility, and interpretability of the anomaly detection process.

The system is composed of specialized agents, each responsible for a specific task in the pipeline. This design allows for separation of concerns and easier extensibility compared to a monolithic approach.

---

### Data Agent

The Data Agent is responsible for:

- loading and preprocessing raw datasets
- applying the same cleaning logic used in the classical pipeline
- enforcing schema consistency across inputs
- preparing structured data for downstream agents

Key responsibilities:
- standardizing column formats and categorical values
- handling missing values and placeholder tokens
- ensuring logical constraints (e.g., `ENTRATI ≥ INVESTIGATI ≥ ALLARMATI`)
- aligning datasets on the common analytical grain (`date × route_airport`)

The Data Agent ensures that all downstream agents operate on clean and consistent data.

---

### Baseline Agent

The Baseline Agent is responsible for constructing reference patterns that define "normal" behavior.

Two types of baselines are implemented:

#### Rolling Baselines
- Observation-based rolling averages (7 and 30 observations)
- Applied per `route_airport`
- Used for:
  - `entries`
  - `flag_rate`
  - `investigation_rate`

These baselines capture short-term dynamics and recent trends, enabling detection of sudden deviations.

#### Seasonal Baselines
- Monthly aggregation per `route_airport × month`
- Used to compute:
  - `entries_residual`
  - `entries_residual_z`

These features capture longer-term seasonal patterns and deviations from expected behavior.

---

### Design Rationale

The separation between Data Agent and Baseline Agent reflects a key principle of the multi-agent system:

- **Data Agent** ensures input quality and consistency  
- **Baseline Agent** defines expected behavior  

This modular structure allows:
- independent updates to preprocessing or baseline logic
- easier debugging and validation
- reuse of agents in different contexts or pipelines

---

### Report Agent

#### Role in the Multi-Agent System

The Report Agent is the final component of the multi-agent anomaly detection workflow. It receives the structured outputs produced by the previous agents and converts them into a clear, human-readable **Transit Anomaly Report**.

The Report Agent acts as an interpretation and communication layer. Its purpose is to explain the detected anomalies in simple operational language, making the results easier to understand for non-technical users such as airport operators, analysts, or decision-makers.

The Report Agent is executed after the following agents:

1. **Data Agent** – filters the data according to the selected airport perimeter.
2. **Baseline Agent** – builds historical baseline indicators for the selected perimeter.
3. **Outlier Detection Agent** – identifies anomalous patterns using statistical and machine learning methods.
4. **Risk Profiling Agent** – assigns a risk level to each flagged pattern.
5. **Report Agent** – generates the final natural-language anomaly report.

---

#### Input

The Report Agent uses the shared LangGraph state as input. In particular, it reads:

```python
state["perimeter"]
state["anomaly_results"]
state["risk_profile"]
```

** The Report Agent depends on the quality of the previous agents' outputs. ** 
If the anomaly detection or risk profiling steps contain errors, the final report may also reflect those errors. <br>
The Report Agent does not independently verify the detected anomalies. It only explains the structured results that it receives from the previous agents.
---