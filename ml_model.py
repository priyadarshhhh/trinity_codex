from sklearn.ensemble import IsolationForest

def train_model(df):
    if len(df) < 10:
        return None
    
    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(df[["pH", "TDS", "Turbidity"]])
    
    return model


def detect_anomalies(df, model):
    # ALWAYS create anomaly column
    if "anomaly" not in df.columns:
        df["anomaly"] = 1

    if model is None:
        return df

    try:
        preds = model.predict(df[["pH", "TDS", "Turbidity"]])
        df["anomaly"] = preds
    except Exception as e:
        print("ML Error:", e)
        df["anomaly"] = 1

    return df