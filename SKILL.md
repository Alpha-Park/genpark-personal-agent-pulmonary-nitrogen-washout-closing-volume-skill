---
name: genpark-personal-agent-pulmonary-nitrogen-washout-closing-volume-skill
version: 1.0.0
description: Calculates Pulmonary Closing Volume (CV), Closing Capacity (CC), CV/VC%, CC/TLC%, and Phase III Slope (delta N2%/L) via Single-Breath Nitrogen Washout.
authors:
  - GenPark Ecosystem
tags:
  - personal-agent
  - pulmonary
  - closing-volume
  - nitrogen-washout
  - small-airway
  - zero-dependency
---

# Pulmonary SBN2 Closing Volume Skill

## Mathematical Formulation

Single-Breath Nitrogen Washout parameters:

$$\text{CC} = \text{CV} + \text{RV}$$
$$\text{TLC} = \text{VC} + \text{RV}$$
$$\text{CV/VC} \, (\%) = \left(\frac{\text{CV}}{\text{VC}}\right) \times 100$$
$$\text{CC/TLC} \, (\%) = \left(\frac{\text{CC}}{\text{TLC}}\right) \times 100$$

Phase III alveolar slope ($\Delta N_2\%/\text{L}$): rate of nitrogen concentration increase during mid-expiration.

Tidal airway closure occurs when:

$$\text{CC} \ge \text{FRC}$$

leading to dependent airway collapse during quiet resting respiration.

## Clinical Interpretation
- **Normal**: Phase III slope $< 1.5\%/\text{L}$, $\text{CC} < \text{FRC}$
- **Mild Small Airway Inhomogeneity**: Phase III slope $1.5 - 2.5\%/\text{L}$
- **Severe Peripheral Airway Disease**: Phase III slope $> 2.5\%/\text{L}$ or $\text{CC} \ge \text{FRC}$ (arterial desaturation risk)
