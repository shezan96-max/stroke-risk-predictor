def calculate_drift(old_probs, new_probs):
    """
    Optional advanced drift calculation
    e.g., KL-divergence, Wasserstein distance
    """
    import numpy as np
    old_mean = np.mean(old_probs)
    new_mean = np.mean(new_probs)
    drift = abs(new_mean - old_mean)
    return drift
