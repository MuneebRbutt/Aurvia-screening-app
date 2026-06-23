"""
Aurvia Screening App - FastAPI Backend
--------------------------------------
This file is the heart of the application. It does two things:
  1. Serves the React frontend (the HTML/UI) at the root URL "/"
  2. Provides a POST API endpoint at "/api/threshold" that:
       - Validates incoming JSON data
       - Computes the mean (average) of the values
       - Returns "STABLE" or "CRITICAL" based on variance
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from typing import List
import statistics
import os

# ── App Setup ──────────────────────────────────────────────────────────────────
app = FastAPI(title="Aurvia Threshold API")


# ── Pydantic Schema (Data Validation) ─────────────────────────────────────────
# Pydantic automatically checks that incoming JSON matches this structure.
# If it doesn't, FastAPI returns a 422 error automatically.
class ThresholdRequest(BaseModel):
    stream_values: List[float]   # Must be a list of numbers
    max_variance: float          # Must be a single number

    # Extra validation: reject empty lists BEFORE we even try to calculate
    @field_validator("stream_values")
    @classmethod
    def must_not_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("stream_values must not be empty")
        return v


# ── API Endpoint ───────────────────────────────────────────────────────────────
@app.post("/api/threshold")
async def check_threshold(payload: ThresholdRequest):
    """
    Accepts stream_values (list of floats) and max_variance (float).
    Returns the mean and a status of STABLE or CRITICAL.
    """
    values = payload.stream_values
    max_variance = payload.max_variance

    # Step 1: Calculate the mean (average)
    mean = statistics.mean(values)

    # Step 2: Check if ANY value deviates more than max_variance from the mean
    is_critical = any(abs(v - mean) > max_variance for v in values)

    # Step 3: Return the result
    return {
        "mean": round(mean, 4),
        "status": "CRITICAL" if is_critical else "STABLE",
        "max_variance": max_variance,
        "count": len(values),
    }


# ── Exception Handler: Catch Bad Input (strings, nulls, etc.) ─────────────────
# FastAPI/Pydantic throws a RequestValidationError when types are wrong.
# We catch it here and return a clean 400 instead of an ugly 500 crash.
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Bad Request",
            "detail": "stream_values must be a non-empty list of numbers, and max_variance must be a number.",
        },
    )


# ── Static File Mount (Serve the React UI) ────────────────────────────────────
# This mounts the /templates folder so that index.html is served at "/"
# The `html=True` flag makes it serve index.html automatically for "/"
app.mount("/", StaticFiles(directory="templates", html=True), name="static")
