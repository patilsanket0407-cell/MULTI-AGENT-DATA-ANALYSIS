import pandas as pd


def preprocessing_agent(file_path):
    """
    Preprocess the dataset for further analysis.
    """

    # Load dataset
    df = pd.read_csv(file_path)

    # Store original information
    original_rows = len(df)
    original_columns = len(df.columns)

    # 1. Remove duplicate rows
    duplicates_removed = df.duplicated().sum()
    df = df.drop_duplicates()

    # 2. Handle missing values
    missing_before = df.isnull().sum().sum()

    for column in df.columns:

        if df[column].dtype == "object":
            # Fill categorical missing values with mode
            if df[column].isnull().sum() > 0:
                df[column] = df[column].fillna(df[column].mode()[0])

        else:
            # Fill numerical missing values with median
            if df[column].isnull().sum() > 0:
                df[column] = df[column].fillna(df[column].median())

    missing_after = df.isnull().sum().sum()

    # Return processed dataset and information
    return {
        "data": df,
        "preprocessing_info": {
            "original_rows": original_rows,
            "original_columns": original_columns,
            "duplicates_removed": int(duplicates_removed),
            "missing_values_before": int(missing_before),
            "missing_values_after": int(missing_after),
            "final_rows": len(df),
            "final_columns": len(df.columns)
        }
    }