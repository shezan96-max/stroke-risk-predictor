def map_symptoms_to_features(symptoms):
    """
    v3_mass model এর জন্য symptom → model features mapping
    Bangladesh perspective: mass screening / low-risk population
    """
    return {
        "age": symptoms.age,
        "hypertension": 0,  # assume unknown for mass screening
        "heart_disease": 0,  # assume unknown
        "avg_glucose_level": 120,  # baseline/fallback
        "bmi": None  # optional
    }
