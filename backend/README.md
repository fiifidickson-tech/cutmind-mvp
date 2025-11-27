# CUTMIND Backend (MVP – To Be Implemented)

The backend provides all core logic for the CUTMIND MVP.  
It exposes APIs for natural-language interpretation, rule validation, pattern transformation, and base pattern retrieval.

This directory currently contains placeholders and documentation only.  
Implementation will begin once the full architectural plan is finalized.

---

## Core Components (Planned)

### **1. LLM Interpretation Layer**
- Converts natural-language instructions into structured JSON rules.
- Uses provider (OpenAI or compatible) defined through environment variables.
- Strictly produces rule objects; it does *not* perform geometry.

**Module:** `interpretation.py`

---

### **2. Rules Engine**
- Validates structured rules from the interpretation layer or client.
- Ensures each operation is supported by the MVP.
- Enforces numeric requirements (`value_cm` must be numeric).

**Module:** `rules_engine.py`

---

### **3. Pattern Geometry Engine**
- Loads base SVG files.
- Applies vector transformations based on validated rules.
- Must produce valid, deterministic SVG output.

**Module:** `geometry_engine.py`

---

### **4. Pattern Loader**
- Retrieves base pattern files from `/pattern`.
- MVP supports three blocks:
  - `tshirt`
  - `long_sleeve`
  - `crop_top`

**Module:** `pattern_loader.py`

---

### **5. API Server**
Responsible for exposing MVP endpoints:

- `POST /interpret`  
- `POST /apply-rules`  
- `GET  /patterns/{id}`

**Entry Point:** `server.py`

---

## Language and Framework

### Primary Target
- **Python (FastAPI)**

Python is chosen for:
- simpler LLM integration  
- deterministic SVG/geometry processing  
- clarity for future scaling  

---

## Reference Files

Engineers should review:

- `mvp_spec.md` (system behavior + in-scope rules)
- `api_contract.md` (request/response shapes)
- `router.md` (endpoint flow)
- `config/prompt_mapping.json` (language → operation mapping)
- `/pattern/*` (base assets)

---

## Implementation Notes

- No modules are implemented yet; files are placeholders.
- Backend must remain *stateless*.
- Do not commit secrets. Use `.env` or system environment variables.
- All errors must follow the unified error schema:

```json
{
  "error": "some_error_code",
  "details": {}
}
