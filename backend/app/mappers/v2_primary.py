def map_symptoms_to_features(symptoms):
    """
    v2_primary model এর জন্য symptom → model features mapping
    Bangladesh perspective: medium risk / primary care
    """
    return {
        "age": symptoms.age,
        "hypertension": symptoms.high_blood_pressure,
        "heart_disease": int(symptoms.irregular_heartbeat),
        "avg_glucose_level": 130,  # population median fallback
        "bmi": None  # optional, leave None if not available
    }
