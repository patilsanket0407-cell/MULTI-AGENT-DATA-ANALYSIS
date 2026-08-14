from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from backend.agents.dataset_agent import dataset_agent
from backend.agents.preprocessing_agent import preprocessing_agent
from backend.agents.analysis_agent import analysis_agent
from backend.agents.pattern_agent import pattern_agent
from backend.agents.visualization_agent import visualization_agent
from backend.agents.insight_agent import insight_agent


class AnalysisState(TypedDict, total=False):
    file_path: str

    dataset_result: Any
    preprocessing_result: Any
    analysis_result: Any
    pattern_result: Any
    visualization_result: Any
    insight_result: Any


# --------------------------------------------------
# DATASET AGENT
# --------------------------------------------------

def run_dataset_agent(state: AnalysisState):
    result = dataset_agent(state["file_path"])

    return {
        "dataset_result": result
    }


# --------------------------------------------------
# PREPROCESSING AGENT
# --------------------------------------------------

def run_preprocessing_agent(state: AnalysisState):
    result = preprocessing_agent(state["file_path"])

    return {
        "preprocessing_result": result
    }


# --------------------------------------------------
# ANALYSIS AGENT
# --------------------------------------------------

def run_analysis_agent(state: AnalysisState):
    result = analysis_agent(state["file_path"])

    return {
        "analysis_result": result
    }


# --------------------------------------------------
# PATTERN AGENT
# --------------------------------------------------

def run_pattern_agent(state: AnalysisState):
    result = pattern_agent(state["file_path"])

    return {
        "pattern_result": result
    }


# --------------------------------------------------
# VISUALIZATION AGENT
# --------------------------------------------------

def run_visualization_agent(state: AnalysisState):
    result = visualization_agent(state["file_path"])

    return {
        "visualization_result": result
    }


# --------------------------------------------------
# INSIGHT AGENT
# --------------------------------------------------

def run_insight_agent(state: AnalysisState):
    result = insight_agent(state["file_path"])

    return {
        "insight_result": result
    }


# --------------------------------------------------
# BUILD LANGGRAPH
# --------------------------------------------------

graph = StateGraph(AnalysisState)

graph.add_node(
    "dataset_agent",
    run_dataset_agent
)

graph.add_node(
    "preprocessing_agent",
    run_preprocessing_agent
)

graph.add_node(
    "analysis_agent",
    run_analysis_agent
)

graph.add_node(
    "pattern_agent",
    run_pattern_agent
)

graph.add_node(
    "visualization_agent",
    run_visualization_agent
)

graph.add_node(
    "insight_agent",
    run_insight_agent
)


# --------------------------------------------------
# CONNECT AGENTS
# --------------------------------------------------

graph.add_edge(
    START,
    "dataset_agent"
)

graph.add_edge(
    "dataset_agent",
    "preprocessing_agent"
)

graph.add_edge(
    "preprocessing_agent",
    "analysis_agent"
)

graph.add_edge(
    "analysis_agent",
    "pattern_agent"
)

graph.add_edge(
    "pattern_agent",
    "visualization_agent"
)

graph.add_edge(
    "visualization_agent",
    "insight_agent"
)

graph.add_edge(
    "insight_agent",
    END
)


# --------------------------------------------------
# COMPILE LANGGRAPH
# --------------------------------------------------

analysis_graph = graph.compile()