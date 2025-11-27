# Developer Guide – CUTMIND MVP

This guide explains how the CUTMIND MVP backend, rule engine, geometry engine, and routing should be implemented.  
It supports **three garment block families** (tshirt, long_sleeve, crop_top) and a minimal natural-language → pattern transformation workflow.

Before coding, read:
- `mvp_spec.md`
- `README.md`
- `config/prompt_mapping.json`

---

# 1. Repository Overview

```
/backend
  server.py
  router.md
  api_contract.md
  interpretation.py
  rules_engine.py
  geometry_engine.py
  pattern_loader.py
/config
  prompt_mapping.json
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
```

All backend code will eventually live inside `/backend`.  
Frontend is minimal and does not affect backend logic.

---

# 2. Backend Architecture

The backend consists of **four key modules**:

### 2.1 Interpretation Layer (`interpretation.py`)
- Accepts the natural-language prompt.
- Calls LLM provider (OpenAI or compatible).
- Returns structured rule JSON as defined in `api_contract.md`.
- No geometry or SVG logic should exist here.

### 2.2 Rules Engine (`rules_engine.py`)
- Validates rule format.
- Ensures operations and units match MVP spec.
- Rejects unsupported rules.
- Passes rules to the geometry engine for application.

### 2.3 Geometry Engine (`geometry_engine.py`)
- Loads SVG via `pattern_loader.py`.
- Applies transformations to SVG paths/groups.
- Outputs modified SVG string.
- Must remain deterministic.

### 2.4 Routing Layer (`router.md` → server.py)
- Maps HTTP endpoints to backend logic.
- Defines request/response structure.

---

# 3. Block Family System

CUTMIND MVP supports **three block families**:

- `tshirt`
- `long_sleeve`
- `crop_top`

Each family has identical structure:
- `/front.svg`
- `/back.svg`
- `/sleeve.svg`

This is crucial because:
- Operation logic is the same across all 3.
- Geometry transformations require consistent grouping conventions.

All pattern SVGs **must** have consistent `id` attributes such as:

```
<g id="front">
<g id="back">
<g id="sleeve">
```

If missing, geometry engine will fail.

---

# 4. Interpretation Layer (LLM)

### Responsibilities
- Convert user prompt → structured rule JSON.
- Validate rules against `prompt_mapping.json`.
- Reject out-of-scope instructions.

### Implementation Steps
1. Load and parse `prompt_mapping.json`.
2. Send prompt + mapping to LLM.
3. Extract rule JSON.
4. Normalize keys (lowercase, underscores).
5. Return errors when needed.

### Do NOT:
- Make geometry edits
- Guess unsupported operations
- Output anything other than rule JSON

---

# 5. Rules Engine

### Responsibilities
- Validate each rule:
  - operation is allowed
  - value_cm is numeric
- Transform rules into executable geometry operations.
- Reject unsupported combinations.

### Rule Format
```json
{
  "operation": "crop_hem",
  "value_cm": 5
}
```

### Failure Modes
- Missing `value_cm`
- Non-numeric values
- Operation not in MVP list
- Empty rule arrays

### Output
- Cleaned, validated rule list
- Pattern ID (string)
- Ready for geometry engine

---

# 6. Geometry Engine

### Responsibilities
- Load base SVG via `pattern_loader.py`
- Apply transforms:
  - Vertical offset (hem)
  - Horizontal width changes (ease)
  - Sleeve length
  - Neckline depth

### SVG Requirements
- Must preserve XML validity
- Must preserve folder structure
- Must maintain consistent group IDs

### Example Transform Types
- Translate Y-positions of paths
- Scale or stretch sleeve width
- Move neckline bezier control points

Geometry engine **must never**:
- Create new paths
- Delete paths
- Perform style/visual smoothing
- Modify non-geometry attributes unless needed (`x`, `y`, `d`, `transform` only)

---

# 7. Pattern Loader

### Responsibilities
- Load SVG for given pattern family.
- Return as string for geometry engine.
- File structure must match:

```
pattern/{pattern_id}/front.svg
pattern/{pattern_id}/back.svg
pattern/{pattern_id}/sleeve.svg
```

### Fail Conditions
- Invalid pattern_id
- Missing SVG file
- Invalid XML

---

# 8. API Routing

The FastAPI routing exposes three endpoints:

### 8.1 POST `/interpret`
- Calls `interpretation.py`
- Converts prompt → rules

### 8.2 POST `/apply-rules`
- Validates rules
- Loads pattern
- Applies geometry transformations
- Returns modified SVG

### 8.3 GET `/patterns/{id}`
- Serves base pattern SVG files

Error handling follows unified format:

```json
{
  "error": "invalid_rule_format",
  "details": {}
}
```

No additional formats are allowed.

---

# 9. Development Conventions

### Coding Standards
- Python 3.10+
- FastAPI + pydantic
- Black formatter recommended
- Avoid inline logic inside `server.py`

### Naming Standards
- snake_case for functions
- pattern families: lowercase (`tshirt`, `long_sleeve`, `crop_top`)
- operations: lowercase snake_case

### File Standards
- All SVG files must have descriptive IDs
- Avoid raw string manipulation where possible—use XML parsing

---

# 10. Local Development Setup

### Install Dependencies
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run Server
```bash
uvicorn server:app --reload
```

### Run Tests (once implemented)
```bash
pytest
```

---

# 11. Error Handling Rules

### All modules must throw unified errors:

Example:
```json
{
  "error": "invalid_rule_format",
  "details": {
    "operation": "unknown_operation"
  }
}
```

### Error Origins
- Bad JSON
- Unsupported operation
- Invalid pattern ID
- Non-numeric rule values
- Geometry failure
- Missing SVG assets

**No stack traces should leak into API responses.**

---

# 12. Future Developer Notes (Post-MVP)

These items are out-of-scope but the architecture must allow them:

- Multi-size garments  
- Automatic grading  
- Tech pack generation  
- Fabric simulation  
- Hoodies, jackets, pants  
- Real-time editing  
- PDF export  

---

# 13. Final Notes

This document is the **source of truth** for backend developers.  
If any rule or behavior differs from this file, this file wins.

Before implementation begins, ensure:
- Pattern SVGs are clean & consistent
- prompt_mapping.json matches MVP operations
- README.md and mvp_spec.md are aligned

CutMIND MVP must remain **narrow, deterministic, and stable**.

