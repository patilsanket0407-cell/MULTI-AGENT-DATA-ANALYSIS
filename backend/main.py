from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pathlib import Path
import shutil
import math

import pandas as pd
import numpy as np

from backend.graph.workflow import analysis_graph


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Multi-Agent Data Analysis System",
    description="AI-powered multi-agent data analysis system using LangGraph",
    version="1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DIRECTORIES
# ============================================================

UPLOAD_DIR = Path("backend/uploads")
CHARTS_DIR = Path("backend/charts")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CHARTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SERVE CHARTS
# ============================================================

app.mount(
    "/charts",
    StaticFiles(directory=str(CHARTS_DIR)),
    name="charts"
)


# ============================================================
# CONVERT RESULTS TO JSON-SAFE DATA
# ============================================================

def make_json_safe(obj):

    # Pandas DataFrame
    if isinstance(obj, pd.DataFrame):

        return make_json_safe(
            obj.to_dict(orient="records")
        )

    # Pandas Series
    if isinstance(obj, pd.Series):

        return make_json_safe(
            obj.to_dict()
        )

    # NumPy integer
    if isinstance(obj, np.integer):

        return int(obj)

    # NumPy floating point
    if isinstance(obj, np.floating):

        value = float(obj)

        if not math.isfinite(value):
            return None

        return value

    # NumPy boolean
    if isinstance(obj, np.bool_):

        return bool(obj)

    # NumPy array
    if isinstance(obj, np.ndarray):

        return make_json_safe(
            obj.tolist()
        )

    # Python float
    if isinstance(obj, float):

        if not math.isfinite(obj):
            return None

        return obj

    # Dictionary
    if isinstance(obj, dict):

        return {
            str(key): make_json_safe(value)
            for key, value in obj.items()
        }

    # List
    if isinstance(obj, list):

        return [
            make_json_safe(item)
            for item in obj
        ]

    # Tuple
    if isinstance(obj, tuple):

        return [
            make_json_safe(item)
            for item in obj
        ]

    # Set
    if isinstance(obj, set):

        return [
            make_json_safe(item)
            for item in obj
        ]

    # Path
    if isinstance(obj, Path):

        return str(obj)

    # Normal Python value
    return obj


# ============================================================
# CLEAN DATASET RESULT
# ============================================================

def clean_dataset_result(dataset_result):

    if not isinstance(dataset_result, dict):

        return make_json_safe(dataset_result)

    cleaned = {}

    # Dataset information
    if "dataset_info" in dataset_result:

        cleaned["dataset_info"] = make_json_safe(
            dataset_result["dataset_info"]
        )

    # DataFrame preview
    if "dataframe" in dataset_result:

        dataframe = dataset_result["dataframe"]

        if isinstance(dataframe, pd.DataFrame):

            cleaned["preview"] = make_json_safe(
                dataframe.head(5)
            )

        elif isinstance(dataframe, list):

            cleaned["preview"] = make_json_safe(
                dataframe[:5]
            )

    return cleaned


# ============================================================
# CONVERT CHART PATHS
# ============================================================

def convert_chart_paths(obj):

    if isinstance(obj, dict):

        return {
            key: convert_chart_paths(value)
            for key, value in obj.items()
        }

    if isinstance(obj, list):

        return [
            convert_chart_paths(item)
            for item in obj
        ]

    if isinstance(obj, tuple):

        return [
            convert_chart_paths(item)
            for item in obj
        ]

    if isinstance(obj, str):

        # Windows path
        if "backend\\charts\\" in obj:

            filename = Path(obj).name

            return f"/charts/{filename}"

        # Linux / normal path
        if "backend/charts/" in obj:

            filename = Path(obj).name

            return f"/charts/{filename}"

    return obj


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Multi-Agent Data Analysis Backend is running",
        "status": "healthy"
    }


# ============================================================
# ANALYZE DATASET
# ============================================================

@app.post("/analyze")
async def analyze_dataset(
    file: UploadFile = File(...)
):

    try:

        # ----------------------------------------------------
        # VALIDATE FILE
        # ----------------------------------------------------

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="No file selected"
            )

        if not file.filename.lower().endswith(".csv"):

            raise HTTPException(
                status_code=400,
                detail="Only CSV files are currently supported"
            )


        # ----------------------------------------------------
        # SAVE FILE
        # ----------------------------------------------------

        file_path = UPLOAD_DIR / file.filename

        with file_path.open("wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # ----------------------------------------------------
        # RUN LANGGRAPH
        # ----------------------------------------------------

        result = analysis_graph.invoke(
            {
                "file_path": str(file_path)
            }
        )


        # ----------------------------------------------------
        # MAKE JSON SAFE
        # ----------------------------------------------------

        safe_result = make_json_safe(result)


        # ----------------------------------------------------
        # CLEAN DATASET RESULT
        # ----------------------------------------------------

        if "dataset_result" in safe_result:

            safe_result["dataset_result"] = (
                clean_dataset_result(
                    safe_result["dataset_result"]
                )
            )


        # ----------------------------------------------------
        # CONVERT CHART PATHS
        # ----------------------------------------------------

        safe_result = convert_chart_paths(
            safe_result
        )


        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return {
            "success": True,
            "filename": file.filename,
            "results": safe_result
        }


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )