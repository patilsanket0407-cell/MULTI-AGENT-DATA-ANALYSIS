import pandas as pd
from pathlib import Path


def insight_agent(file_path):
    """
    Insight Agent

    Analyzes the dataset and generates human-readable
    insights from numerical and categorical data.
    """

    # -------------------------------------------------
    # 1. LOAD DATASET
    # -------------------------------------------------

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)

    elif file_path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)

    else:
        raise ValueError(
            "Unsupported file format. Use CSV or Excel."
        )

    # -------------------------------------------------
    # 2. BASIC DATASET INFORMATION
    # -------------------------------------------------

    insights = []

    rows, columns = df.shape

    insights.append(
        f"The dataset contains {rows} rows and {columns} columns."
    )

    # -------------------------------------------------
    # 3. MISSING VALUE INSIGHTS
    # -------------------------------------------------

    missing_values = df.isnull().sum()

    missing_columns = missing_values[
        missing_values > 0
    ]

    if len(missing_columns) == 0:

        insights.append(
            "The dataset does not contain any missing values."
        )

    else:

        for column, count in missing_columns.items():

            insights.append(
                f"{column} contains {count} missing values."
            )

    # -------------------------------------------------
    # 4. NUMERICAL DATA INSIGHTS
    # -------------------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns[:10]:

        # Skip columns containing no valid values
        if df[column].dropna().empty:
            continue

        mean_value = df[column].mean()
        min_value = df[column].min()
        max_value = df[column].max()

        insights.append(
            f"{column} has an average value of "
            f"{mean_value:.2f}, with values ranging from "
            f"{min_value} to {max_value}."
        )

    # -------------------------------------------------
    # 5. CATEGORICAL DATA INSIGHTS
    # -------------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    for column in categorical_columns[:10]:

        value_counts = df[column].value_counts()

        if len(value_counts) > 0:

            top_category = value_counts.index[0]
            top_count = value_counts.iloc[0]

            percentage = (
                top_count / len(df)
            ) * 100

            insights.append(
                f"In {column}, the most common category is "
                f"'{top_category}', representing "
                f"{percentage:.2f}% of the dataset."
            )

    # -------------------------------------------------
    # 6. ATTRITION-SPECIFIC INSIGHT
    # -------------------------------------------------

    if "Attrition" in df.columns:

        attrition_counts = df[
            "Attrition"
        ].value_counts()

        total = len(df)

        for category, count in attrition_counts.items():

            percentage = (
                count / total
            ) * 100

            insights.append(
                f"Attrition category '{category}' represents "
                f"{percentage:.2f}% of employees."
            )

    # -------------------------------------------------
    # 7. CORRELATION INSIGHTS
    # -------------------------------------------------

    if len(numeric_columns) > 1:

        correlation_matrix = df[
            numeric_columns
        ].corr()

        correlations = []

        for i in range(
            len(correlation_matrix.columns)
        ):

            for j in range(
                i + 1,
                len(correlation_matrix.columns)
            ):

                column1 = (
                    correlation_matrix.columns[i]
                )

                column2 = (
                    correlation_matrix.columns[j]
                )

                correlation_value = (
                    correlation_matrix.iloc[i, j]
                )

                # Ignore NaN correlations
                # caused by constant columns
                if pd.notna(correlation_value):

                    correlations.append(
                        (
                            abs(correlation_value),
                            column1,
                            column2,
                            correlation_value
                        )
                    )

        # Sort by strongest correlation
        correlations.sort(
            reverse=True
        )

        # Add top 5 valid correlations
        for (
            _,
            column1,
            column2,
            value
        ) in correlations[:5]:

            insights.append(
                f"{column1} and {column2} have a "
                f"correlation coefficient of "
                f"{value:.2f}."
            )

    # -------------------------------------------------
    # 8. RETURN RESULTS
    # -------------------------------------------------

    return {
        "insight_summary": {
            "total_insights": len(insights),
            "insights": insights
        }
    }