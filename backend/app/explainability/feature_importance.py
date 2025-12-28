from sklearn.inspection import permutation_importance
import pandas as pd

def get_feature_importance(model, features, top_n=5, X=None, y=None):
    """
    Returns top_n important features for a given model.
    - model: trained scikit-learn model
    - features: list of feature names
    - X, y: optional data to compute permutation importance
    """
    if X is None or y is None:
        # If data not provided, return default importance
        return {f: None for f in features[:top_n]}

    result = permutation_importance(model, X, y, n_repeats=10, random_state=42)
    importance_df = pd.DataFrame({
        "feature": features,
        "importance": result.importances_mean
    })
    importance_df = importance_df.sort_values(by="importance", ascending=False)
    return dict(zip(importance_df["feature"][:top_n], importance_df["importance"][:top_n]))
