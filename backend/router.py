Here’s the **fixed `router.py`** aligned with your current MVP spec, `interpretation.py`, `rules_engine.py`, `geometry_engine.py`, and `api_contract.md`.

You can paste this **directly** over the existing file.

```python
"""
router.py

Purpose:
- Define and register all HTTP routes for the CUTMIND backend.
- Integrate the interpretation, rules engine, geometry engine,
  and pattern loader into a single API surface.

Responsibilities:
- Define FastAPI route handlers for:
    - POST /interpret
    - POST /apply-rules
    - GET  /patterns/{id}
- Coordinate calls between:
    - interpretation.py
    - rules_engine.py
    - geometry_engine.py
    - pattern_loader.py
- Enforce the API contracts defined in api_contract.md and mvp_spec.md.

Non-responsibilities (handled elsewhere):
- App creation and startup → server.py
- Business logic implementation within the individual modules.

Implementation Status:
- Placeholder only. Route handlers are provided as commented examples.
"""

# Example FastAPI router structure (commented out, not active yet):

# from fastapi import APIRouter, HTTPException
# from typing import Any, Dict
#
# from .interpretation import interpret_prompt, InterpretationError
# from .rules_engine import validate_rules, RuleValidationError
# from .geometry_engine import apply_geometry, GeometryEngineError
# from .pattern_loader import load_pattern_svg, PatternNotFoundError
#
# router = APIRouter()
#
#
# @router.post("/interpret")
# async def interpret(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Placeholder route:
#     - Accepts a "prompt" in the request body.
#     - Returns structured rules as defined in api_contract.md.
#     - On error, returns unified error JSON with appropriate error code.
#     """
#     prompt = payload.get("prompt")
#     if not prompt:
#         # Unified error format – missing/invalid input
#         raise HTTPException(
#             status_code=400,
#             detail={"error": "invalid_rule_format", "details": {}},
#         )
#
#     try:
#         rules = interpret_prompt(prompt)
#     except InterpretationError:
#         # Interpretation failed → unsupported_instruction or invalid_rule_format.
#         # For MVP scaffold, we treat all interpretation failures as unsupported_instruction.
#         raise HTTPException(
#             status_code=400,
#             detail={"error": "unsupported_instruction", "details": {}},
#         )
#     except Exception:
#         # Catch-all safety net → internal_error
#         raise HTTPException(
#             status_code=500,
#             detail={"error": "internal_error", "details": {}},
#         )
#
#     return {"rules": rules}
#
#
# @router.post("/apply-rules")
# async def apply_rules(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Placeholder route:
#     - Accepts pattern_id and rules.
#     - Returns modified SVG only, as defined in api_contract.md.
#     - On error, uses the unified error format with the correct error codes.
#     """
#     pattern_id = payload.get("pattern_id")
#     rules = payload.get("rules", [])
#
#     if not pattern_id:
#         raise HTTPException(
#             status_code=400,
#             detail={"error": "invalid_pattern_id", "details": {}},
#         )
#
#     try:
#         validated_rules = validate_rules(rules)
#         base_svg = load_pattern_svg(pattern_id)
#         modified_svg = apply_geometry(base_svg, validated_rules)
#     except RuleValidationError:
#         raise HTTPException(
#             status_code=400,
#             detail={"error": "invalid_rule_format", "details": {}},
#         )
#     except PatternNotFoundError:
#         raise HTTPException(
#             status_code=404,
#             detail={"error": "invalid_pattern_id", "details": {}},
#         )
#     except GeometryEngineError:
#         raise HTTPException(
#             status_code=400,
#             detail={"error": "geometry_application_failed", "details": {}},
#         )
#     except Exception:
#         raise HTTPException(
#             status_code=500,
#             detail={"error": "internal_error", "details": {}},
#         )
#
#     return {
#         "modified_pattern_svg": modified_svg,
#     }
#
#
# @router.get("/patterns/{pattern_id}")
# async def get_pattern(pattern_id: str) -> str:
#     """
#     Placeholder route:
#     - Returns the base SVG for a given pattern_id.
#     - On error, returns unified error JSON with invalid_pattern_id.
#     """
#     try:
#         svg = load_pattern_svg(pattern_id)
#     except PatternNotFoundError:
#         raise HTTPException(
#             status_code=404,
#             detail={"error": "invalid_pattern_id", "details": {}},
#         )
#     except Exception:
#         raise HTTPException(
#             status_code=500,
#             detail={"error": "internal_error", "details": {}},
#         )
#
#     return svg
#
#
# def register_routes(app):
#     """
#     Helper to attach the router to a FastAPI app instance.
#     Intended to be called from server.py once the backend is implemented.
#     """
#     app.include_router(router)
```
