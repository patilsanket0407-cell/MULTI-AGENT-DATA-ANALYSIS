from backend.gemini_service import generate_insights


def insight_agent(state):
    """Generate verified and AI-powered insights from previous agents."""

    dataset_results = state.get("dataset", {})
    preprocessing_results = state.get("preprocessing", {})
    analysis_results = state.get("analysis", {})
    pattern_results = state.get("patterns", {})

    # Send ONLY verified summaries to Gemini.
    # Do not send the complete Pandas DataFrames.
    verified_results = {
        "dataset": dataset_results.get("dataset_info", {}),
        "preprocessing": preprocessing_results.get("preprocessing_info", {}),
        "analysis": analysis_results,
        "patterns": pattern_results,
    }

    try:
        ai_insights = generate_insights(verified_results)

    except Exception as e:
        print("========================================")
        print("GEMINI ERROR:")
        print(repr(e))
        print("========================================")

        ai_insights = {
            "summary": (
                "AI insight generation was unavailable. "
                "The previous analysis agents completed successfully."
            ),
            "key_insights": [],
            "recommendations": [],
            "risk_factors": [],
            "error": str(e)
        }

    state["insights"] = {
        "ai_insights": ai_insights
    }

    return state

