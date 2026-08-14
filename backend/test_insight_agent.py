from agents.insight_agent import insight_agent


result = insight_agent("datasets/employee.csv")


print("\n===== INSIGHT AGENT RESULTS =====")

summary = result["insight_summary"]

print("Total Insights:", summary["total_insights"])

print("\nGenerated Insights:")

for insight in summary["insights"]:
    print("•", insight)