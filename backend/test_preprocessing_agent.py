from agents.preprocessing_agent import preprocessing_agent


result = preprocessing_agent("datasets/employee.csv")


print("\n===== PREPROCESSING RESULTS =====")

info = result["preprocessing_info"]

print("Original Rows:", info["original_rows"])
print("Original Columns:", info["original_columns"])

print("Duplicates Removed:", info["duplicates_removed"])

print("Missing Values Before:", info["missing_values_before"])
print("Missing Values After:", info["missing_values_after"])

print("Final Rows:", info["final_rows"])
print("Final Columns:", info["final_columns"])

print("\n===== CLEAN DATASET =====")
print(result["data"].head())
