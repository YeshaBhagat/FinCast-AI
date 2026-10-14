"""
Machine Learning Pipeline Module for FinCast AI
Trains an XGBoost Regressor to forecast next-day stock prices and directional trends.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor


def prepare_multimodal_dataset(
    df: pd.DataFrame,
    feature_cols: List[str],
    current_sentiment_score: float
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Fuses technical indicators with sentiment data into a modeling matrix.

    Args:
        df: DataFrame containing technical indicators and targets
        feature_cols: Base list of technical feature column names
        current_sentiment_score: Real-time FinBERT sentiment score for the latest day

    Returns:
        Tuple of (Cleaned DataFrame, Full feature column names including sentiment)
    """
    data = df.copy()

    # Assign sentiment feature column
    # For historical days, simulate a smooth market sentiment with slight momentum correlation
    # For the latest day (today), assign the actual live FinBERT score
    np.random.seed(42)
    hist_sentiment = (
        data['Daily_Return'].fillna(0).clip(-0.05, 0.05) * 10
        + np.random.normal(0, 0.25, len(data))
    ).clip(-1.0, 1.0)

    data['Sentiment_Score'] = hist_sentiment
    data.loc[data.index[-1], 'Sentiment_Score'] = current_sentiment_score

    all_features = feature_cols + ['Sentiment_Score']

    # Drop any initial rows with NaN from rolling indicator windows (e.g., first 30 days)
    data = data.dropna(subset=feature_cols)

    return data, all_features


def train_and_evaluate_model(
    df: pd.DataFrame,
    features: List[str],
    test_ratio: float = 0.2
) -> Dict[str, Any]:
    """
    Performs a chronological time-series train/test split, trains an XGBoost model,
    and computes financial forecasting evaluation metrics.

    Returns:
        Dictionary with trained model, test metrics, predictions, and feature importance.
    """
    # Clean rows with valid target values
    labeled_data = df.dropna(subset=['Target_Next_Close']).copy()
    if len(labeled_data) < 40:
        raise ValueError("Insufficient historical data for model training (requires at least 40 data points).")

    # Train on stationary Target_Return to avoid non-stationary price level bias
    X = labeled_data[features]
    y = labeled_data['Target_Return']

    # Chronological Split (Strictly preserving time order - NO SHUFFLING)
    split_idx = int(len(labeled_data) * (1 - test_ratio))
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    test_dates = labeled_data.index[split_idx:]
    current_close_test = labeled_data.loc[test_dates, 'Close'].values
    actual_next_close_test = labeled_data.loc[test_dates, 'Target_Next_Close'].values

    # Instantiate XGBoost Regressor with regularization to prevent overfitting
    model = XGBRegressor(
        n_estimators=100,
        learning_rate=0.03,
        max_depth=3,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.5,
        reg_lambda=2.0,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Predictions on Test Set (predicted returns)
    predicted_returns_test = model.predict(X_test)
    y_test_pred_price = current_close_test * (1 + predicted_returns_test)

    # Compute Evaluation Metrics
    rmse = float(np.sqrt(mean_squared_error(actual_next_close_test, y_test_pred_price)))
    mae = float(mean_absolute_error(actual_next_close_test, y_test_pred_price))
    r2 = float(r2_score(actual_next_close_test, y_test_pred_price))

    # Directional Accuracy (% of times the model correctly predicts up or down movement)
    actual_direction = (y_test.values > 0).astype(int)
    predicted_direction = (predicted_returns_test > 0).astype(int)
    directional_accuracy = float(np.mean(actual_direction == predicted_direction) * 100)

    # Feature Importance
    importance_scores = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': features,
        'Importance': importance_scores
    }).sort_values(by='Importance', ascending=False).reset_index(drop=True)

    # Test Set Predictions DataFrame for plotting
    test_results_df = pd.DataFrame({
        'Date': test_dates,
        'Actual_Close': actual_next_close_test,
        'Predicted_Close': y_test_pred_price
    }).set_index('Date')

    # Latest row inference for tomorrow's prediction
    latest_row = df[features].iloc[[-1]]
    tomorrow_predicted_return = float(model.predict(latest_row)[0])
    current_price = float(df['Close'].iloc[-1])
    tomorrow_predicted_price = current_price * (1 + tomorrow_predicted_return)
    expected_change = tomorrow_predicted_price - current_price
    expected_change_pct = tomorrow_predicted_return * 100
    predicted_trend = "BULLISH 📈" if expected_change >= 0 else "BEARISH 📉"

    return {
        "model": model,
        "features": features,
        "metrics": {
            "r2_score": round(r2, 4),
            "rmse": round(rmse, 2),
            "mae": round(mae, 2),
            "directional_accuracy_pct": round(directional_accuracy, 1),
            "train_samples": len(X_train),
            "test_samples": len(X_test)
        },
        "forecast": {
            "current_price": round(current_price, 2),
            "predicted_price": round(tomorrow_predicted_price, 2),
            "expected_change": round(expected_change, 2),
            "expected_change_pct": round(expected_change_pct, 2),
            "trend": predicted_trend
        },
        "feature_importance": feature_importance_df,
        "test_results": test_results_df
    }
