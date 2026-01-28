import pandas as pd
from sklearn.ensemble import IsolationForest


FEATURE_COLS = ["dst_port", "bytes"]


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Anomali tespiti için kullanılacak temel sayısal özellikleri hazırlar.
    Geliştirmek istersen buraya yeni kolonlar ekleyebilirsin.
    """
    feat_df = df.copy()
    for col in FEATURE_COLS:
        if col not in feat_df.columns:
            feat_df[col] = 0
    feat_df = feat_df[FEATURE_COLS].fillna(0)
    return feat_df


def run_isolation_forest(df: pd.DataFrame, contamination: float = 0.02) -> pd.DataFrame:
    """
    Isolation Forest ile basit anomali tespiti yapar.

    contamination: Verinin yaklaşık ne kadarının anomali olduğunu tahmin ediyorsun (% olarak).
    """
    if df.empty:
        df["anomaly_score"] = []
        return df

    X = prepare_features(df)
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42,
    )
    df = df.copy()
    df["anomaly_score"] = model.fit_predict(X)  # -1: anomali, 1: normal
    return df

