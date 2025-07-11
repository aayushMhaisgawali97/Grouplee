
import pandas as pd

def analyze_data(df):
    insights = {}
    time_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    
    if time_cols:
        time_col = time_cols[0]
        df[time_col] = pd.to_datetime(df[time_col])
        df.set_index(time_col, inplace=True)
        trends = df.resample('M').mean(numeric_only=True)
        insights["monthly_trends"] = trends

    # You can add more stats here (e.g. top categories, averages)
    return insights
