import os
import matplotlib.pyplot as plt
import seaborn as sns
import openai

# Ensure output folder exists
os.makedirs("outputs", exist_ok=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_charts(df):
    chart_info = []

    numeric_cols = df.select_dtypes(include='number').columns
    categorical_cols = df.select_dtypes(exclude='number').columns

    for col in numeric_cols:
        # Histogram
        plt.figure(figsize=(8, 6))
        sns.histplot(df[col].dropna())
        plt.title(f'Distribution of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        hist_path = f"outputs/{col}_hist.png"
        plt.savefig(hist_path)
        plt.close()

        # Line plot (trend over index)
        plt.figure(figsize=(8, 6))
        plt.plot(df.index, df[col])
        plt.title(f'Trend of {col} over Index')
        plt.xlabel('Index')
        plt.ylabel(col)
        line_path = f"outputs/{col}_line.png"
        plt.savefig(line_path)
        plt.close()

        # GPT-generated description
        description = generate_gpt_insight(col)

        chart_info.append({
            "title": f"{col} Histogram",
            "file": hist_path,
            "description": description
        })
        chart_info.append({
            "title": f"{col} Trend Line",
            "file": line_path,
            "description": description
        })

    # If 2 numeric cols, make scatter plot
    if len(numeric_cols) >= 2:
        x_col = numeric_cols[0]
        y_col = numeric_cols[1]
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=df[x_col], y=df[y_col])
        plt.title(f'Scatter: {x_col} vs {y_col}')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        scatter_path = f"outputs/scatter_{x_col}_vs_{y_col}.png"
        plt.savefig(scatter_path)
        plt.close()

        description = generate_gpt_insight(f"Scatter: {x_col} vs {y_col}")

        chart_info.append({
            "title": f"{x_col} vs {y_col} Scatter",
            "file": scatter_path,
            "description": description
        })

    # If categorical + numeric → pie or bar chart
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        cat_col = categorical_cols[0]
        num_col = numeric_cols[0]
        group = df.groupby(cat_col)[num_col].sum()

        # Pie chart
        plt.figure(figsize=(8, 8))
        group.plot(kind='pie', autopct='%1.1f%%')
        plt.title(f'{num_col} by {cat_col} (Pie)')
        pie_path = f"outputs/{num_col}_by_{cat_col}_pie.png"
        plt.savefig(pie_path)
        plt.close()

        # Bar chart
        plt.figure(figsize=(10, 6))
        group.plot(kind='bar')
        plt.title(f'{num_col} by {cat_col} (Bar)')
        plt.xlabel(cat_col)
        plt.ylabel(num_col)
        bar_path = f"outputs/{num_col}_by_{cat_col}_bar.png"
        plt.savefig(bar_path)
        plt.close()

        description = generate_gpt_insight(f"{num_col} by {cat_col}")

        chart_info.append({
            "title": f"{num_col} by {cat_col} Pie",
            "file": pie_path,
            "description": description
        })
        chart_info.append({
            "title": f"{num_col} by {cat_col} Bar",
            "file": bar_path,
            "description": description
        })

    return chart_info


def generate_gpt_insight(prompt_topic):
    prompt = f"Give a short, simple description for a chart about: {prompt_topic}"
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data analyst assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']
