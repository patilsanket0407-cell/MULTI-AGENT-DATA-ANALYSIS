from agents.dataset_agent import dataset_agent


result = dataset_agent("datasets/employee.csv")

print("\n===== DATASET INFORMATION =====")

info = result["dataset_info"]

print("Rows:", info["rows"])
print("Columns:", info["columns"])

print("\nColumn Names:")
print(info["column_names"])

print("\nData Types:")
print(info["data_types"])

print("\nMissing Values:")
print(info["missing_values"])

