# CUTMIND MVP – Repository Overview

CUTMIND is an AI-assisted pattern transformation system. It interprets natural-language instructions (e.g., “crop the hem by 5 cm,” “add 3 cm ease,” “make sleeves oversized”) and applies structured geometry operations to SVG pattern files.

The MVP supports **three garment block families**:
- T-shirt  
- Long sleeve  
- Crop top  

Each block contains three SVG pattern pieces:
- front.svg  
- back.svg  
- sleeve.svg  

This repository defines the structure and specification for the MVP. Implementation has not yet begun.

---

## 1. Folder Structure

### `/backend`
Intended for backend services, including:
- Natural-language → structured rule interpretation  
- Rules engine  
- SVG geometry engine  
- HTTP API server (FastAPI example)  

### `/frontend`
Will contain the lightweight UI for entering prompts and previewing modified patterns.

### `/config`
Configuration files such as natural-language → operation mappings.

### `/pattern`
Base pattern assets for the three blocks:

```
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

### `mvp_spec.md`
Defines garment rules, supported operations, constraints, and mapping logic.

### `DEVELOPERS.md`
Internal developer reference for conventions, architecture, and implementation flow.

---

## 2. Requirements and Vision

The MVP’s core goal is to validate:

- Whether an LLM can reliably translate natural-language garment modification requests into structured, machine-readable rules.
- Whether those rules can be deterministically applied to SVG pattern pieces across **three block types**.
- Whether CUTMIND can form a scalable foundation for multi-garment, multi-adjustment workflows.

---

## 3. How to Run This Repo (Once Code Exists)

There is no executable code yet.  
The following installation steps are placeholders.

---

### Backend (FastAPI Example)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn server:app --reload
```

### Environment Variables

```env
OPENAI_API_KEY=...
MODEL_PROVIDER=openai
```

---

### Frontend (React/Vite Example)

```bash
cd frontend
npm install
npm run dev
```

---

### Testing (Planned)

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## 4. Contributions and Documentation Rules

- Keep `README.md`, `mvp_spec.md`, and `DEVELOPERS.md` updated as system design evolves.  
- Do not commit secrets or API keys.  
- Maintain consistency in naming, structure, and mapping logic.  
- Ensure rule definitions and geometry operations remain synchronized.  
- The repo should be understandable to a new engineer within ten minutes.

---

## 5. Status

This repository is a structural and specification scaffold.  
Implementation will begin once requirements are finalized.

---

## 6. Scope of the MVP

### In-Scope
- Three block families:
  - T-shirt  
  - Long sleeve  
  - Crop top  
- One format: **SVG patterns**  
- Core operations:
  - Crop hem  
  - Adjust body length  
  - Adjust sleeve width  
  - Adjust sleeve length  
  - Add/remove ease  
  - Adjust neckline depth  
- Natural-language → structured JSON mapping  
- Deterministic geometry transformations  
- Simple combined adjustments (e.g., “widen sleeves and crop hem”)  

### Out-of-Scope
- Tech packs (removed from MVP)  
- Multi-piece garments beyond the three blocks  
- DXF/AAMA formats  
- Automatic grading  
- Fabric simulation  
- 3D visualization  
- Real-time editing  
- Multi-size support  
- BOM (Bill of Materials)  
- Production-ready documentation  

---

## 7. Technical Assumptions

### LLM Layer
- Generates structured rule JSON only  
- No geometry logic inside the LLM  
- Must be deterministic given identical prompts  

### Pattern Format
- All patterns represented as clean SVG paths/groups  
- Transformations must maintain SVG validity  

### Rules Engine
- Only numeric & explicit instructions  
- No conflict resolution in MVP  
- Rules applied sequentially  

### Geometry Engine
- Vector operations only  
- Modifies SVG elements based on parsed rules  
- Supports three block families with consistent structure  

### Frontend
- Simple UI  
- Displays SVG before/after  

### Backend
- Stateless  
- Provides endpoints for interpreting prompts and applying rules  

---

## 8. Preliminary API Design

### POST `/interpret`

Converts natural-language instructions into structured rules.

**Request**
```json
{
  "prompt": "crop the hem by 5 cm and widen the sleeves"
}
```

**Response**
```json
{
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 },
    { "operation": "widen_sleeve", "value_cm": 3 }
  ]
}
```

---

### POST `/apply-rules`

Applies rules to a specified block family.

**Request**
```json
{
  "pattern_id": "tshirt",
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 }
  ]
}
```

**Response**
```json
{
  "modified_pattern_svg": "<svg>...modified block...</svg>"
}
```

---

### GET `/patterns/{id}`

Returns raw SVG for:
- tshirt  
- long_sleeve  
- crop_top  

---

### Unified Error Format

```json
{
  "error": "invalid_rule_format",
  "details": {}
}
```

---

## 9. Planned Stack

### Backend
- Python  
- FastAPI  
- pydantic  
- uvicorn  

### Frontend
- React  
- Vite  

### LLM Layer
- OpenAI or compatible provider  

### Geometry
- Custom SVG transformation utilities  

### Deployment
- Local environment during MVP  

---

## 10. Open Questions

### Pattern
- Should instructions use cm or SVG units?  
- Should edits apply to paths or groups?  

### Rules Processing
- Should multiple rules merge or execute sequentially?  

### Frontend
- Should UI support side-by-side preview?  

### Backend
- Should patterns be cached for faster responses?  

---

## 11. Future Extensions (Not for MVP)

- Tech packs (post-MVP)
- Additional garment families  
- DXF/AAMA export  
- Automated grading  
- 3D visualization  
- Real-time pattern editing  
- Fabric simulation  
- Bulk operations  

---

## 12. License

```
This repository is private and proprietary.
All rights reserved.
Unauthorized distribution or copying is prohibited.
```
