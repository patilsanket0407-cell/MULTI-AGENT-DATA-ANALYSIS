from agents.pattern_agent import pattern_agent


result = pattern_agent("datasets/employee.csv")


print("\n========== PATTERN DETECTION ==========")


print("\n--- SUMMARY ---")

summary = result["summary"]

print(
    "Total Strong Correlations:",
    summary["total_correlations"]
)

print(
    "Columns With Outliers:",
    summary["total_outlier_columns"]
)

print(
    "Categorical Patterns:",
    summary["total_categorical_patterns"]
)


print("\n--- CORRELATIONS ---")

for item in result["patterns"]["correlations"]:

    print(
        item["feature_1"],
        "<->",
        item["feature_2"],
        ":",
        item["correlation"]
    )


print("\n--- OUTLIERS ---")

for item in result["patterns"]["outliers"]:

    print(
        item["column"],
        "→",
        item["outlier_count"],
        "outliers (",
        item["percentage"],
        "%)"
    )


print("\n--- CATEGORICAL PATTERNS ---")

for item in result["patterns"]["categorical_patterns"]:

    print(
        item["column"],
        "→",
        item["most_common_value"],
        "(",
        item["percentage"],
        "%)"
    )