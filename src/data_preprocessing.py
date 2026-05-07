import pandas as pd

def load_and_clean_data(path):
    df = pd.read_csv(path)

    # Convert date
    df['date'] = pd.to_datetime(df['date'])

    # Sort by time
    df = df.sort_values('date')

    # Filter single store-item (important)
    if 'store' in df.columns and 'item' in df.columns:
        df = df[(df['store'] == 1) & (df['item'] == 1)]

    # Reduce dataset size for faster experimentation
    df = df.sample(n=50000, random_state=42)

# Sort again after sampling
    df = df.sort_values("date")

    df = df.reset_index(drop=True)

    return df