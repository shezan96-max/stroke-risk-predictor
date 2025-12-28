import pandas as pd
import joblib
from config import MODEL_REGISTRY
from utils import COLUMN_MAP
from app.monitoring.store import log_prediction, prediction_logs
from app.monitoring.service import monitor_model
from app.explainability.feature_importance import get_feature_importance

_MODEL_CACHE = {}

def load_model(path):
    """
    Load model from disk or cache
    """
    if path in _MODEL_CACHE:
        return _MODEL_CACHE[path]
    bundle = joblib.load(f"{path}/stroke_model.pkl")
    _MODEL_CACHE[path] = bundle
    return bundle

def preprocess_input(features_dict, feature_list):
    """
    Map snake_case input → model feature names
    """
    mapped_dict = {COLUMN_MAP[k]: v for k, v in features_dict.items() if k in COLUMN_MAP}
    df = pd.DataFrame([mapped_dict])
    
    # enforce exact training feature order
    missing_cols = [c for c in feature_list if c not in df.columns]
    for c in missing_cols:
        df[c] = 0  # fallback default
    
    df = df[feature_list]
    return df

def predict_risk(features_dict, model_key, explain=False):
    """
    Full risk prediction:
    - features_dict: mapped features for the selected model
    - model_key: v1_clinical / v2_primary / v3_mass
    - explain: whether to return top features
    """
    model_bundle = load_model(MODEL_REGISTRY[model_key]["path"])
    df = preprocess_input(features_dict, model_bundle["features"])
    model = model_bundle["model"]
    threshold = MODEL_REGISTRY[model_key]["threshold"]

    # prediction
    prob = model.predict_proba(df)[0][1]
    pred = int(prob >= threshold)
    risk = "High Risk" if pred else "Low Risk"

    # 📊 monitoring
    log_prediction(features=df.to_dict(orient='records')[0], prob=prob, pred=pred)
    status = monitor_model(prediction_logs)
    if status["retrain_needed"]:
        print("⚠️ DRIFT ALERT: Retraining recommended")

    # response
    response = {
        
        "risk": risk,
        "prediction": pred,
        "threshold": threshold,
        "model_version": model_key
    }

    if explain:
        # optional: requires X, y for permutation importance
        response["top_features"] = get_feature_importance(model, model_bundle["features"], top_n=5, X=df, y=None)

    return response
