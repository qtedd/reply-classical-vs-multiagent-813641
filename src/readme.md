## Data Preparation
### Passenger Dataset `TIPOLOGIA_VIAGGIATORE`

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

### Cases Dataset `ALLARMI`

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

## Feature Engineering

### Analytical Grain

The dataset is aggregated at:

**`date × route_airport`**

This grain was selected because:
- it guarantees uniqueness
- it aligns best with operational behavior
- it provides the most precise level for anomaly detection

`route_city` and `route_country` are retained for interpretability.

---

### Base Features

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

### Calendar Features

Derived from date:

- `year`, `month`, `day`
- `weekday`
- `is_weekend`

These enable detection of:
- temporal patterns
- weekday/weekend effects
- periodic trends

---

### Segment-Level Features

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

### Case-Based Features

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

### Temporal Change Features

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

### Low-Volume Indicators

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