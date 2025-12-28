print("🔥 guidance.py LOADED")


# Symptom-based guidance
SYMPTOM_GUIDANCE = {
    "chest_pain": [
        "Avoid heavy physical activity",
        "Seek medical attention if chest pain continues",
        "Reduce oily and spicy food"
    ],
    "shortness_of_breath": [
        "Rest properly",
        "Avoid smoking",
        "Consult a doctor if breathing difficulty increases"
    ],
    "high_blood_pressure": [
        "Reduce salt intake",
        "Check blood pressure regularly",
        "Maintain a healthy weight"
    ],
    "dizziness": [
        "Stay hydrated",
        "Avoid sudden movements",
        "Ensure proper sleep"
    ],
    "snoring_sleep_apnea": [
        "Sleep on your side",
        "Avoid alcohol before sleep",
        "Consult a doctor if snoring is severe"
    ]
}

# Lifestyle-based guidance
LIFESTYLE_GUIDANCE = {
    "smoking": "Gradually reduce and quit smoking",
    "alcohol": "Limit alcohol consumption",
    "physical_inactivity": "Engage in at least 30 minutes of physical activity daily",
    "high_salt_diet": "Reduce salt intake to control blood pressure",
    "poor_sleep": "Aim for 7–8 hours of quality sleep",
    "high_stress": "Practice stress-reducing activities like breathing or prayer"
}

# Fallback preventive guidance (VERY IMPORTANT)
DEFAULT_GUIDANCE = [
    "Maintain a balanced diet with fruits and vegetables",
    "Stay physically active to keep your heart healthy",
    "Monitor blood pressure and blood sugar regularly",
    "Avoid smoking and excessive alcohol consumption"
]


def generate_guidance(symptoms):
    print("🔥 generate_guidance CALLED")
    print("🔥 symptoms dict:", symptoms.dict())
    guidance = []

    # 🔹 Symptom-based guidance
    for symptom, value in symptoms.dict().items():
        if value == 1 and symptom in SYMPTOM_GUIDANCE:
            guidance.extend(SYMPTOM_GUIDANCE[symptom])

    # 🔹 Lifestyle-based guidance
    for habit, text in LIFESTYLE_GUIDANCE.items():
        if getattr(symptoms, habit, 0) == 1:
            guidance.append(text)

    # 🔹 Remove duplicates
    guidance = list(set(guidance))

    # 🔹 Fallback: never return empty guidance
    if not guidance:
        guidance = DEFAULT_GUIDANCE

    return guidance
