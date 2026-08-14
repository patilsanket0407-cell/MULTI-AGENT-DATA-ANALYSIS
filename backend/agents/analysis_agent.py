import pandas as pd


def analysis_agent(file_path):

    # Load dataset
    df = pd.read_csv(file_path)

    # Separate numerical and categorical columns
    numerical_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = df.select_dtypes(exclude="number").columns.tolist()

    # Numerical analysis
    numerical_analysis = {}

    for column in numerical_columns:

        numerical_analysis[column] = {
            "mean": round(df[column].mean(), 2),
            "median": round(df[column].median(), 2),
            "minimum": df[column].min(),
            "maximum": df[column].max(),
            "standard_deviation": round(df[column].std(), 2)
        }

    # Categorical analysis
    categorical_analysis = {}

    for column in categorical_columns:

        categorical_analysis[column] = df[column].value_counts().to_dict()

    # Correlation analysis
    correlation = {}

    if len(numerical_columns) > 1:
        correlation = df[numerical_columns].corr().round(2).to_dict()

    # Final analysis result
    result = {
        "numerical_analysis": numerical_analysis,
        "categorical_analysis": categorical_analysis,
        "correlation": correlation
    }

    return result

    