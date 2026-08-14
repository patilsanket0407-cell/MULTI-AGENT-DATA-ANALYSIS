from agents.visualization_agent import visualization_agent


result = visualization_agent("datasets/employee.csv")


print("\n===== VISUALIZATION RESULTS =====")

summary = result["visualization_summary"]

print("Total Charts:", summary["total_charts"])

print("\nGenerated Charts:")

for chart in summary["charts"]:
    print(chart)