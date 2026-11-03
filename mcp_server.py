"""
MCP Server for Pulmonary SBN2 Closing Volume Skill.
Provides standard Model Context Protocol JSON-RPC tool endpoints.
"""

import sys
import json
from client import NitrogenWashoutClosingVolumeClient


def main():
    client = NitrogenWashoutClosingVolumeClient()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        method = req.get("method")
        msg_id = req.get("id")

        if method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "evaluate_sbn2",
                            "description": "Calculates Pulmonary Closing Volume (CV), Closing Capacity (CC), CV/VC%, CC/TLC%, and Phase III Slope (delta N2%/L) via Single-Breath Nitrogen Washout.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "vital_capacity_vc_l": {
                                        "type": "number",
                                        "description": "Vital capacity in Liters (L)."
                                    },
                                    "closing_volume_cv_l": {
                                        "type": "number",
                                        "description": "Measured closing volume in Liters (L)."
                                    },
                                    "residual_volume_rv_l": {
                                        "type": "number",
                                        "description": "Residual volume in Liters (L)."
                                    },
                                    "phase3_slope_n2_pct_per_l": {
                                        "type": "number",
                                        "description": "Phase III alveolar plateau slope in % N2 per Liter."
                                    },
                                    "functional_residual_capacity_frc_l": {
                                        "type": "number",
                                        "description": "Functional residual capacity in Liters (optional)."
                                    },
                                    "patient_age_years": {
                                        "type": "integer",
                                        "description": "Patient age in years (optional)."
                                    }
                                },
                                "required": [
                                    "vital_capacity_vc_l",
                                    "closing_volume_cv_l",
                                    "residual_volume_rv_l",
                                    "phase3_slope_n2_pct_per_l"
                                ]
                            }
                        }
                    ]
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {})

            if name == "evaluate_sbn2":
                try:
                    out = client.evaluate_sbn2(**args)
                    res = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(out, indent=2)}]
                        }
                    }
                except Exception as e:
                    res = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "isError": True,
                        "error": {"code": -32000, "message": str(e)}
                    }
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    main()
