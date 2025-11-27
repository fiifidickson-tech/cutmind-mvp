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
  "error": "some_error_code",
  "details": {}
}
```

- `error` must be a short machine-readable string.  
- `details` must always be an object.  
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

On failure, the route must return the unified error format.  
Typical error codes:

- `"unsupported_instruction"`
- `"invalid_rule_format"`
- `"internal_error"`

Example error response:

```json
{
  "error": "unsupported_instruction",
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

On failure, the route must return the unified error format.  
Typical error codes:

- `"invalid_pattern_id"`  
- `"invalid_rule_format"`  
- `"geometry_application_failed"`  
- `"internal_error"`

Example error response:

```json
{
  "error": "invalid_rule_format",
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
- Load SVG from `/pattern/{id}/front.svg`, `/back.svg`, and `/sleeve.svg`.  
- If the file or pattern family does not exist → return unified error.

## Successful Response (raw SVG)
```
<svg>...</svg>
```

## Failure Cases

- `"invalid_pattern_id"`

Example error response:

```json
{
  "error": "invalid_pattern_id",
  "details": {}
}
```

---

# 5. Routing Integration in `server.py`

Expected structure:

```python
from fastapi import FastAPI
from router import router

app = FastAPI()
app.include_router(router)
```

Route handlers should only orchestrate:
- interpretation → rules validation → geometry engine → response  
No heavy logic inside routing functions.

---

# 6. Final Notes

- Router must remain stable for entire MVP.  
- No new routes should be added until MVP is complete.  
- If behavior changes, update `api_contract.md`, `router.md`, and `mvp_spec.md`.
