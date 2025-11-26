"""
interpretation.py

Purpose:
- This module will handle natural-language → structured rule translation.
- It loads prompt mappings from /config/prompt_mapping.json.
- It sends the user prompt to the LLM provider (OpenAI or similar),
  and converts the model output into a normalized rule structure.

Responsibilities:
- Read prompt_mapping.json and use synonyms to guide extraction.
- Call the LLM with a controlled prompt template.
- Parse the model's response and normalize operations into:
    {
        "operation": "crop_hem",
        "value_cm": 5
    }
- Ensure all operations match supported MVP operations before
  passing output to the rules engine.

Non-responsibilities (handled elsewhere):
- Rule validation → rules_engine.py
- Geometry operations → geometry_engine.py
- Tech pack creation → techpack_generator.py

Implementation Status:
- Placeholder only. No functional code yet.
"""

# Example placeholder structure (not active code):

# import json
# from pathlib import Path
#
# class Interpreter:
#     def __init__(self):
#         mapping_path = Path(__file__).parent.parent / "config" / "prompt_mapping.json"
#         self.mapping = json.loads(mapping_path.read_text())
#
#     def parse_prompt(self, prompt: str) -> dict:
#         """
#         Placeholder for:
#         - LLM call
#         - synonym matching
#         - operation extraction
#         - numeric value normalization
#         """
#         return {"rules": []}
#
# interpreter = Interpreter()
