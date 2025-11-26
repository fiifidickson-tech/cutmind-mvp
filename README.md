# CUTMIND MVP – Repository Overview

CUTMIND is an AI-assisted pattern transformation system. It interprets natural-language instructions (e.g., “crop the hem by 5 cm,” “add 3 cm ease to the chest,” “make sleeves oversized”) and applies structured geometry operations to pattern files.

In addition to generating modified patterns, CUTMIND also produces a **tech pack draft** based on the applied adjustments. This provides founders and new designers with a ready-to-review document they can send to manufacturers. The tech pack is intentionally lightweight for the MVP and includes garment metadata, applied operations, and simplified measurements. Final manufacturing review is still expected, but this feature significantly accelerates early sampling and reduces the need for technical design expertise.

This repository contains the current specification and initial structure for the MVP. Implementation has not yet begun; this repo establishes the technical foundation for development.

---

## 1. Folder Structure

A clear explanation of each folder and its purpose.

### `/backend`
(Currently unimplemented.) Intended to contain backend services responsible for:

- LLM interpretation endpoint  
- Rules engine  
- Pattern geometry engine (operating on SVG)  
- **Tech pack generation module (techpack_generator.py)**  
- HTTP API for frontend and external clients  

### `/frontend`
(Currently unimplemented.) Will contain the user interface for testing natural-language adjustments, previewing pattern output, and viewing the tech pack draft.

### `/config`
Contains configuration files, including mappings between natural-language terms and engineered operations. Future versions may include tech pack templates.

### `/pattern`
Base pattern assets (e.g., the T-shirt block SVG), which serve as input to the geometry and tech pack engines.

### `mvp_spec.md`
Full MVP specification, including requirements, constraints, and operational rules.

### `DEVELOPERS.md`
Documentation for contributors, environment setup guidelines, and project conventions.

---

## 2. Requirements and Vision

CUTMIND’s MVP validates whether natural-language adjustments can be reliably converted into structured rules, and whether those rules can be applied deterministically to an SVG pattern.

The MVP also validates whether a **tech pack draft** can be generated from the modified pattern and applied rules, giving users (especially early-stage founders) a fast way to communicate manufacturing intent.

### High-level goals:
- Demonstrate natural-language → structured rule translation  
- Demonstrate deterministic geometry transformations  
- Provide a minimal UI for testing  
- Enable further expansion toward multi-garment capabilities  
- **Generate a basic tech pack draft for manufacturer handoff**  

---

## 3. How to Run This Repo (Once Code Exists)

There is currently no executable code.  
The following outline describes the expected project setup and will be updated once development begins.

---

### Backend (Planned – FastAPI Example)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Example environment variables

```env
OPENAI_API_KEY=...
MODEL_PROVIDER=openai
```

---

### Frontend (Planned – React/Vite Example)

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

- Keep `README.md`, `mvp_spec.md`, and `DEVELOPERS.md` up to date with system changes.  
- Do not commit secrets; use environment variables.  
- Maintain documentation consistency as new components or folders are added.  
- Ensure mappings, rule definitions, and geometry operations stay synchronized.  
- The repository should be understandable to a new engineer within ten minutes.

---

## 5. Status

This repository is a structural and specification scaffold. Implementation will begin once requirements are finalized.

---

## 6. Scope of the MVP

The MVP is intentionally narrow. Its purpose is to validate whether natural-language instructions can be translated into consistent, reproducible pattern modifications using a rules-based geometry engine and whether a basic tech pack draft can be generated from those modifications.

### In-Scope
- One garment type: basic T-shirt block  
- One pattern format: SVG  
- Core adjustments:
  - Crop hem  
  - Widen or narrow sleeves  
  - Add or remove ease  
  - Adjust neckline depth  
  - Extend or shorten body length  
- Natural-language → structured JSON mapping  
- Deterministic geometry transformations  
- Generation of a **tech pack draft**, including:
  - garment metadata  
  - applied operations  
  - simplified measurement summaries  
- Support for single or simple combined adjustments  

### Out-of-Scope
- Multi-piece garments  
- DXF / AAMA formats  
- Automatic grading  
- Fabric or 3D simulation  
- Real-time editing  
- Batch operations  
- Factory-ready or region-specific tech pack formats  
- Bill of Materials (BOM)  
- Multi-size measurement tables  
- Guarantees that the tech pack draft is production-ready without expert review  

---

## 7. Technical Assumptions

### LLM Interpretation
- LLM generates structured rule JSON only.  
- No direct geometry manipulation by the model.  
- Geometry engine behavior must be deterministic.

### Pattern Format
- SVG is the canonical pattern representation.  
- No raster elements.  
- Transformations must preserve SVG validity.

### Rules Engine
- Explicit numeric instructions only.  
- No conflict resolution in the MVP.

### Geometry Engine
- Pure vector transformations.  
- All changes must be traceable and reversible.  
- Limited to the T-shirt block asset.

### Tech Pack Generator
- Produces a structured JSON draft only.  
- Measurements are simplified and derived from applied rules.  
- Not intended to replace full technical design review.

### Frontend
- Thin client.  
- All processing handled by backend.

### Backend
- Stateless except optional caching.  
- All secrets must be passed through environment variables.

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
Applies structured rules to a base pattern and returns both the modified SVG and a tech pack draft.

**Request**
```json
{
  "pattern_id": "tshirt_block_v1",
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 }
  ]
}
```

**Response**
```json
{
  "modified_pattern_svg": "<svg>...</svg>",
  "techpack": {
    "garment_type": "tshirt",
    "operations_applied": [
      { "operation": "crop_hem", "value_cm": 5 }
    ],
    "measurements": {
      "body_length_change_cm": -5
    },
    "notes": "This is a draft tech pack. Manufacturer review required."
  }
}
```

---

### GET `/patterns/{id}`
Returns pattern SVG assets.

---

### Error Format
```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

---

## 9. Planned Stack Decisions

### Backend
- Python  
- FastAPI  
- `pydantic`, `uvicorn`  

### Frontend
- React  
- Vite  

### LLM Layer
- OpenAI or compatible provider  
- No fine-tuning for MVP  

### Geometry
- SVG-based geometry engine  
- Custom vector math utilities  

### Deployment
- Local or simple cloud environment during MVP  
- CI/CD optional  

---

## 10. Open Questions / Unknowns

### Pattern & Geometry
- Should units be centimeters or pixels?  
- Should transformations occur at path-level or group-level?  
- How should ease be distributed?

### Rules Engine
- Should conflicting rules fail or auto-resolve?  
- Should rules be applied sequentially or merged?

### LLM Interpretation
- How should ambiguous instructions be handled?  
- Should the LLM infer numeric values?

### Tech Pack
- How detailed should the measurement summaries be?  
- Should the tech pack draft be downloadable as HTML/PDF?  
- Should users provide optional metadata (fabric, size, fit notes)?

### Frontend
- Should a before/after preview exist?  
- Should pattern uploading be allowed?

### Backend
- Should patterns be cached or regenerated on each request?

---

## 11. Future Extensions (Not for MVP)

- Multi-piece garment support  
- DXF import/export  
- Automatic grading  
- 3D visualization  
- Full natural-language garment generation  
- Third-party tool integrations  
- Bulk operations  
- Desktop app  
- Real-time previews  

---

## 12. License

```
This repository is private and proprietary.
All rights reserved.
Unauthorized distribution or copying is prohibited.
```
