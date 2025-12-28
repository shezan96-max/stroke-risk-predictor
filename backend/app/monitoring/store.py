# logs/stored in-memory for simplicity
prediction_logs = []

def log_prediction(features, prob, pred):
    """
    Log each prediction for monitoring / drift detection
    """
    record = {
        "features": features,
        "probability": prob,
        "prediction": pred
    }
    prediction_logs.append(record)
    return True
