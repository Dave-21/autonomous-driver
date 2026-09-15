import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    # Feature engineering here using available columns (EXCEPT target_escanaba_retail_price):
    d['rack_spread_ema'] = (d['rbob_wholesale_usd_gal'] - d['wti_usd_bbl']/42.0).ewm(span=3).mean()
    d['crack_spread_volatility_ratio'] = d['crude_to_rbob_crack_spread'].rolling(window=30).std() / d['crude_to_rbob_crack_spread'].rolling(window=30).mean()
    d['tax_floor_ema'] = (d['target_escanaba_retail_price'] - d['tax_floor_usd']).ewm(span=3).mean()
    d['wholesale_acceleration'] = (d['rbob_wholesale_usd_gal'].diff(1) - d['rbob_wholesale_usd_gal'].diff(2)).fillna(0.0)
    d['crack_spread_momentum'] = d['crude_to_rbob_crack_spread'].diff().div(d['crude_to_rbob_crack_spread']).fillna(0.0)
    d['crack_spread_momentum_ratio'] = d['crude_to_rbob_crack_spread'].diff().div(d['crude_to_rbob_crack_spread'].shift(1)).fillna(0.0)
    d['wholesale_acceleration_lag'] = d['wholesale_acceleration'].shift(1).fillna(0.0)
    
    # New features
    d['log_return_wholesale_acceleration'] = np.log(d['wholesale_acceleration'] + 1).diff().fillna(0.0)
    d['momentum_ratio_crack_spread'] = d['crack_spread_momentum'].div(d['crack_spread_momentum'].shift(1)).fillna(0.0)
    
    numeric_cols = [c for c in d.columns if c not in ['timestamp', 'target_escanaba_retail_price'] and pd.api.types.is_numeric_dtype(d[c])]
    return d[numeric_cols].replace([np.inf, -np.inf], np.nan).bfill().ffill().fillna(0.0)

def train_and_forecast(df_train: pd.DataFrame, df_test: pd.DataFrame, tomorrow_features: dict) -> dict:
    y_train = df_train['target_escanaba_retail_price'] - df_train['rbob_wholesale_usd_gal'] - df_train['tax_floor_usd']
    X_train = extract_features(df_train)
    X_test = extract_features(df_test)[X_train.columns]

    # Select architecture and hyperparameters:
    model = ElasticNetCV(l1_ratio=0.7, cv=10)
    model.fit(X_train, y_train)
    pred_margins = model.predict(X_test)
    pred_test = df_test['rbob_wholesale_usd_gal'].values + df_test['tax_floor_usd'].values + pred_margins

    df_tomorrow = pd.DataFrame([tomorrow_features])
    X_tomorrow = extract_features(df_tomorrow)[X_train.columns]
    tomorrow_margin = float(np.ravel(model.predict(X_tomorrow))[0])
    pred_tomorrow = float(tomorrow_features['rbob_wholesale_usd_gal'] + tomorrow_features['tax_floor_usd'] + tomorrow_margin)

    return {
        'model_type': 'ElasticNetCV',
        'test_predictions': pred_test.tolist(),
        'predicted_tomorrow_retail': round(pred_tomorrow, 3),
        'hyperparameters': {'l1_ratio': 0.7, 'cv': 10}
    }