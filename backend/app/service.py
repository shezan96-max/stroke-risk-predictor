from config import MODEL_REGISTRY, BANGLADESH_DECISION_POLICY
from app.predictor import load_model, preprocess_input
from app.mappers import v1_clinical, v2_primary, v3_mass
from app.awareness.guidance import generate_guidance
from app.utils.bmi import calculate_bmi
from app.utils.lifestyle import lifestyle_score


def select_model_from_symptoms(symptoms):
    """
    Clinical symptom based initial model selection
    """
    score = (
        symptoms.chest_pain * 3
        + symptoms.shortness_of_breath * 3
        + symptoms.irregular_heartbeat * 3
        + symptoms.dizziness * 2
        + symptoms.fatigue_weakness * 2
        + symptoms.snoring_sleep_apnea * 1
        + symptoms.high_blood_pressure * 1
        + (1 if symptoms.age > 55 else 0)
    )

    if score >= 8:
        return "v1_clinical"
    elif score >= 4:
        return "v2_primary"
    else:
        return "v3_mass"


def predict(symptoms, explain: bool = False):
    """
    Main prediction pipeline (Bangladesh context)
    """

    # 1️⃣ Initial model from clinical symptoms
    model_key = select_model_from_symptoms(symptoms)

    # 2️⃣ BMI calculation (safe)
    bmi = calculate_bmi(symptoms.weight, symptoms.height)

    # 3️⃣ Lifestyle risk score
    life_score = lifestyle_score(symptoms)

    # 4️⃣ Soft model upgrade (BD-safe)
    if model_key == "v3_mass" and life_score >= 3:
        model_key = "v2_primary"

    # 🔍 DEBUG (VERY IMPORTANT – do not remove yet)
    print(f"🔍 Selected model: {model_key}")
    print(f"📊 BMI: {bmi}, Lifestyle score: {life_score}")

    # 5️⃣ Load model
    model_cfg = MODEL_REGISTRY[model_key]
    model_bundle = load_model(model_cfg["path"])

    # 6️⃣ Feature mapping
    if model_key == "v1_clinical":
        features = v1_clinical.map_symptoms_to_features(symptoms)
    elif model_key == "v2_primary":
        features = v2_primary.map_symptoms_to_features(symptoms)
    else:
        features = v3_mass.map_symptoms_to_features(symptoms)

    # 7️⃣ Preprocess
    df = preprocess_input(features, model_bundle["features"])

    # 8️⃣ Prediction
    prob = model_bundle["model"].predict_proba(df)[0][1]
    threshold = model_cfg["threshold"]

    # 9️⃣ Base response
    response = {
        "selected_model": model_key,
        "risk_probability": round(prob, 4),
        "risk": "High Risk" if prob >= threshold else "Low Risk",
        "message": BANGLADESH_DECISION_POLICY[
            model_key.split("_")[0]
        ]["message"],
        "bmi": bmi,
        "lifestyle_score": life_score,
    }

    # 🔟 Personalized guidance (symptom + lifestyle)
    guidance = generate_guidance(symptoms)
    print("🧠 GUIDANCE GENERATED:", guidance)  # 🔥 PROOF LINE
    response["guidance"] = guidance

    # 1️⃣1️⃣ Optional explainability
    if explain:
        from app.explainability.feature_importance import get_feature_importance
        response["top_features"] = get_feature_importance(
            model_bundle["model"],
            model_bundle["features"],
            top_n=5
        )

    return response
