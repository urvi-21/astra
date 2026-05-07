import numpy as np

def create_features(df):
    df = df.copy()

    # Lag features
    df['lag_1'] = df['sales'].shift(1)
    df['lag_7'] = df['sales'].shift(7)

    # Rolling mean
    df['rolling_mean_7'] = df['sales'].rolling(window=7).mean()

    # Time features
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month

    # Synthetic price
    np.random.seed(42)
    df['price'] = 1000 - 0.5 * df['sales'] + np.random.normal(0, 20, len(df))

    df = df.dropna()

    return df


def prepare_data(df):
    features = [
        'lag_1',
        'lag_7',
        'rolling_mean_7',
        'day_of_week',
        'month',
        'price'
    ]

    X = df[features]
    y = df['sales']

    return X, y