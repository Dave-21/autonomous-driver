import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    df['crude_to_brent_diff'] = df['wti_usd_bbl'] - df['brent_usd_bbl']
    df['refinery_outage_impact'] = df['local_price_spread_usd'] * (df['whiting_refinery_outage_risk'] + 
                                                                  df['green_bay_terminal_risk'] + 
                                                                  df['national_refinery_outage_risk'])
    return df[['month', 'day_of_week', 'wti_usd_bbl', 'brent_usd_bbl', 'rbob_wholesale_usd_gal', 
               'crude_to_rbob_crack_spread', 'local_price_spread_usd', 'tax_floor_usd', 
               'traffic_index', 'is_summer_blend', 'crude_to_brent_diff', 'refinery_outage_impact']].bfill().fillna(0.0)

def train_and_forecast(df_train: pd.DataFrame, df_test: pd.DataFrame, tomorrow_features: dict) -> dict:
    y_train = df_train['target_escanaba_retail_price'] - df_train['rbob_wholesale_usd_gal'] - df_train['tax_floor_usd']
    X_train = extract_features(df_train)
    X_test = extract_features(df_test)
    
    model = GradientBoostingRegressor(n_estimators=35, max_depth=2, learning_rate=0.04, subsample=0.85)
    model.fit(X_train, y_train)
    
    pred_test = df_test['rbob_wholesale_usd_gal'].values + df_test['tax_floor_usd'].values + model.predict(X_test)
    
    df_tomorrow = pd.DataFrame([tomorrow_features])
    pred_tomorrow = float(tomorrow_features['rbob_wholesale_usd_gal'] + tomorrow_features['tax_floor_usd'] + 
                          float(np.ravel(model.predict(extract_features(df_tomorrow)))[0]))
    
    return {'model_type': 'GradientBoostingRegressor', 'test_predictions': pred_test.tolist(), 
            'predicted_tomorrow_retail': round(pred_tomorrow, 3), 'hyperparameters': model.get_params()}