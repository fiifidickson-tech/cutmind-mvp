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
    - garment_type
    - operations
    - intensity_keywords
    - fit_keywords
    - examples

    If the file does not exist or is invalid, returns an empty mapping so that
    the rest of the system can still run with basic fallback behavior.
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
    Detect an intensity keyword (e.g., 'a bit', 'oversized') and return
    its numeric value, if any.
    """
    for phrase, value in intensity_map.items():
        if phrase in text:
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    return None


def _apply_fit_keywords(
    text: str,
    fit_keywords: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Use fit_keywords to generate default operations.

    Example fit_keywords entry:
        "oversized": {
            "operations": ["add_ease"],
            "default_values": {
                "chest_width": 5,
                "body_width": 5
            }
        }

    For MVP, we collapse default_values down to a single value_cm per operation.
    Strategy:
    - Take the max of the default_values for that fit keyword.
    """
    rules: List[Dict[str, Any]] = []

    lower = text.lower()

    for fit_word, config in fit_keywords.items():
        if fit_word not in lower:
            continue

        ops = config.get("operations", [])
        default_values = config.get("default_values", {})

        # Collapse per-target default values into a single representative cm value.
        numeric_defaults = []
        for v in default_values.values():
            try:
                numeric_defaults.append(float(v))
            except (TypeError, ValueError):
                continue

        if not numeric_defaults:
            continue

        # Use the max default value as a simple heuristic.
        value_cm = max(numeric_defaults)

        for op in ops:
            rules.append(
                {
                    "operation": op,
                    "value_cm": value_cm,
                }
            )

    return rules


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

    Current Behavior (Heuristic)
    ----------------------------
    - Uses:
        - operations.synonyms
        - intensity_keywords
        - fit_keywords
    - Is intentionally simple and deterministic.
    - Does NOT call any LLM yet.

    Future Behavior
    ---------------
    - Replace the heuristic with an LLM call.
    - Use mapping to constrain outputs (allowed operations, fit bundles, etc.).
    """
    if mapping is None:
        mapping = load_prompt_mapping()

    lower = prompt.lower()
    rules: List[Dict[str, Any]] = []
    seen_operations: set[str] = set()

    operations_cfg = mapping.get("operations", {})
    intensity_map = mapping.get("intensity_keywords", {}) or {}
    fit_keywords = mapping.get("fit_keywords", {}) or {}

    # ------------------------------------------------------------------------
    # 1. Fit keywords (e.g., "oversized", "relaxed", "fitted", "cropped")
    # ------------------------------------------------------------------------
    fit_rules = _apply_fit_keywords(lower, fit_keywords)
    for r in fit_rules:
        op = r["operation"]
        if op not in seen_operations:
            rules.append(r)
            seen_operations.add(op)

    # ------------------------------------------------------------------------
    # 2. Operation synonyms + numeric/intensity handling
    # ------------------------------------------------------------------------
    explicit_value = _extract_numeric_cm(lower)
    intensity_value = _detect_intensity(lower, intensity_map)

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
        # 2. Intensity keyword (e.g., "a bit", "very oversized")
        # 3. Fallback default of 3.0
        if explicit_value is not None:
            value_cm = explicit_value
        elif intensity_value is not None:
            value_cm = intensity_value
        else:
            value_cm = 3.0

        rules.append(
            {
                "operation": op_name,
                "value_cm": value_cm,
            }
        )
        seen_operations.add(op_name)

    # ------------------------------------------------------------------------
    # 3. Fallback rule (ensure non-empty rule set)
    # ------------------------------------------------------------------------
    if not rules:
        # If mapping includes add_ease, use that as a safe default.
        if "add_ease" in operations_cfg:
            rules.append({"operation": "add_ease", "value_cm": 2.0})
        else:
            # Absolute last-resort fallback.
            rules.append({"operation": "crop_hem", "value_cm": 2.0})

    return rules
