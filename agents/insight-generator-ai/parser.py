import pandas as pd

def load_data(filepath):
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filepath.endswith(".xlsx"):
        df = pd.read_excel(filepath)
    else:
        raise ValueError("Unsupported file format. Upload CSV or Excel.")
    return df
