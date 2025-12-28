def map_symptoms_to_features(symptoms):
    return {
        "age": symptoms.age,
        "hypertension": symptoms.high_blood_pressure,
        "heart_disease": int(symptoms.irregular_heartbeat or symptoms.chest_pain),
        "avg_glucose_level": 140,  # fallback
        "bmi": None
    }
