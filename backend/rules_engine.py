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

This module is called by the routing layer / server, e.g.:

    validated_rules = validate_rules(rules)

If validation fails, this module raises RuleValidationError, which the router
must convert into the unified JSON error:

    {
        "error": "invalid_rule_format",
        "details": {}
    }

This file must stay in sync with:
- mvp_spec.md
- api_contract.md
- config/prompt_mapping.json
"""

from __future__ import annotations

from typing import Any, Dict, List


class RuleValidationError(Exception):
    """
    Raised when one or more rules fail validation.

    The router must catch this exception and return an API error with:
        "error": "invalid_rule_format"
    using the unified error format.
    """


# ---------------------------------------------------------------------------
# Allowed Operations (MVP)
# ---------------------------------------------------------------------------

# These operation names must match:
# - mvp_spec.md section "In-Scope Adjustments"
# - config/prompt_mapping.json → "operations" keys
ALLOWED_OPERATIONS = {
    # Body adjustments
    "crop_hem",
    "extend_hem",
    "adjust_body_length",
    "add_ease_body",
    "remove_ease_body",
    # Sleeve adjustments
    "widen_sleeve",
    "narrow_sleeve",
    "shorten_sleeve",
    "extend_sleeve",
    "add_ease_sleeve",
    # Neckline adjustments
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
    RuleValidationError
        If the operation is missing, not a string, or not allowed.
    """
    if not isinstance(name, str):
        raise RuleValidationError("operation must be a string")

    op = name.strip()
    if not op:
        raise RuleValidationError("operation cannot be empty")

    if op not in ALLOWED_OPERATIONS:
        raise RuleValidationError(f"unsupported operation: {op}")

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
    RuleValidationError
        If value is missing or not numeric.
    """
    if value is None:
        raise RuleValidationError("value_cm is required")

    try:
        num = float(value)
    except (TypeError, ValueError) as exc:
        raise RuleValidationError("value_cm must be numeric") from exc

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
    RuleValidationError
        If the rules list or any rule is invalid.

    Notes
    -----
    - The router or server is responsible for catching RuleValidationError and
      converting it into the unified error format with:
          "error": "invalid_rule_format".
    - This function does not decide how to resolve conflicting rules; it only
      validates format and allowed operations.
    """
    if not isinstance(rules, list):
        raise RuleValidationError("rules must be a list")

    if len(rules) == 0:
        raise RuleValidationError("rules list cannot be empty")

    normalized_rules: List[Dict[str, Any]] = []

    for idx, raw_rule in enumerate(rules):
        if not isinstance(raw_rule, dict):
            raise RuleValidationError(f"rule at index {idx} must be a dict")

        if "operation" not in raw_rule:
            raise RuleValidationError(f"rule at index {idx} missing 'operation' field")

        if "value_cm" not in raw_rule:
            raise RuleValidationError(f"rule at index {idx} missing 'value_cm' field")

        op = _validate_operation(raw_rule.get("operation"))
        val = _validate_value_cm(raw_rule.get("value_cm"))

        normalized_rules.append(
            {
                "operation": op,
                "value_cm": val,
            }
        )

    return normalized_rules
