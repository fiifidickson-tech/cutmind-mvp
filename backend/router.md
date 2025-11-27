# Router Specification – CUTMIND MVP

This document defines how API routes must be structured in the backend.  
The routing layer connects HTTP requests → interpretation layer → rules engine → geometry engine.

CUTMIND MVP exposes **three endpoints**:

1. `POST /interpret`
2. `POST /apply-rules`
3. `GET /patterns/{id}`

No additional routes are allowed during the MVP.

---

# 1. General Routing Requirements

- Must use **FastAPI**.
- Each endpoint must return JSON or SVG as specified.
- All errors follow the unified error format:

```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

- All endpoints must be registered in `server.py`.
- Router logic must remain thin — no heavy processing in routing.

---

# 2. POST `/interpret`

## Purpose
Convert natural-language text into structured rule JSON.

## Flow
1. Receive `prompt` (string).
2. Pass text to `interpretation.py`.
3. Validate that resulting rules match MVP format.
4. Return structured rule JSON.

## Request Body
```json
{
  "prompt": "crop the hem by 5 cm and widen the sleeves"
}
```

## Successful Response
```json
{
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 },
    { "operation": "widen_sleeve", "value_cm": 3 }
  ]
}
```

## Failure Cases
- LLM returns invalid structure
- Unsupported operations
- Missing numeric values

Must return:

```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

---

# 3. POST `/apply-rules`

## Purpose
Apply validated rules to one of the three MVP block families.

Valid `pattern_id` values:
- `tshirt`
- `long_sleeve`
- `crop_top`

## Flow
1. Validate `pattern_id`.
2. Validate each rule.
3. Load base SVG through `pattern_loader.py`.
4. Pass SVG + rules to `geometry_engine.py`.
5. Return transformed SVG.

## Request Body
```json
{
  "pattern_id": "tshirt",
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 }
  ]
}
```

## Successful Response
```json
{
  "modified_pattern_svg": "<svg>...</svg>"
}
```

## Failure Cases
- Invalid pattern ID
- Invalid rule structure
- Geometry transformation failure

All failures must return:

```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

---

# 4. GET `/patterns/{id}`

## Purpose
Return the raw base SVG for the requested pattern family.

Valid IDs:
- `tshirt`
- `long_sleeve`
- `crop_top`

## Behavior
- Load SVG from `/pattern/{id}/front.svg`, `/back.svg`, or `/sleeve.svg`.
- If the file or pattern family does not exist → return unified error.

## Example Response
```
<svg>...</svg>
```

(This route returns raw SVG, not JSON.)

---

# 5. Routing Integration in `server.py`

Example of expected structure:

```python
from fastapi import FastAPI
from interpretation import interpret_prompt
from rules_engine import validate_rules
from geometry_engine import apply_geometry
from pattern_loader import load_pattern

app = FastAPI()

@app.post("/interpret")
def interpret(payload: dict):
    # Call interpretation layer
    # Return structured rules
    pass

@app.post("/apply-rules")
def apply_rules(payload: dict):
    # Validate pattern ID
    # Validate rules
    # Apply geometry engine
    # Return modified SVG
    pass

@app.get("/patterns/{pattern_id}")
def get_pattern(pattern_id: str):
    # Return base SVG
    pass
```

Do NOT implement heavy logic directly in route functions.  
Use dedicated modules.

---

# 6. Final Notes

- Router must remain stable for entire MVP.
- No new routes should be added until MVP is complete.
- If behavior changes, update `api_contract.md` and this file.
