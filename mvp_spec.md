# CUTMIND – MVP Specification

This document defines the requirements, technical boundaries, and acceptance criteria for the CUTMIND MVP. It serves as the single source of truth for engineers and contributors during early implementation.

The goal of the MVP is to validate two core capabilities:

1. **Interpret natural-language garment adjustments into structured rules**
2. **Apply those rules to a base SVG pattern and generate a tech pack draft**

The system is not intended to be production-ready or support all garment types at this stage. The focus is correctness, determinism, and demonstrating end-to-end functionality.

---

## 1. Problem Overview

Pattern-making is complex, slow, and often inaccessible to new designers and entrepreneurs. Even small changes (e.g., “crop the hem by 5 cm,” “widen the sleeves”) require technical skill or paid specialists.

Manufacturers also require **tech packs**, which further slows down sampling, increases communication overhead, and creates waste during prototyping.

The MVP solves this by enabling users to:

- Describe adjustments in **plain language**
- Receive a **modified pattern** (SVG)
- Receive a **tech pack draft** summarizing the applied changes

This empowers:

- Early-stage clothing founders  
- Non-technical designers  
- Even experienced CLO3D or pattern-making users who want faster iteration  

---

## 2. MVP Goals

### Primary Goals
- Convert natural-language instructions into structured rules  
- Apply those rules to a base T-shirt pattern (SVG)  
- Generate a **tech pack draft** including:
  - garment metadata  
  - list of applied operations  
  - simplified measurement summaries  
  - optional notes  

### Secondary Goals
- Expose a simple API for both frontend and external integration  
- Provide a minimal frontend to test natural-language → output behavior  
- Maintain deterministic behavior for identical inputs  

---

## 3. In-Scope

The MVP includes:

### Base Asset
- One garment type: **basic T-shirt block**
- One file format: **SVG**

### Supported Adjustments
- Crop hem  
- Extend/shorten body length  
- Widen or narrow sleeves  
- Add or remove ease  
- Adjust neckline depth  

### Natural-Language → Rule Mapping
- LLM converts text prompts into structured JSON rules  
- No direct geometry manipulation by the model  

### Geometry Engine
- Deterministic vector-based SVG transformations  
- Path-level adjustments  
- Output must remain valid SVG  

### Tech Pack Draft Generation
- JSON structure including:
  - garment type  
  - operations applied  
  - simplified measurement calculations  
  - optional notes  
- Intended as a **draft**, not a manufacturing-complete document  

### API Endpoints
- `/interpret`  
- `/apply-rules` (returns pattern + techpack)  
- `/patterns/{id}`  

### Frontend (Minimal)
- Input field for prompt  
- Display of modified pattern  
- Display of tech pack draft  

---

## 4. Out-of-Scope

These are explicitly excluded from the MVP:

### Garment Complexity
- Multi-piece garments  
- Pants, jackets, dresses, etc.  
- DXF / AAMA formats  

### Tech Pack Depth
- Factory-ready formats  
- Bill of Materials (BOM)  
- Stitch type specifications  
- Grading / multi-size measurement tables  
- Fabric performance constraints  

### System Behavior
- Conflict resolution between multiple rules  
- Real-time editing  
- 3D visualization  
- Batch operations  
- Full measurement validation  

---

## 5. User Stories

### Story 1 — Founder Creating First Garment
“As a founder, I want to describe how I want a shirt to fit in plain language so I can get a pattern and tech pack draft I can send to a manufacturer.”

### Story 2 — Designer Rapid Iteration
“As a designer, I want to quickly adjust a base pattern and view the updated measurements without redoing work manually.”

### Story 3 — Technical User Testing Changes
“As a CLO3D or pattern-making user, I want a fast way to generate pattern variations from prompts.”

---

## 6. High-Level Workflow

1. User selects the base T-shirt pattern  
2. User enters natural-language instructions  
3. Backend LLM interprets the prompt  
4. Rules engine validates and structures rule outputs  
5. Geometry engine applies rules to SVG  
6. System calculates simplified measurements  
7. **Tech pack generator creates a draft**  
8. Backend returns:
   - modified SVG  
   - tech pack draft JSON  

---

## 7. Functional Requirements

### 7.1 Natural-Language Interpretation
The system must:
- Accept a text prompt  
- Return structured rules with numeric values  
- Handle combined operations (e.g., “crop 5 cm and widen sleeves 3 cm”)  

### 7.2 Rule Validation
The system must:
- Validate that each rule is supported  
- Reject unsupported operations  
- Ensure numeric values are present  

### 7.3 Geometry Engine
The engine must:
- Apply rule transformations to the SVG  
- Produce a valid SVG output  
- Remain deterministic  

### 7.4 Tech Pack Draft Generator
The system must:
- Convert applied rules into structured metadata  
- Calculate simplified measurement changes  
- Output JSON in a consistent schema  
- Indicate clearly that it is a **draft** requiring review  

### 7.5 API Layer
- All endpoints must return JSON  
- Errors must follow the standardized format  

---

## 8. API Requirements

### `/interpret`
- Input: text prompt  
- Output: structured rule JSON  

### `/apply-rules`
- Input: pattern ID + rules  
- Output:
  - modified SVG  
  - tech pack JSON  

### `/patterns/{id}`
- Returns base patterns  

### Error Format
```json
{
  "error": "string",
  "details": {}
}
```

---

## 9. Tech Pack Draft Specification

### Required Fields
```json
{
  "garment_type": "tshirt",
  "operations_applied": [],
  "measurements": {},
  "notes": "string or null"
}
```

### Measurement Rules
Examples:
- Cropping hem by 5 cm → body length reduction  
- Sleeve widening → updated sleeve width summary  

### Notes
- No grading  
- No BOM  
- No fabric requirements  
- No production tolerances  

---

## 10. Non-Functional Requirements

### Determinism
- Same input → same output every time  

### Performance
- MVP acceptable: < 3 seconds per request  

### Reliability
- API must not crash on malformed instructions  
- All errors must be descriptive and consistent  

### Maintainability
- Code must be modular:  
  - rules engine  
  - geometry engine  
  - tech pack generator  
  - LLM interpretation layer  

---

## 11. Open Questions

### Pattern
- Should measurements be stored or computed on the fly?  

### Tech Pack
- Should we allow user metadata (fabric, fit notes)?  
- Should we support exporting drafts to HTML/PDF?

### Rules
- Should combined operations be sequential or merged?

### Future
- Should users upload their own base patterns?

---

## 12. Future Extensions (Not for MVP)

- Multi-piece garment support  
- DXF import/export  
- Full tech pack generator with BOM + grading  
- Real-time editing interface  
- Fabric-aware adjustments  
- Full LLM garment creation model  
- 3D viewer  
- Design assistant mode  

---

## 13. Acceptance Criteria

The MVP is considered complete when:

- A user inputs natural-language adjustments  
- `/interpret` returns valid structured rules  
- `/apply-rules` returns:
  - a modified SVG  
  - a valid tech pack JSON with measurement changes  
- The modified SVG reflects the rule inputs deterministically  
- The tech pack draft follows the defined schema  
- The frontend can display:
  - input field  
  - resulting SVG  
  - resulting tech pack JSON  
- All out-of-scope features are clearly excluded  

---

## 14. Versioning

This MVP spec is v0.1.  
Any future changes must be documented and versioned.

