import os
import pandas as pd
import joblib
from huggingface_hub import hf_hub_download

from config import MODEL_REGISTRY
from utils import COLUMN_MAP
from app.monitoring.store import log_prediction, prediction_logs
from app.monitoring.service import monitor_model
from app.explainability.feature_importance import get_feature_importance


# ===============================
# Hugging Face model config
# ===============================
HF_REPO_ID = "shezan96/stroke-risk-predictor"
HF_FILENAME = "stroke_model.pkl"

LOCAL_MODEL_DIR = "app/models"
LOCAL_MODEL_PATH = os.path.join(LOCAL_MODEL_DIR, HF_FILENAME)

_MODEL_CACHE = {}


# ===============================
# Model download + load
# ===============================
def _ensure_model_downloaded():
    """
    Download model from Hugging Face once (Render-safe)
    """
    if not os.path.exists(LOCAL_MODEL_DIR):
        os.makedirs(LOCAL_MODEL_DIR)

    if not os.path.exists(LOCAL_MODEL_PATH):
        print("⬇️ Downloading model from Hugging Face...")
        hf_hub_download(
            repo_id=HF_REPO_ID,
            filename=HF_FILENAME,
            local_dir=LOCAL_MODEL_DIR,
            repo_type="model"
        )
        print("✅ Model downloaded successfully")


def load_model(model_key):
    """
    Load model bundle (cached).
    - model_key is used ONLY as cache key
    - actual model is shared base model from HF
    """
    if model_key in _MODEL_CACHE:
        return _MODEL_CACHE[model_key]

    _ensure_model_downloaded()

    bundle = joblib.load(LOCAL_MODEL_PATH)
    _MODEL_CACHE[model_key] = bundle
    return bundle


# ===============================
# Preprocessing
# ===============================
def preprocess_input(features_dict, feature_list):
    """
    Map snake_case input → model feature names
    """
    mapped_dict = {
        COLUMN_MAP[k]: v
        for k, v in features_dict.items()
        if k in COLUMN_MAP
    }

    df = pd.DataFrame([mapped_dict])

    # enforce exact training feature order
    for col in feature_list:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_list]
    return df


# ===============================
# Prediction
# ===============================
def predict_risk(features_dict, model_key, explain=False):
    """
    Full risk prediction pipeline
    """
    model_bundle = load_model(model_key)
    df = preprocess_input(features_dict, model_bundle["features"])

    model = model_bundle["model"]
    threshold = MODEL_REGISTRY[model_key]["threshold"]

    prob = model.predict_proba(df)[0][1]
    pred = int(prob >= threshold)
    risk = "High Risk" if pred else "Low Risk"

    # 📊 monitoring
    log_prediction(
        features=df.to_dict(orient="records")[0],
        prob=prob,
        pred=pred
    )

    status = monitor_model(prediction_logs)
    if status.get("retrain_needed"):
        print("⚠️ DRIFT ALERT: Retraining recommended")

    response = {
        "risk": risk,
        "prediction": pred,
        "threshold": threshold,
        "model_version": model_key,
        "probability": round(prob, 4)
    }

    if explain:
        response["top_features"] = get_feature_importance(
            model,
            model_bundle["features"],
            top_n=5,
            X=df,
            y=None
        )

    return response
