from backend.graph.workflow import analysis_graph


FILE_PATH = "backend/uploads/WA_Fn-UseC_-HR-Employee-Attrition.csv"


print("=" * 60)
print("MULTI-AGENT DATA ANALYSIS WORKFLOW")
print("=" * 60)

print("\n[1] Starting LangGraph workflow...\n")

result = analysis_graph.invoke({
    "file_path": FILE_PATH
})

print("[2] WORKFLOW EXECUTED SUCCESSFULLY\n")


# --------------------------------------------------
# DATASET
# --------------------------------------------------

print("=" * 60)
print("1. DATASET AGENT")
print("=" * 60)

print(result.get("dataset_result"))


# --------------------------------------------------
# PREPROCESSING
# --------------------------------------------------

print("\n" + "=" * 60)
print("2. PREPROCESSING AGENT")
print("=" * 60)

print(result.get("preprocessing_result"))


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 60)
print("3. ANALYSIS AGENT")
print("=" * 60)

print(result.get("analysis_result"))


# --------------------------------------------------
# PATTERN
# --------------------------------------------------

print("\n" + "=" * 60)
print("4. PATTERN AGENT")
print("=" * 60)

print(result.get("pattern_result"))


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("5. VISUALIZATION AGENT")
print("=" * 60)

print(result.get("visualization_result"))


# --------------------------------------------------
# INSIGHT
# --------------------------------------------------

print("\n" + "=" * 60)
print("6. INSIGHT AGENT")
print("=" * 60)

print(result.get("insight_result"))


# --------------------------------------------------
# FINAL STATE
# --------------------------------------------------

print("\n" + "=" * 60)
print("FINAL STATE KEYS")
print("=" * 60)

for key in result.keys():
    print("✓", key)

print("\n" + "=" * 60)
print("WORKFLOW TEST COMPLETE")
print("=" * 60)
