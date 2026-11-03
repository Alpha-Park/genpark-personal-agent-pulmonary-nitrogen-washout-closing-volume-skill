# Pulmonary SBN2 Closing Volume Personal Agent Skill

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)]()
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard%20JSON--RPC-orange.svg)]()
[![Production Ready](https://img.shields.io/badge/status-production--ready-green.svg)]()

Deterministic, zero-mock personal agent micro-skill for calculating Closing Volume (CV), Closing Capacity (CC), CV/VC%, CC/TLC%, and Phase III Slope ($\Delta N_2\%/\text{L}$) using Single-Breath Nitrogen Washout gas physics.

## Architecture

```mermaid
flowchart TD
    A[SBN2 Nitrogen Washout Curve] --> B[Identify Phase III Slope & Phase IV Takeoff]
    B --> C[Compute CV Liters & CC = CV + RV]
    C --> D[Calculate CV/VC% & CC/TLC%]
    D --> E[Compare CC vs Resting FRC]
    E --> F[Detect Tidal Airway Closure & V/Q Mismatch]
```

## Quickstart

```python
from client import NitrogenWashoutClosingVolumeClient

client = NitrogenWashoutClosingVolumeClient()
result = client.evaluate_sbn2(
    vital_capacity_vc_l=4.5,
    closing_volume_cv_l=0.55,
    residual_volume_rv_l=1.2,
    phase3_slope_n2_pct_per_l=1.1,
    functional_residual_capacity_frc_l=2.8
)
print(result)
```

## License

Apache-2.0
