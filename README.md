# Project Highlight

This project develops a proactive anomaly detection system for passenger transit data in airport and border control operations.  
The objective is to identify unusual route-level traffic patterns before they become operational or security risks.

The project compares two approaches:

- **Classical Pipeline**: a traditional machine learning workflow using preprocessing, feature engineering, baselines, anomaly detection, and rule-based post-processing.
- **Multi-Agent System**: a modular architecture where specialized agents handle data preparation, baseline construction, anomaly detection, risk profiling, and report generation.

The final output is a **Transit Anomaly Report**, which highlights anomalous patterns, assigns risk levels, and provides understandable explanations for decision-makers.

---

## Repository Structure

```text
src/
├── classical.ipynb
├── multi_agent.ipynb
└── readme.md
```

classical.ipynb:	Implements the classical anomaly detection pipeline
multi_agent.ipynb:	Implements the multi-agent architecture for the same task
readme.md:	Documents the project idea, implementation logic, and main outputs

---
## Implementation Structure
```
        │
        ├── Classical Pipeline
        │       ├── Data Cleaning
        │       ├── Feature Engineering
        │       ├── Baseline Construction
        │       ├── Anomaly Detection
        │       └── Static Output
        │
        └── Multi-Agent System
                ├── Data Agent
                ├── Baseline Agent
                ├── Outlier Detection Agent
                ├── Risk Profiling Agent
                └── Report Agent
```