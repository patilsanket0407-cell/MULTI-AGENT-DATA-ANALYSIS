import pandas as pd
from pathlib import Path


def load_dataset(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)

    elif file_path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    return df


def validate_dataset(df):
    if df.empty:
        raise ValueError("Dataset is empty.")

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
    }


def dataset_agent(file_path):
    df = load_dataset(file_path)

    dataset_info = validate_dataset(df)

    return {
        "dataframe": df,
        "dataset_info": dataset_info
    }

