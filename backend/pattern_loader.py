"""
pattern_loader.py

Purpose:
- This module is responsible for loading base pattern assets (SVG files)
  from the /pattern directory.
- It provides a simple interface for retrieving SVG strings by pattern ID.

Responsibilities:
- Map pattern IDs (e.g., "tshirt_block_v1") to actual SVG files on disk.
- Read and return SVG content as a string.
- Raise a clear error if the pattern is missing or unsupported.

Non-responsibilities (handled elsewhere):
- Geometry mutations → geometry_engine.py
- HTTP handling → server.py, router.py
- Tech pack generation → techpack_generator.py

MVP Scope:
- Single pattern ID: "tshirt_block_v1".
- Single SVG source file under /pattern.

Implementation Status:
- Placeholder only. Currently does not perform real file I/O.
"""

from pathlib import Path


class PatternNotFoundError(Exception):
    """Raised when a requested pattern ID cannot be resolved or loaded."""
    pass


def get_pattern_path(pattern_id: str) -> Path:
    """
    Resolve the filesystem path for a given pattern ID.

    In the MVP, this will likely map:
        "tshirt_block_v1" -> /pattern/tshirt_block_v1.svg

    :param pattern_id: The identifier for the pattern.
    :return: Path object pointing to the SVG file.
    :raises PatternNotFoundError: if the pattern ID is unsupported.
    """
    # Placeholder mapping. This may later be configured or expanded.
    base_dir = Path(__file__).parent.parent / "pattern"

    if pattern_id == "tshirt_block_v1":
        return base_dir / "tshirt_block_v1.svg"

    raise PatternNotFoundError(f"Unsupported pattern_id: {pattern_id}")


def load_pattern_svg(pattern_id: str) -> str:
    """
    Load the SVG for a given pattern ID and return it as a string.

    Expected behavior (once implemented):
    - Use get_pattern_path() to resolve the filepath.
    - Read the SVG file from disk.
    - Return the SVG contents.

    Current placeholder behavior:
    - Returns a minimal SVG stub instead of reading from disk.

    :param pattern_id: The identifier for the pattern.
    :return: SVG content as a string.
    :raises PatternNotFoundError: if the pattern ID is unsupported.
    """
    # For now, we validate the ID and return a stub.
    _ = get_pattern_path(pattern_id)

    # Placeholder SVG stub (not a real pattern).
    stub_svg = "<svg><!-- Placeholder SVG for pattern_id='{}' --></svg>".format(pattern_id)
    return stub_svg
