"""
interpretation.py

CUTMIND MVP – Interpretation Layer

Purpose:
- Convert natural-language garment modification prompts into structured rule JSON.
- Use config/prompt_mapping.json to constrain and guide interpretation.

MVP Scope:
- Output only rule dictionaries of the form:
    { "operation": "<name>", "value_cm": <float> }
- Operation names must match:
    - config/prompt_mapping.json → "operations" keys
    - rules_engine.ALLOWED_OPERATIONS
- If a prompt cannot be mapped cleanly to one or more valid operations with
  numeric values, this module must raise InterpretationError so the router can
  return an "unsupported_instruction" or "invalid_rule_format" error.

Implementation Status:
- This file currently provides a heuristic, non-LLM implementation so:
    - The API shape is stable.
    - Frontend and backend can be wired end-to-end.
- When LLM integration is added, this module should be updated to:
    - Call the model.
    - Use the mapping to constrain valid outputs.
    - Return the same rule format.

Expected Function Signature:
- interpret_prompt(prompt: str) -> list[dict]
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class InterpretationError(Exception):
    """
    Raised when a prompt cannot be mapped to valid MVP rule JSON.

    Typical cases:
    - No supported operations detected.
    - Missing numeric values for required operations.
    - Mapping configuration is missing or unusable.
    """


# ---------------------------------------------------------------------------
# Configuration Loading
# ---------------------------------------------------------------------------


def _get_config_path() -> Path:
    """
    Return the path to config/prompt_mapping.json relative to this file.

    Expected structure:

        /backend
            interpretation.py
        /config
            prompt_mapping.json
    """
    backend_dir = Path(__file__).resolve().parent
    project_root = backend_dir.parent
    return project_root / "config" / "prompt_mapping.json"


def load_prompt_mapping() -> Dict[str, Any]:
    """
    Load prompt mapping configuration from /config/prompt_mapping.json.

    The file is expected to define:
    - operations
    - intensity_keywords
    - examples

    If the file does not exist or is invalid, returns an empty mapping so that
    the rest of the system can still run. However, interpret_prompt will raise
    InterpretationError if it cannot use the mapping to produce valid rules.
    """
    path = _get_config_path()
    if not path.exists():
        return {}

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Utility helpers using mapping
# ---------------------------------------------------------------------------


def _extract_numeric_cm(text: str) -> Optional[float]:
    """
    Extract the first numeric value followed by 'cm' in the text, if any.

    Example:
        "shorten the shirt by 3 cm" -> 3.0
    """
    match = re.search(r"(\d+(?:\.\d+)?)\s*cm", text)
    if not match:
        return None
    return float(match.group(1))


def _detect_intensity(text: str, intensity_map: Dict[str, Any]) -> Optional[float]:
    """
    Detect an intensity keyword (e.g., 'a bit') and return its numeric value,
    if any.

    Note:
    - This is allowed because it still results in a numeric value_cm.
    - Style/fit interpretation such as "boxy", "oversized", etc. is out of MVP
      scope and must not be inferred here.
    """
    for phrase, value in intensity_map.items():
        if phrase in text:
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    return None


# ---------------------------------------------------------------------------
# Interpretation Logic (Heuristic Placeholder)
# ---------------------------------------------------------------------------


def interpret_prompt(prompt: str, mapping: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Convert a natural-language prompt into a list of rule dictionaries.

    Expected output format (per MVP spec and api_contract.md):

        [
            { "operation": "crop_hem", "value_cm": 5 },
            { "operation": "widen_sleeve", "value_cm": 3 }
        ]

    Parameters
    ----------
    prompt : str
        Natural-language instructions, e.g.:
        "crop the hem by 5 cm and widen the sleeves"
    mapping : dict, optional
        Mapping loaded from config/prompt_mapping.json. If not provided, this
        function will load it automatically.

    Returns
    -------
    list[dict]
        A list of rule dictionaries matching the API contract.

    Error Behavior
    --------------
    - If no supported operations are detected, raise InterpretationError.
    - If operations are detected but no numeric value can be determined
      (explicit cm or intensity), raise InterpretationError.
    - The router is responsible for translating InterpretationError into the
      appropriate API error code ("unsupported_instruction" or
      "invalid_rule_format").
    """
    if mapping is None:
        mapping = load_prompt_mapping()

    if not mapping:
        raise InterpretationError("No prompt mapping configuration available.")

    operations_cfg = mapping.get("operations", {})
    if not operations_cfg:
        raise InterpretationError("No operations defined in prompt mapping configuration.")

    intensity_map = mapping.get("intensity_keywords", {}) or {}

    lower = prompt.lower()
    rules: List[Dict[str, Any]] = []
    seen_operations: set[str] = set()

    # ------------------------------------------------------------------------
    # 1. Determine numeric value from explicit cm or intensity.
    # ------------------------------------------------------------------------
    explicit_value = _extract_numeric_cm(lower)
    intensity_value = _detect_intensity(lower, intensity_map)

    # ------------------------------------------------------------------------
    # 2. Operation synonyms + numeric handling
    # ------------------------------------------------------------------------
    for op_name, op_cfg in operations_cfg.items():
        synonyms = op_cfg.get("synonyms", [])
        if not isinstance(synonyms, list):
            continue

        # If any synonym phrase appears in the prompt, consider it a match.
        matched = any(phrase.lower() in lower for phrase in synonyms)
        if not matched:
            continue

        if op_name in seen_operations:
            # Do not add duplicate operations.
            continue

        # Determine value_cm priority:
        # 1. Explicit "X cm" in text
        # 2. Intensity keyword (e.g., "a bit")
        if explicit_value is not None:
            value_cm = explicit_value
        elif intensity_value is not None:
            value_cm = intensity_value
        else:
            # For MVP, we do not invent arbitrary values without numeric basis.
            raise InterpretationError("Missing numeric value for operation.")

        rules.append(
            {
                "operation": op_name,
                "value_cm": value_cm,
            }
        )
        seen_operations.add(op_name)

    # ------------------------------------------------------------------------
    # 3. Ensure at least one valid rule exists
    # ------------------------------------------------------------------------
    if not rules:
        # No operations detected from the prompt → unsupported instruction.
        raise InterpretationError("No supported operations could be inferred from prompt.")

    return rules
