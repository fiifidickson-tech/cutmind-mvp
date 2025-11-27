"""
interpretation.py

CUTMIND MVP – Interpretation Layer

Purpose:
- Convert natural-language garment modification prompts into structured rule JSON.
- This module defines the interface that the rest of the backend depends on.

MVP Scope:
- Supported operations and structure are defined in:
    - mvp_spec.md
    - api_contract.md
    - prompt_mapping.json

Implementation Status:
- This file currently provides a placeholder implementation so the API shape
  remains stable while the LLM integration is not yet implemented.
- It is safe to call `interpret_prompt()` during early development; it will
  return deterministic dummy rules until real logic is added.

Expected Function Signature:
- interpret_prompt(prompt: str) -> list[dict]
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Configuration Loading
# ---------------------------------------------------------------------------


def _get_config_path() -> Path:
    """
    Return the path to config/prompt_mapping.json relative to this file.

    This assumes the following structure:

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

    This file is expected to include:
    - synonyms for operations
    - allowed operations
    - example phrases

    If the file does not exist, returns an empty mapping but does not crash,
    so the rest of the system can continue using default behavior.
    """
    path = _get_config_path()
    if not path.exists():
        # Silent fallback to an empty mapping so early development is not blocked.
        return {}

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # If parsing fails, treat as empty mapping.
        return {}


# ---------------------------------------------------------------------------
# Interpretation Logic (Placeholder)
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
        Optional mapping loaded from config/prompt_mapping.json.
        Can contain:
        - synonyms
        - phrase → operation hints
        - domain-specific tweaks

    Returns
    -------
    list[dict]
        A list of rule dictionaries matching the API contract.

    Current Behavior (Placeholder)
    ------------------------------
    - This implementation does NOT actually call an LLM yet.
    - It returns deterministic dummy rules so the backend can be wired and tested.
    - Replace the placeholder logic with a real LLM integration later.

    Real Implementation Notes
    -------------------------
    When implementing LLM integration:
    - Use `mapping` to bias the prompt (e.g., include allowed operations).
    - Ask the model to return ONLY JSON matching the rules format.
    - Parse JSON safely and validate operations/values.
    - Do not let the model invent unsupported operations.
    """
    # Load mapping if not provided, but do not enforce its presence.
    if mapping is None:
        mapping = load_prompt_mapping()

    # ----------------------------------------------------------------------------
    # PLACEHOLDER IMPLEMENTATION
    # ----------------------------------------------------------------------------
    # For now, ignore the actual prompt content and return a deterministic, valid
    # rule structure that conforms to the MVP spec. This keeps the rest of the
    # system stable while interpretation logic is being built.
    #
    # You can modify this dummy behavior for local testing (e.g., vary based on
    # keywords like "crop", "widen", etc.), but the interface must remain the same.
    # ----------------------------------------------------------------------------

    dummy_rules: List[Dict[str, Any]] = []

    normalized = prompt.lower()

    # Very primitive keyword-based heuristic, just for early testing.
    # This is NOT the final LLM-driven behavior.
    if "crop" in normalized or "shorten" in normalized:
        dummy_rules.append({"operation": "crop_hem", "value_cm": 5.0})

    if "widen" in normalized and "sleeve" in normalized:
        dummy_rules.append({"operation": "widen_sleeve", "value_cm": 3.0})

    if not dummy_rules:
        # Default fallback rule so the API never returns an empty list during early dev.
        dummy_rules.append({"operation": "add_ease_body", "value_cm": 2.0})

    return dummy_rules
