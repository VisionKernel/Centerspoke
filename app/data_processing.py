import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    General data cleaning function applicable to all data types.

    :param df: DataFrame containing the data to be cleaned.
    :return: Cleaned DataFrame.
    """

    # Convert index to date column if it's a DateTimeIndex
    if isinstance(df.index, pd.DatetimeIndex):
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Date'}, inplace=True)
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    # Handling missing values
    # Forward-fill and then backward-fill to handle missing values
    df = df.fillna(method='ffill').fillna(method='bfill')

    # Standardizing formats for other date columns if they exist
    for col in df.select_dtypes(include=['datetime', 'datetime64']):
        df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')

    # Removing duplicates
    df = df.drop_duplicates()

    # Correcting data types for numeric columns
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                pass  # Column is a genuine string column

    # Further processing steps can be added here as needed

    return df
