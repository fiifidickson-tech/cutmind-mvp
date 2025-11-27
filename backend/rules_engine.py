"""
rules_engine.py

CUTMIND MVP – Rules Engine

Purpose:
- Validate and normalize rule objects produced by the interpretation layer
  (interpretation.py) or received from the /interpret endpoint.
- Enforce the MVP rule format and allowed operations.
- Provide a clean list of rules for the geometry engine (geometry_engine.py).

MVP Scope:
- Only supports a fixed list of operations (see ALLOWED_OPERATIONS below).
- Only accepts numeric values in centimeters (`value_cm`).
- Does not handle conflict resolution; rules are applied sequentially.

This module is called by server.py in:

    validated_rules = validate_rules([rule.dict() for rule in request.rules])

If validation fails, this module raises an exception, which server.py converts
into a unified JSON error:

    {
        "error": "Invalid rule format",
        "details": {}
    }
"""

from __future__ import annotations

from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Allowed Operations (MVP)
# ---------------------------------------------------------------------------

# These operations must stay in sync with:
# - mvp_spec.md
# - api_contract.md
# - config/prompt_mapping.json
ALLOWED_OPERATIONS = {
    # Body length / hem
    "crop_hem",
    "extend_hem",
    "adjust_body_length",
    # Body ease
    "add_ease_body",
    "remove_ease_body",
    # Sleeves
    "widen_sleeve",
    "narrow_sleeve",
    "shorten_sleeve",
    "extend_sleeve",
    "add_ease_sleeve",
    # Neckline
    "raise_neckline",
    "lower_neckline",
}


# ---------------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------------


def _validate_operation(name: Any) -> str:
    """
    Validate that the operation name is a supported MVP operation.

    Parameters
    ----------
    name : Any
        The raw operation value from a rule dict.

    Returns
    -------
    str
        The normalized operation string.

    Raises
    ------
    ValueError
        If the operation is missing, not a string, or not allowed.
    """
    if not isinstance(name, str):
        raise ValueError("operation must be a string")

    op = name.strip()
    if not op:
        raise ValueError("operation cannot be empty")

    if op not in ALLOWED_OPERATIONS:
        raise ValueError(f"unsupported operation: {op}")

    return op


def _validate_value_cm(value: Any) -> float:
    """
    Validate that value_cm exists and is numeric.

    Parameters
    ----------
    value : Any
        The raw value_cm field.

    Returns
    -------
    float
        The numeric value in centimeters.

    Raises
    ------
    ValueError
        If value is missing or not numeric.
    """
    if value is None:
        raise ValueError("value_cm is required")

    try:
        num = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("value_cm must be numeric") from exc

    return num


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def validate_rules(rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Validate and normalize a list of rule dictionaries.

    Expected input (from interpretation layer or API):

        [
            { "operation": "crop_hem", "value_cm": 5 },
            { "operation": "widen_sleeve", "value_cm": 3 }
        ]

    This function ensures that:
    - rules is a non-empty list
    - each rule has:
        - operation: str and in ALLOWED_OPERATIONS
        - value_cm: numeric (float)
    - returns a new list of clean rule dicts.

    Parameters
    ----------
    rules : list[dict]
        Raw rules from the interpretation layer or request body.

    Returns
    -------
    list[dict]
        Validated and normalized rules.

    Raises
    ------
    ValueError
        If the rules list or any rule is invalid.

    Notes
    -----
    - server.py is responsible for catching exceptions and converting them into
      the unified error format.
    - This function does not decide how to resolve conflicting rules; it only
      validates format and allowed operations.
    """
    if not isinstance(rules, list):
        raise ValueError("rules must be a list")

    if len(rules) == 0:
        raise ValueError("rules list cannot be empty")

    normalized_rules: List[Dict[str, Any]] = []

    for idx, raw_rule in enumerate(rules):
        if not isinstance(raw_rule, dict):
            raise ValueError(f"rule at index {idx} must be a dict")

        if "operation" not in raw_rule:
            raise ValueError(f"rule at index {idx} missing 'operation' field")

        if "value_cm" not in raw_rule:
            raise ValueError(f"rule at index {idx} missing 'value_cm' field")

        op = _validate_operation(raw_rule.get("operation"))
        val = _validate_value_cm(raw_rule.get("value_cm"))

        normalized_rules.append(
            {
                "operation": op,
                "value_cm": val,
            }
        )

    return normalized_rules
