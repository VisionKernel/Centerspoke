import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enhanced data cleaning and processing for investment analysis.
    Handles datetime formats, technical indicators, numeric and categorical data.
    """
    df = standardize_datetime(df)
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    df.drop_duplicates(inplace=True)
    df = correct_data_types(df)
    df = add_technical_indicators(df, 'Price')
    return df

def standardize_datetime(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include=['datetime', 'datetime64']):
        df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%dT%H:%M:%S')
    return df

def correct_data_types(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                if df[col].nunique() / len(df[col]) < 0.05:
                    df[col] = df[col].astype('category').cat.codes
    return df

def add_technical_indicators(df: pd.DataFrame, price_column: str) -> pd.DataFrame:
    if price_column in df.columns:
        df['200DMA'] = df[price_column].rolling(window=200).mean()
        df['ReturnVolMetric'] = calculate_return_vol_metric(df, price_column)
        df['RSI'] = calculate_rsi(df, price_column)
        df['MACD'], df['MACDSignal'] = calculate_macd(df, price_column)
    return df

def calculate_return_vol_metric(df: pd.DataFrame, price_column: str) -> pd.Series:
    daily_returns = df[price_column].pct_change()
    return daily_returns.rolling(window=20).mean() / daily_returns.rolling(window=20).std()

def calculate_rsi(df: pd.DataFrame, price_column: str, period: int = 14) -> pd.Series:
    delta = df[price_column].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(df: pd.DataFrame, price_column: str, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> tuple:
    exp1 = df[price_column].ewm(span=fast_period, adjust=False).mean()
    exp2 = df[price_column].ewm(span=slow_period, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal_line

# Example usage commented out for brevity
