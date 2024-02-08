import pandas as pd
import numpy as np
from scipy.stats import norm

def calculate_mean(df, column):
    return df[column].mean()

def calculate_variance(df, column):
    return df[column].var()

def calculate_standard_deviation(df, column):
    return df[column].std()

def calculate_z_score(df, column):
    mean = calculate_mean(df, column)
    std_dev = calculate_standard_deviation(df, column)
    df[f'{column}_z_score'] = (df[column] - mean) / std_dev
    return df

# Example Black-Scholes function for call options
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    return call_price

# Add more functions as needed
