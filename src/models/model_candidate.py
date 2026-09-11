import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['month'] = df['timestamp'].dt.month
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['wholesale_momentum_5d'] = df['rbob_wholesale_usd_gal'].diff(5).fillna(0.0)
    df['wholesale_momentum_10d'] = df['rbob_wholesale_usd_gal'].diff(10).fillna(0.0)
    df['wholesale_momentum_20d'] = df['rbob_wholesale_usd_gal'].diff(20).fillna(0.0)
    df['crack_spread_interact'] = df['crude_to_rbob_crack_spread'] * df['is_summer_blend']
    df['refinery_risk_weighted'] = (df['whiting_refinery_outage_risk'] * 0.3 +
                                   df['green_bay_terminal_risk'] * 0.4 +
                                   df['national_refinery_outage_risk'] * 0.3)
    return df[['month', 'day_of_week', 'wti_usd_bbl', 'brent_usd_bbl', 'rbob_wholesale_usd_gal',
               'crude_to_rbob_crack_spread', 'local_price_spread_usd', 'tax_floor_usd',
               'traffic_index', 'is_summer_blend', 'whiting_refinery_outage_risk',
               'green_bay_terminal_risk', 'national_refinery_outage_risk', 'wholesale_momentum_5d',
               'wholesale_momentum_10d', 'wholesale_momentum_20d', 'crack_spread_interact',
               'refinery_risk_weighted']]

def train_and_forecast(df_train: pd.DataFrame, df_test: pd.DataFrame, tomorrow_features: dict) -> dict:
    y_train = df_train['target_escanaba_retail_price'] - df_train['rbob_wholesale_usd_gal'] - df_train['tax_floor_usd']
    X_train = extract_features(df_train)
    X_test = extract_features(df_test)
    
    model = GradientBoostingRegressor(n_estimators=35, max_depth=2, learning_rate=0.04, subsample=0.85)
    model.fit(X_train, y_train)
    
    pred_test = df_test['rbob_wholesale_usd_gal'].values + df_test['tax_floor_usd'].values + model.predict(X_test)
    
    df_tomorrow = pd.DataFrame([tomorrow_features])
    X_tomorrow = extract_features(df_tomorrow)
    pred_tomorrow = float(tomorrow_features['rbob_wholesale_usd_gal'] + tomorrow_features['tax_floor_usd'] + 
                          float(np.ravel(model.predict(X_tomorrow))[0]))
    
    return {
        'model_type': 'GradientBoostingRegressor',
        'test_predictions': pred_test.tolist(),
        'predicted_tomorrow_retail': round(pred_tomorrow, 3),
        'hyperparameters': {
            'n_estimators': 35,
            'max_depth': 2,
            'learning_rate': 0.04,
            'subsample': 0.85
        }
    }