# CUTMIND Backend (MVP – To Be Implemented)

The backend provides all core logic for the CUTMIND MVP.  
It exposes APIs for natural-language interpretation, rule validation, pattern transformation, and tech pack generation.

This directory currently contains placeholders and documentation only.  
Implementation will begin once the full architectural plan is finalized.

---

## Core Components (Planned)

### **1. LLM Interpretation Layer**
- Converts natural-language instructions into structured JSON rules.
- Uses provider (OpenAI or compatible) defined through environment variables.
- Strictly produces rule objects; it does not perform geometry.

**Module:** `interpretation.py`

---

### **2. Rules Engine**
- Validates structured rules.
- Ensures each operation is supported by the MVP.
- Enforces numeric requirements.

**Module:** `rules_engine.py`

---

### **3. Pattern Geometry Engine**
- Loads base SVG files.
- Applies vector transformations based on validated rules.
- Must produce valid, deterministic SVG.

**Module:** `geometry_engine.py`

---

### **4. Tech Pack Generator**
- Creates a tech pack draft from:
  - pattern ID  
  - applied rule set  
  - simplified measurement outputs  
- Output is JSON formatted for the frontend.

**Module:** `techpack_generator.py`

---

### **5. Pattern Loader**
- Retrieves base pattern files from `/pattern`.
- MVP supports one pattern: `tshirt_block_v1`.

**Module:** `pattern_loader.py`

---

### **6. API Server**
Responsible for exposing endpoints described in `api_contract.md`:

- `POST /interpret`
- `POST /apply-rules`
- `GET /patterns/{id}`

**Entry Point:** `server.py`

---

## Language and Framework

### Primary Target
- **Python (FastAPI)**

### Alternative Option (Not recommended for MVP)
- Node.js (Express)

The MVP prioritizes Python due to ease of integrating LLM logic and deterministic geometry tooling.

---

## Reference Files

Engineers should review:

- `mvp_spec.md` (system behavior)
- `api_contract.md` (request/response shapes)
- `router.md` (endpoint flow)
- `config/prompt_mapping.json` (natural language → operations mapping)
- `/pattern/*` (base assets)

---

## Implementation Notes

- No modules are implemented yet; all files are placeholders.
- Backend should remain stateless for the MVP.
- Do not commit secrets. Use `.env` or system environment variables.
- All errors must follow the shared error schema defined in `api_contract.md`.

---

## Future Work (Post-MVP)

Once the MVP is validated, backend expansion may include:

- Support for multi-piece garments
- DXF/AAMA import/export
- Full production-ready tech pack generator
- Authentication
- Versioned API
- Real-time pattern editing
- Multi-size grading engine

