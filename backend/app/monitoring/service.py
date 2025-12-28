def monitor_model(logs, drift_threshold=0.1):
    """
    Basic drift detection example:
    Compares recent predictions to previous distribution
    """
    if not logs or len(logs) < 20:
        return {"retrain_needed": False}

    last_20 = logs[-20:]
    probs = [rec['probability'] for rec in last_20]

    avg_prob = sum(probs)/len(probs)
    # simple threshold drift check
    if avg_prob > drift_threshold:
        return {"retrain_needed": True}
    return {"retrain_needed": False}
