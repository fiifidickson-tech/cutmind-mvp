"""
server.py

CUTMIND MVP – Backend Entry Point

This file defines the FastAPI application and HTTP routes for the MVP.

MVP Scope:
- Three pattern families: tshirt, long_sleeve, crop_top
- Endpoints:
    - POST /interpret
    - POST /apply-rules
    - GET  /patterns/{pattern_id}

Implementation Status:
- Wiring and schemas are defined.
- Core logic (interpretation, rules, geometry, pattern loading) should be
  implemented in:
    - interpretation.py
    - rules_engine.py
    - geometry_engine.py
    - pattern_loader.py
"""

from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# These modules are expected to be implemented separately.
# For now, they can be stubbed or left unimplemented.
try:
    from interpretation import interpret_prompt  # type: ignore
    from rules_engine import validate_rules      # type: ignore
    from geometry_engine import apply_geometry   # type: ignore
    from pattern_loader import load_pattern_svg  # type: ignore
except ImportError:
    # During early scaffold phase, these may not exist yet.
    interpret_prompt = None
    validate_rules = None
    apply_geometry = None
    load_pattern_svg = None


app = FastAPI(
    title="CUTMIND MVP API",
    version="0.1.0",
    description="Natural-language pattern adjustment API for three base blocks."
)


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------


class Rule(BaseModel):
    operation: str = Field(..., description="Name of the operation, e.g., 'crop_hem'.")
    value_cm: float = Field(..., description="Numeric value in centimeters.")


class InterpretRequest(BaseModel):
    prompt: str = Field(..., description="Natural-language instructions for garment modifications.")


class InterpretResponse(BaseModel):
    rules: List[Rule]


class ApplyRulesRequest(BaseModel):
    pattern_id: str = Field(..., description="One of: 'tshirt', 'long_sleeve', 'crop_top'.")
    rules: List[Rule]


class ApplyRulesResponse(BaseModel):
    modified_pattern_svg: str = Field(..., description="Transformed SVG pattern string.")


class ErrorResponse(BaseModel):
    error: str
    details: Dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------


def error_response(message: str, details: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Return a unified error response matching the API contract.
    """
    return {
        "error": message,
        "details": details or {},
    }


def validate_pattern_id(pattern_id: str) -> None:
    """
    Ensure pattern_id is one of the supported MVP blocks.
    Raises HTTPException on invalid ID.
    """
    valid_ids = {"tshirt", "long_sleeve", "crop_top"}
    if pattern_id not in valid_ids:
        raise HTTPException(
            status_code=400,
            detail=error_response("Invalid pattern ID", {"pattern_id": pattern_id}),
        )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.post("/interpret", response_model=InterpretResponse, responses={400: {"model": ErrorResponse}})
def interpret(request: InterpretRequest):
    """
    Convert a natural-language prompt into structured rules.

    Expected behavior (once implemented):
    - Use interpretation.py / LLM to map prompt → rule JSON.
    - Validate rule structure before returning.
    """
    if interpret_prompt is None:
        # Placeholder behavior until interpretation.py is implemented.
        # This keeps the API shape stable for frontend experiments.
        dummy_rules = [
            Rule(operation="crop_hem", value_cm=5.0),
            Rule(operation="widen_sleeve", value_cm=3.0),
        ]
        return InterpretResponse(rules=dummy_rules)

    try:
        raw_rules = interpret_prompt(request.prompt)
        # raw_rules is expected to be a list of dicts with operation + value_cm.
        rules = [Rule(**rule_dict) for rule_dict in raw_rules]
        return InterpretResponse(rules=rules)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=400,
            detail=error_response("Invalid rule format", {"exception": str(exc)}),
        ) from exc


@app.post("/apply-rules", response_model=ApplyRulesResponse, responses={400: {"model": ErrorResponse}})
def apply_rules(request: ApplyRulesRequest):
    """
    Apply validated rules to a base pattern and return the modified SVG.

    Expected behavior (once implemented):
    - Validate pattern_id.
    - Use rules_engine.py to validate/normalize rules.
    - Use pattern_loader.py to load base SVG.
    - Use geometry_engine.py to apply transformations.
    """
    validate_pattern_id(request.pattern_id)

    if any(module is None for module in (validate_rules, load_pattern_svg, apply_geometry)):
        # Placeholder behavior until individual modules are implemented.
        dummy_svg = "<svg><!-- placeholder modified pattern --></svg>"
        return ApplyRulesResponse(modified_pattern_svg=dummy_svg)

    try:
        # Step 1: Validate rules
        validated_rules = validate_rules([rule.dict() for rule in request.rules])

        # Step 2: Load base SVG
        base_svg = load_pattern_svg(request.pattern_id)

        # Step 3: Apply geometry transformations
        modified_svg = apply_geometry(base_svg, validated_rules)

        return ApplyRulesResponse(modified_pattern_svg=modified_svg)
    except HTTPException:
        # Re-raise any explicit HTTPException as-is
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=400,
            detail=error_response("Invalid rule format", {"exception": str(exc)}),
        ) from exc


@app.get("/patterns/{pattern_id}", responses={200: {"content": {"image/svg+xml": {}}}, 400: {"model": ErrorResponse}})
def get_pattern(pattern_id: str):
    """
    Return the raw base SVG pattern for the given pattern_id.

    - tshirt
    - long_sleeve
    - crop_top
    """
    validate_pattern_id(pattern_id)

    if load_pattern_svg is None:
        # Placeholder SVG until pattern_loader is implemented.
        return "<svg><!-- placeholder base pattern --></svg>"

    try:
        svg = load_pattern_svg(pattern_id)
        return svg
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=400,
            detail=error_response("Invalid pattern ID", {"exception": str(exc)}),
        ) from exc


# Optional health check for sanity
@app.get("/health")
def health_check():
    """
    Simple health endpoint to verify the server is running.
    """
    return {"status": "ok"}
