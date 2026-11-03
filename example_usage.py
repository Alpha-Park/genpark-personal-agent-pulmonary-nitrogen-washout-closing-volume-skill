"""
Example usage of Pulmonary SBN2 Closing Volume Skill.
Demonstrates normal peripheral airway dynamics vs premature small airway closure in smoker.
"""

import json
from client import NitrogenWashoutClosingVolumeClient


def main():
    print("=== Testing Pulmonary SBN2 Closing Volume Skill ===")
    client = NitrogenWashoutClosingVolumeClient()

    # 1. Healthy young non-smoker (VC=4.5L, CV=0.55L -> CV/VC=12.2%, Phase III slope=1.1%/L, FRC=2.8L, CC=1.75L < FRC)
    res_normal = client.evaluate_sbn2(
        vital_capacity_vc_l=4.5,
        closing_volume_cv_l=0.55,
        residual_volume_rv_l=1.2,
        phase3_slope_n2_pct_per_l=1.1,
        functional_residual_capacity_frc_l=2.8,
        patient_age_years=25
    )
    print("\n[Case 1: Normal Small Airway Mechanics]")
    print(json.dumps(res_normal, indent=2))

    # 2. Chronic smoker with small airway dysfunction (VC=4.0L, CV=1.10L -> CV/VC=27.5%, Phase III slope=3.4%/L, FRC=2.5L, CC=2.7L > FRC -> Tidal Closure)
    res_smoker = client.evaluate_sbn2(
        vital_capacity_vc_l=4.0,
        closing_volume_cv_l=1.10,
        residual_volume_rv_l=1.6,
        phase3_slope_n2_pct_per_l=3.4,
        functional_residual_capacity_frc_l=2.5,
        patient_age_years=52
    )
    print("\n[Case 2: Early Small Airway Disease / Tidal Closure]")
    print(json.dumps(res_smoker, indent=2))

    # Assertions
    assert not res_normal["interpretation"]["tidal_airway_closure_detected"]
    assert "Normal" in res_normal["interpretation"]["small_airway_status"]
    assert res_smoker["interpretation"]["tidal_airway_closure_detected"]
    assert "Significant" in res_smoker["interpretation"]["small_airway_status"]
    print("\n[SUCCESS] SBN2 Closing Volume tests passed!")


if __name__ == "__main__":
    main()
