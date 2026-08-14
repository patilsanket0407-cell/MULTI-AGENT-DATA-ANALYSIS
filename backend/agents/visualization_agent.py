import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def visualization_agent(file_path):
    """
    Visualization Agent

    Reads a CSV/Excel dataset and automatically generates
    useful visualizations.

    Returns information about the generated charts.
    """

    # -------------------------------------------------
    # 1. LOAD DATASET
    # -------------------------------------------------

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)

    elif file_path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    # -------------------------------------------------
    # 2. CREATE CHART DIRECTORY
    # -------------------------------------------------

    chart_dir = Path("backend/charts")
    chart_dir.mkdir(parents=True, exist_ok=True)

    generated_charts = []

    # -------------------------------------------------
    # 3. NUMERICAL COLUMN VISUALIZATIONS
    # -------------------------------------------------

    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns[:5]:

        plt.figure(figsize=(8, 5))

        df[column].dropna().hist(bins=20)

        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        chart_path = chart_dir / f"{column}_distribution.png"

        plt.savefig(chart_path, bbox_inches="tight")
        plt.close()

        generated_charts.append(str(chart_path))

    # -------------------------------------------------
    # 4. CATEGORICAL COLUMN VISUALIZATIONS
    # -------------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns[:5]:

        # Take top 10 categories
        value_counts = df[column].value_counts().head(10)

        plt.figure(figsize=(9, 5))

        value_counts.plot(kind="bar")

        plt.title(f"Top Categories - {column}")
        plt.xlabel(column)
        plt.ylabel("Count")

        plt.xticks(rotation=45, ha="right")

        chart_path = chart_dir / f"{column}_categories.png"

        plt.savefig(chart_path, bbox_inches="tight")
        plt.close()

        generated_charts.append(str(chart_path))

    # -------------------------------------------------
    # 5. CORRELATION HEATMAP
    # -------------------------------------------------

    if len(numeric_columns) > 1:

        correlation = df[numeric_columns].corr()

        plt.figure(figsize=(10, 8))

        plt.imshow(correlation, cmap="coolwarm")

        plt.colorbar()

        plt.xticks(
            range(len(correlation.columns)),
            correlation.columns,
            rotation=90
        )

        plt.yticks(
            range(len(correlation.columns)),
            correlation.columns
        )

        plt.title("Correlation Matrix")

        chart_path = chart_dir / "correlation_matrix.png"

        plt.savefig(chart_path, bbox_inches="tight")
        plt.close()

        generated_charts.append(str(chart_path))

    # -------------------------------------------------
    # 6. RETURN RESULT
    # -------------------------------------------------

    return {
        "visualization_summary": {
            "total_charts": len(generated_charts),
            "charts": generated_charts
        }
    }