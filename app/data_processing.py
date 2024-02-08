import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enhanced data cleaning and processing for investment analysis.
    Handles datetime formats, technical indicators, numeric and categorical data.
    """

    # Convert and standardize datetime formats
    df = standardize_datetime(df)

    # Handling missing values
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Correct data types and handle numeric/categorical data
    df = correct_data_types(df)

    # Add technical indicators
    df = add_technical_indicators(df, 'Price')  # Assumes 'Price' column for price-related indicators

    return df

def standardize_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes datetime columns to include time component."""
    for col in df.select_dtypes(include=['datetime', 'datetime64']):
        df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%dT%H:%M:%S')
    return df

def correct_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Converts object columns to numeric where possible, encodes categorical data."""
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                if df[col].nunique() / len(df[col]) < 0.05:  # Threshold for categorical conversion
                    df[col] = df[col].astype('category').cat.codes
    return df

def add_technical_indicators(df: pd.DataFrame, price_column: str) -> pd.DataFrame:
    """Adds technical indicators to the DataFrame, such as the 200-day moving average."""
    if price_column in df.columns:
        df['200DMA'] = df[price_column].rolling(window=200).mean()
        # Placeholder for proprietary return/volatility metric
        df['ReturnVolMetric'] = calculate_return_vol_metric(df, price_column)
    return df

def calculate_return_vol_metric(df: pd.DataFrame, price_column: str) -> pd.Series:
    """Calculates a proprietary return/volatility metric. Placeholder for actual calculation."""
    # Example calculation (to be replaced with actual logic)
    daily_returns = df[price_column].pct_change()
    return daily_returns.rolling(window=20).mean() / daily_returns.rolling(window=20).std()

# Example Usage
if __name__ == "__main__":
    # Simulate loading data (replace with actual data loading logic)
    data = {
        'Date': pd.date_range(start='2020-01-01', periods=5),
        'Price': [100, 102, 104, 103, 105],
        'Sector': ['Tech', 'Tech', 'Finance', 'Healthcare', 'Tech']
    }
    df = pd.DataFrame(data)
    cleaned_df = clean_data(df)
    print(cleaned_df)
