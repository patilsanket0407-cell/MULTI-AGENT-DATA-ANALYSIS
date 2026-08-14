import pandas as pd
import numpy as np


def pattern_agent(file_path):
    """
    Detect important patterns in a dataset.
    """

    # Load dataset
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format")

    patterns = {
        "correlations": [],
        "outliers": [],
        "categorical_patterns": []
    }

    # ------------------------------------------------
    # 1. CORRELATION DETECTION
    # ------------------------------------------------

    numeric_df = df.select_dtypes(include=np.number)

    if len(numeric_df.columns) > 1:

        correlation_matrix = numeric_df.corr()

        for column1 in correlation_matrix.columns:

            for column2 in correlation_matrix.columns:

                # Avoid comparing a column with itself
                if column1 >= column2:
                    continue

                correlation_value = correlation_matrix.loc[
                    column1, column2
                ]

                if abs(correlation_value) >= 0.7:

                    patterns["correlations"].append({
                        "feature_1": column1,
                        "feature_2": column2,
                        "correlation": round(
                            float(correlation_value), 2
                        )
                    })

    # ------------------------------------------------
    # 2. OUTLIER DETECTION
    # ------------------------------------------------

    for column in numeric_df.columns:

        Q1 = numeric_df[column].quantile(0.25)
        Q3 = numeric_df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = numeric_df[
            (numeric_df[column] < lower_bound) |
            (numeric_df[column] > upper_bound)
        ]

        if len(outliers) > 0:

            patterns["outliers"].append({
                "column": column,
                "outlier_count": int(len(outliers)),
                "percentage": round(
                    (len(outliers) / len(df)) * 100,
                    2
                )
            })

    # ------------------------------------------------
    # 3. CATEGORICAL PATTERN DETECTION
    # ------------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    for column in categorical_columns:

        value_counts = df[column].value_counts(
            normalize=True
        ) * 100

        if len(value_counts) > 0:

            most_common_category = value_counts.index[0]
            percentage = value_counts.iloc[0]

            patterns["categorical_patterns"].append({
                "column": column,
                "most_common_value": str(
                    most_common_category
                ),
                "percentage": round(
                    float(percentage), 2
                )
            })

    # ------------------------------------------------
    # 4. SUMMARY
    # ------------------------------------------------

    summary = {
        "total_correlations": len(
            patterns["correlations"]
        ),
        "total_outlier_columns": len(
            patterns["outliers"]
        ),
        "total_categorical_patterns": len(
            patterns["categorical_patterns"]
        )
    }

    return {
        "patterns": patterns,
        "summary": summary
    }

