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

Error Contract:
- All errors must follow the unified format:

    {
        "error": "some_error_code",
        "details": {}
    }

- Typical error codes:
    - unsupported_instruction
    - invalid_rule_format
    - invalid_pattern_id
    - geometry_application_failed
    - internal_error
"""

from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError

# These modules are expected to be implemented separately.
# For now, they can be stubbed or left unimplemented.
try:
    from interpretation import interpret_prompt, InterpretationError  # type: ignore
    from rules_engine import validate_rules, RuleValidationError      # type: ignore
    from geometry_engine import apply_geometry, GeometryEngineError   # type: ignore
    from pattern_loader import load_pattern_svg, PatternNotFoundError # type: ignore
except ImportError:
    # During early scaffold phase, these may not exist yet.
    interpret_prompt = None
    validate_rules = None
    apply_geometry = None
    load_pattern_svg = None

    class InterpretationError(Exception):  # type: ignore
        pass

    class RuleValidationError(Exception):  # type: ignore
        pass

    class GeometryEngineError(Exception):  # type: ignore
        pass

    class PatternNotFoundError(Exception):  # type: ignore
        pass


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


def error_response(code: str, details: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Return a unified error response matching the API contract.

    Parameters
    ----------
    code : str
        Machine-readable error code, e.g. "invalid_rule_format".
    details : dict | None
        Optional extra context (always an object in the final JSON).
    """
    return {
        "error": code,
        "details": details or {},
    }


def validate_pattern_id(pattern_id: str) -> None:
    """
    Ensure pattern_id is one of the supported MVP blocks.
    Raises HTTPException with error code 'invalid_pattern_id' on invalid ID.
    """
    valid_ids = {"tshirt", "long_sleeve", "crop_top"}
    if pattern_id not in valid_ids:
        raise HTTPException(
            status_code=400,
            detail=error_response("invalid_pattern_id", {"pattern_id": pattern_id}),
        )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.post(
    "/interpret",
    response_model=InterpretResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def interpret(request: InterpretRequest):
    """
    Convert a natural-language prompt into structured rules.

    Behavior:
    - Uses interpretation.py to map prompt → rule JSON.
    - Validates rule structure via Pydantic before returning.

    Error mapping:
    - Missing/invalid prompt → invalid_rule_format (400)
    - InterpretationError → unsupported_instruction (400)
    - Pydantic validation error on rules → invalid_rule_format (400)
    - Other unexpected errors → internal_error (500)
    """
    # Scaffold: if interpretation is not implemented yet, return dummy rules.
    if interpret_prompt is None:
        dummy_rules = [
            Rule(operation="crop_hem", value_cm=5.0),
            Rule(operation="widen_sleeve", value_cm=3.0),
        ]
        return InterpretResponse(rules=dummy_rules)

    # Normal behavior
    try:
        raw_rules = interpret_prompt(request.prompt)
    except InterpretationError:
        # Prompt couldn't be mapped into valid MVP rules.
        raise HTTPException(
            status_code=400,
            detail=error_response("unsupported_instruction"),
        )
    except Exception:
        # Catch-all for unexpected interpretation failures.
        raise HTTPException(
            status_code=500,
            detail=error_response("internal_error"),
        )

    # Validate the shape of returned rules using Pydantic
    try:
        rules = [Rule(**rule_dict) for rule_dict in raw_rules]
    except ValidationError:
        raise HTTPException(
            status_code=400,
            detail=error_response("invalid_rule_format"),
        )

    return InterpretResponse(rules=rules)


@app.post(
    "/apply-rules",
    response_model=ApplyRulesResponse,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def apply_rules(request: ApplyRulesRequest):
    """
    Apply validated rules to a base pattern and return the modified SVG.

    Behavior:
    - Validate pattern_id.
    - Use rules_engine.py to validate/normalize rules.
    - Use pattern_loader.py to load base SVG.
    - Use geometry_engine.py to apply transformations.

    Error mapping:
    - Invalid pattern_id → invalid_pattern_id (400 or 404 if not found)
    - RuleValidationError → invalid_rule_format (400)
    - GeometryEngineError → geometry_application_failed (400)
    - Other unexpected errors → internal_error (500)
    """
    validate_pattern_id(request.pattern_id)

    # Scaffold: if core modules are not implemented, return placeholder SVG.
    if any(module is None for module in (validate_rules, load_pattern_svg, apply_geometry)):
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

    except RuleValidationError:
        raise HTTPException(
            status_code=400,
            detail=error_response("invalid_rule_format"),
        )
    except PatternNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=error_response("invalid_pattern_id"),
        )
    except GeometryEngineError:
        raise HTTPException(
            status_code=400,
            detail=error_response("geometry_application_failed"),
        )
    except HTTPException:
        # Re-raise explicit HTTPExceptions as-is.
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=error_response("internal_error"),
        )


@app.get(
    "/patterns/{pattern_id}",
    responses={
        200: {"content": {"image/svg+xml": {}}},
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def get_pattern(pattern_id: str):
    """
    Return the raw base SVG pattern for the given pattern_id.

    Valid IDs:
    - tshirt
    - long_sleeve
    - crop_top

    Error mapping:
    - Invalid pattern_id → invalid_pattern_id (400/404)
    - Other unexpected errors → internal_error (500)
    """
    validate_pattern_id(pattern_id)

    # Scaffold: if loader is not implemented, return placeholder SVG.
    if load_pattern_svg is None:
        return "<svg><!-- placeholder base pattern --></svg>"

    try:
        svg = load_pattern_svg(pattern_id)
        if not svg:
            # Treat empty/None SVG as not found.
            raise PatternNotFoundError()
        return svg
    except PatternNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=error_response("invalid_pattern_id"),
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=error_response("internal_error"),
        )


# Optional health check for sanity
@app.get("/health")
def health_check():
    """
    Simple health endpoint to verify the server is running.
    """
    return {"status": "ok"}
