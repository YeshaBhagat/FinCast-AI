"""
Technical Analysis and Feature Engineering Module for FinCast AI
Calculates trend, momentum, volatility, and volume indicators.
"""

from typing import List, Tuple
import numpy as np
import pandas as pd


def compute_technical_indicators(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Computes a comprehensive suite of technical indicators for market modeling.

    Args:
        df: DataFrame with ['Open', 'High', 'Low', 'Close', 'Volume']

    Returns:
        Tuple of (Enriched DataFrame with Target variables, List of feature names)
    """
    data = df.copy()

    # --- 1. Trend Indicators ---
    # Simple Moving Averages
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['SMA_30'] = data['Close'].rolling(window=30).mean()
    data['SMA_Ratio'] = data['SMA_10'] / (data['SMA_30'] + 1e-9)

    # Exponential Moving Averages & MACD
    data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    data['MACD_Hist'] = data['MACD'] - data['MACD_Signal']

    # --- 2. Momentum Indicators ---
    # Relative Strength Index (RSI - 14 period)
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14, min_periods=14).mean()
    avg_loss = loss.rolling(window=14, min_periods=14).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    data['RSI_14'] = 100 - (100 / (1 + rs))

    # --- 3. Volatility Indicators ---
    # Bollinger Bands (20-day window, 2 std dev)
    rolling_mean_20 = data['Close'].rolling(window=20).mean()
    rolling_std_20 = data['Close'].rolling(window=20).std()
    data['BB_Middle'] = rolling_mean_20
    data['BB_Upper'] = rolling_mean_20 + (rolling_std_20 * 2)
    data['BB_Lower'] = rolling_mean_20 - (rolling_std_20 * 2)
    data['BB_Width'] = (data['BB_Upper'] - data['BB_Lower']) / (data['BB_Middle'] + 1e-9)

    # 10-day Rolling Volatility (standard deviation of daily returns)
    daily_returns = data['Close'].pct_change()
    data['Daily_Return'] = daily_returns
    data['Volatility_10'] = daily_returns.rolling(window=10).std()

    # --- 4. Volume Indicators ---
    data['Volume_SMA_10'] = data['Volume'].rolling(window=10).mean()
    data['Volume_Ratio'] = data['Volume'] / (data['Volume_SMA_10'] + 1e-9)

    # --- 5. Target Variables (Next-Day Forward Values) ---
    data['Target_Next_Close'] = data['Close'].shift(-1)
    data['Target_Return'] = (data['Target_Next_Close'] - data['Close']) / data['Close']
    data['Target_Direction'] = (data['Target_Next_Close'] > data['Close']).astype(float)

    # Technical feature columns list (excluding Targets and raw metadata)
    feature_cols = [
        'Close',
        'Volume',
        'Daily_Return',
        'SMA_10',
        'SMA_30',
        'SMA_Ratio',
        'EMA_12',
        'EMA_26',
        'MACD',
        'MACD_Signal',
        'MACD_Hist',
        'RSI_14',
        'BB_Width',
        'Volatility_10',
        'Volume_Ratio'
    ]

    return data, feature_cols
