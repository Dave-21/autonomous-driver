import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    # Select only numeric columns and fill missing values with the backfill method
    return df.select_dtypes(include=[np.number]).bfill().fillna(0.0)

def train_and_forecast(df_train: pd.DataFrame, df_test: pd.DataFrame, tomorrow_features: dict) -> dict:
    # Calculate net margin target
    y_train = df_train['target_escanaba_retail_price'] - df_train['rbob_wholesale_usd_gal'] - df_train['tax_floor_usd']
    
    # Extract features
    X_train = extract_features(df_train)
    X_test = extract_features(df_test)
    
    # Initialize and train the model
    model = GradientBoostingRegressor(n_estimators=35, max_depth=2, learning_rate=0.04, subsample=0.85)
    model.fit(X_train, y_train)
    
    # Predict test retail
    pred_test = df_test['rbob_wholesale_usd_gal'].values + df_test['tax_floor_usd'].values + model.predict(X_test)
    
    # Prepare tomorrow's features DataFrame
    df_tomorrow = pd.DataFrame([tomorrow_features])
    pred_tomorrow = float(tomorrow_features['rbob_wholesale_usd_gal'] + tomorrow_features['tax_floor_usd'] + float(np.ravel(model.predict(extract_features(df_tomorrow)))[0]))
    
    # Return results
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