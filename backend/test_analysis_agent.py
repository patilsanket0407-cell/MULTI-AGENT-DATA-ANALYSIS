from agents.analysis_agent import analysis_agent


result = analysis_agent("datasets/employee.csv")


print("\n========== NUMERICAL ANALYSIS ==========")

for column, values in result["numerical_analysis"].items():

    print(f"\n{column}")
    print("Mean:", values["mean"])
    print("Median:", values["median"])
    print("Minimum:", values["minimum"])
    print("Maximum:", values["maximum"])
    print("Standard Deviation:", values["standard_deviation"])


print("\n========== CATEGORICAL ANALYSIS ==========")

for column, values in result["categorical_analysis"].items():

    print(f"\n{column}")
    print(values)


print("\n========== CORRELATION ==========")

for column, values in result["correlation"].items():

    print(column, values)
    