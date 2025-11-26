# router.md

## Purpose
This file defines the high-level routing structure for the backend.  
It describes which modules handle which endpoints and how requests flow through the system.

The router acts as the entry point for:
- LLM interpretation  
- Rule validation  
- Geometry transformation  
- Tech pack generation  
- Pattern retrieval  

---

## Route Overview

| Method | Endpoint           | Description                                           | Handler Module                |
|--------|---------------------|--------------------------------------------------------|-------------------------------|
| POST   | `/interpret`        | Converts natural-language instructions into rule JSON | `interpretation.py`           |
| POST   | `/apply-rules`      | Applies rules to pattern and generates tech pack      | `rules_engine.py` + `geometry_engine.py` + `techpack_generator.py` |
| GET    | `/patterns/{id}`    | Retrieves base SVG pattern asset                      | `pattern_loader.py`           |

---

## Routing Flow (Planned)

### 1. `POST /interpret`
**Flow**
1. Router receives the prompt  
2. Sends prompt to LLM interpreter (`interpretation.py`)  
3. Returns structured rule JSON  

**Handler**
- `interpretation.py`
  - `parse_prompt(prompt: str) -> dict`

---

### 2. `POST /apply-rules`
**Flow**
1. Router validates request structure  
2. Fetches base pattern SVG (`pattern_loader.py`)  
3. Sends rules to rules engine  
4. Rules engine hands geometric instructions to geometry engine  
5. Geometry engine outputs modified SVG  
6. Tech pack generator builds the draft tech pack JSON  
7. Router returns:
   - modified SVG  
   - tech pack JSON  

**Handlers**
- `rules_engine.py`
  - `validate_rules(rules: list) -> list`
- `geometry_engine.py`
  - `apply_operations(svg: str, rules: list) -> str`
- `techpack_generator.py`
  - `generate_techpack(pattern_id: str, rules: list) -> dict`

---

### 3. `GET /patterns/{id}`
**Flow**
1. Router receives pattern ID  
2. Loads SVG from `/pattern` directory  
3. Returns SVG string  

**Handler**
- `pattern_loader.py`
  - `load_pattern(pattern_id: str) -> str`

---

## Error Flow (Unified)

All handlers must return errors using the shared format:

```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

Errors may originate from:
- Missing fields  
- Unsupported operations  
- Invalid pattern IDs  
- Geometry failures  
- Failed LLM interpretation  

The router must translate all of them into consistent JSON responses.

---

## Notes

- This router description does not include implementation details (FastAPI, Express, etc). Implementation is decided later.  
- Any new endpoints must be added to this file before code is written.  
- The router must remain simple and delegate all logic to the appropriate modules.  
