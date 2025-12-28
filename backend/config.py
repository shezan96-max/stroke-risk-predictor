MODEL_REGISTRY = {
    "v1_clinical": {
        "path": "app/model/v1_clinical",
        "threshold": 0.5
    },
    "v2_primary": {
        "path": "app/model/v2_primary",
        "threshold": 0.4
    },
    "v3_mass": {
        "path": "app/model/v3_mass",
        "threshold": 0.3
    }
}

BANGLADESH_DECISION_POLICY = {
    "v1": {"message": "High risk detected: follow medical advice immediately."},
    "v2": {"message": "Moderate risk: monitor lifestyle and symptoms."},
    "v3": {"message": "Low risk: maintain healthy lifestyle and regular checkups."}
}
