"""
pattern_loader.py

CUTMIND MVP – Pattern Loader

Purpose:
- Load base SVG pattern assets from the /pattern directory.
- Provide a simple interface for the geometry engine and API layer.

MVP Scope:
- Three pattern families:
    - tshirt
    - long_sleeve
    - crop_top
- Each family has three pieces:
    - front.svg
    - back.svg
    - sleeve.svg

For now, the public function `load_pattern_svg(pattern_id)` returns the
SVG for the FRONT piece by default, since `server.py` expects a single
SVG string. As the geometry engine matures, this can be extended to load
and combine multiple pieces if needed.
"""

from __future__ import annotations

from pathlib import Path


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------


def _get_pattern_root() -> Path:
    """
    Return the path to the /pattern directory relative to this file.

    Expected project structure:

        /backend
            pattern_loader.py
        /pattern
            /tshirt
                front.svg
                back.svg
                sleeve.svg
            /long_sleeve
                front.svg
                back.svg
                sleeve.svg
            /crop_top
                front.svg
                back.svg
                sleeve.svg
    """
    backend_dir = Path(__file__).resolve().parent
    project_root = backend_dir.parent
    return project_root / "pattern"


def _load_svg_file(path: Path) -> str:
    """
    Load a single SVG file as a string.

    Raises FileNotFoundError if the file does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"SVG file not found: {path}")

    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_pattern_svg(pattern_id: str, piece: str = "front") -> str:
    """
    Load the SVG for the given pattern family and piece.

    Parameters
    ----------
    pattern_id : str
        One of:
        - "tshirt"
        - "long_sleeve"
        - "crop_top"

    piece : str, optional
        One of:
        - "front"
        - "back"
        - "sleeve"
        Defaults to "front" for MVP.

    Returns
    -------
    str
        The raw SVG content as a string.

    Raises
    ------
    FileNotFoundError
        If the requested SVG file does not exist.

    Notes
    -----
    - `server.py` currently calls this function with only `pattern_id`,
      relying on the default piece="front".
    - The geometry engine can optionally use `piece` to load all three
      components if needed in future versions.
    """
    pattern_root = _get_pattern_root()

    # Construct path: /pattern/{pattern_id}/{piece}.svg
    svg_path = pattern_root / pattern_id / f"{piece}.svg"

    return _load_svg_file(svg_path)
