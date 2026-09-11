import numpy as np
import pandas as pd
from sklearn.linear_model import HuberRegressor, RidgeCV
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    # Feature transformations here...
    # Drop non-numeric columns like 'timestamp'
    numeric_df = d.select_dtypes(include=[np.number])
    return numeric_df.bfill().fillna(0.0)

def train_and_forecast(df_train: pd.DataFrame, df_test: pd.DataFrame, tomorrow_features: dict) -> dict:
    y_train = df_train['target_escanaba_retail_price'] - df_train['rbob_wholesale_usd_gal'] - df_train['tax_floor_usd']
    X_train = extract_features(df_train.drop(columns=['target_escanaba_retail_price'], errors='ignore'))
    X_test = extract_features(df_test.drop(columns=['target_escanaba_retail_price'], errors='ignore'))
    # Ensure X_test has identical columns as X_train
    X_test = X_test[X_train.columns]

    model = HuberRegressor(alpha=1.0, epsilon=1.35)  # Or GradientBoostingRegressor, RidgeCV
    model.fit(X_train, y_train)
    pred_margins = model.predict(X_test)
    pred_test = df_test['rbob_wholesale_usd_gal'].values + df_test['tax_floor_usd'].values + pred_margins

    df_tomorrow = pd.DataFrame([tomorrow_features])
    X_tomorrow = extract_features(df_tomorrow)[X_train.columns]
    tomorrow_margin = float(np.ravel(model.predict(X_tomorrow))[0])
    pred_tomorrow = float(tomorrow_features['rbob_wholesale_usd_gal'] + tomorrow_features['tax_floor_usd'] + tomorrow_margin)

    return {
        'model_type': 'HuberRegressor',
        'test_predictions': pred_test.tolist(),
        'predicted_tomorrow_retail': round(pred_tomorrow, 3),
        'hyperparameters': {'alpha': 1.0, 'epsilon': 1.35}
    }