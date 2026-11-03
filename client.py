"""
Pulmonary Single-Breath Nitrogen Washout (SBN2) Closing Volume Client.
Zero-mock pure Python standard library implementation.
Calculates Closing Volume (CV), Closing Capacity (CC), CV/VC%, CC/TLC%,
and Phase III Alveolar Plateau Slope (delta N2%/L) for small airway evaluation.
"""

import math
from typing import Dict, Any, Optional


class NitrogenWashoutClosingVolumeClient:
    """
    Evaluates peripheral airway closure and ventilation distribution via Single-Breath Nitrogen Washout:
    - Phase III slope (delta N2 % / Liter): alveolar plateau slope (ventilation inhomogeneity)
    - Closing Volume (CV, L): volume expired from Phase IV takeoff point to RV
    - Closing Capacity (CC, L): CC = CV + RV
    - CV/VC%: (CV / VC) * 100
    - CC/TLC%: (CC / TLC) * 100
    - Tidal airway closure risk: when CC >= FRC, airway closure occurs during normal breathing
    """

    def __init__(self):
        pass

    def evaluate_sbn2(
        self,
        vital_capacity_vc_l: float,
        closing_volume_cv_l: float,
        residual_volume_rv_l: float,
        phase3_slope_n2_pct_per_l: float,
        functional_residual_capacity_frc_l: Optional[float] = None,
        patient_age_years: Optional[int] = 35
    ) -> Dict[str, Any]:
        """
        Calculates closing volume metrics.
        vital_capacity_vc_l: slow or forced vital capacity (L)
        closing_volume_cv_l: measured closing volume (L)
        residual_volume_rv_l: residual volume (L)
        phase3_slope_n2_pct_per_l: Phase III slope (% N2 / L)
        functional_residual_capacity_frc_l: resting FRC (L)
        """
        if vital_capacity_vc_l <= 0 or closing_volume_cv_l <= 0 or residual_volume_rv_l <= 0:
            raise ValueError("Lung volume measurements must be strictly positive.")
        if closing_volume_cv_l >= vital_capacity_vc_l:
            raise ValueError("Closing volume cannot exceed vital capacity.")
        if phase3_slope_n2_pct_per_l < 0:
            raise ValueError("Phase III slope cannot be negative.")

        # Closing Capacity (L)
        closing_capacity_cc_l = closing_volume_cv_l + residual_volume_rv_l

        # Total Lung Capacity (L)
        tlc_l = vital_capacity_vc_l + residual_volume_rv_l

        # Volume ratios
        cv_vc_ratio_pct = (closing_volume_cv_l / vital_capacity_vc_l) * 100.0
        cc_tlc_ratio_pct = (closing_capacity_cc_l / tlc_l) * 100.0

        # Normal predicted values adjust with age:
        # Predicted CV/VC% ~ 10.0 + (0.15 * age)
        # Predicted CC/TLC% ~ 25.0 + (0.35 * age)
        age = patient_age_years if patient_age_years else 35
        pred_cv_vc = 10.0 + (0.15 * age)
        pred_cc_tlc = 25.0 + (0.35 * age)

        # Tidal airway closure assessment:
        # If CC >= FRC, airways close during regular resting tidal respiration, leading to ventilation-perfusion mismatch
        tidal_closure_detected = False
        tidal_closure_margin_l = None
        if functional_residual_capacity_frc_l:
            tidal_closure_margin_l = round(closing_capacity_cc_l - functional_residual_capacity_frc_l, 2)
            tidal_closure_detected = closing_capacity_cc_l >= functional_residual_capacity_frc_l

        # Diagnostic classification:
        # Phase III slope > 2.5 %/L -> Severe ventilation inhomogeneity / small airway disease
        # Phase III slope 1.5 - 2.5 %/L -> Borderline / Mild ventilation unevenness
        # Phase III slope < 1.5 %/L -> Uniform alveolar gas distribution
        if phase3_slope_n2_pct_per_l > 2.5 or cv_vc_ratio_pct > (pred_cv_vc * 1.4):
            small_airway_status = "Significant Small Airway Disease / Premature Closure"
            clinical_significance = "Marked peripheral bronchomotor dysfunction or early emphysematous loss of alveolar tethering."
        elif phase3_slope_n2_pct_per_l > 1.8 or cv_vc_ratio_pct > (pred_cv_vc * 1.2):
            small_airway_status = "Mild Peripheral Airway Dysfunction"
            clinical_significance = "Subclinical ventilation distribution heterogeneity (often observed in early tobacco/vaping exposure)."
        else:
            small_airway_status = "Normal Small Airway Dynamics"
            clinical_significance = "Homogeneous alveolar emptying with physiological dependent airway stability."

        return {
            "status": "success",
            "volumes_liters": {
                "vital_capacity_vc_l": round(vital_capacity_vc_l, 2),
                "closing_volume_cv_l": round(closing_volume_cv_l, 2),
                "residual_volume_rv_l": round(residual_volume_rv_l, 2),
                "closing_capacity_cc_l": round(closing_capacity_cc_l, 2),
                "total_lung_capacity_tlc_l": round(tlc_l, 2),
                "functional_residual_capacity_frc_l": round(functional_residual_capacity_frc_l, 2) if functional_residual_capacity_frc_l else None
            },
            "indices": {
                "cv_vc_ratio_pct": round(cv_vc_ratio_pct, 1),
                "predicted_cv_vc_pct": round(pred_cv_vc, 1),
                "cc_tlc_ratio_pct": round(cc_tlc_ratio_pct, 1),
                "predicted_cc_tlc_pct": round(pred_cc_tlc, 1),
                "phase3_slope_n2_pct_per_l": round(phase3_slope_n2_pct_per_l, 2)
            },
            "interpretation": {
                "small_airway_status": small_airway_status,
                "clinical_significance": clinical_significance,
                "tidal_airway_closure_detected": tidal_closure_detected,
                "cc_minus_frc_margin_l": tidal_closure_margin_l
            }
        }
