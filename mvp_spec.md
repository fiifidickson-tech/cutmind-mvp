# CUTMIND MVP Specification

This document specifies the requirements, rules, and behavior for the CUTMIND MVP.  
The MVP supports **three garment block families** (tshirt, long_sleeve, crop_top) and enables natural-language adjustments that are translated into structured operations and applied to SVG pattern files.

No tech pack generation is included in this MVP.

---

# 1. MVP Goals

The MVP aims to validate:

1. Whether natural-language garment modification instructions can be reliably converted into structured rule JSON.
2. Whether those rules can be applied deterministically to SVG pattern pieces.
3. Whether the system works consistently across **three base garment blocks**.
4. Whether the architecture scales toward multi-garment support post-MVP.

---

# 2. Supported Garment Blocks

The MVP includes **three block families**, each with the same 3-piece structure:

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

Each SVG must:

- Use clean paths/groups.
- Maintain consistent naming across blocks (e.g., `<g id="front">`).
- Follow the same structural logic so geometry transforms can be reused.

---

# 3. In-Scope Adjustments

The MVP supports simple, numeric, deterministic adjustments.  
All adjustments apply identically across the 3 block families.

## 3.1 Body Adjustments
- **crop_hem** (negative length change)
- **extend_hem** (positive length change)
- **adjust_body_length** (generalized version, in cm)
- **add_ease_body**
- **remove_ease_body**

## 3.2 Sleeve Adjustments
- **widen_sleeve**
- **narrow_sleeve**
- **shorten_sleeve**
- **extend_sleeve**
- **add_ease_sleeve**

## 3.3 Neckline Adjustments
- **raise_neckline**
- **lower_neckline**

## 3.4 Combined Adjustments
The system may process prompts such as:

- “Crop the hem by 5 cm and widen the sleeves.”
- “Lower the neckline by 2 cm and add 3 cm of ease to the chest.”

Combined adjustments must simply run sequentially.

---

# 4. Natural-Language → Rule Mapping

The LLM is responsible only for generating **structured rule JSON**.

## 4.1 Rule Format

```json
{
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 },
    { "operation": "widen_sleeve", "value_cm": 3 }
  ]
}
```

### Rules Must Include:
- `"operation"` — one of the allowed MVP operations  
- `"value_cm"` — numeric value in centimeters (integer or float)

### Out-of-Scope
- Multi-operation inference (ex: “make it drapey”)
- Style interpretation (ex: “boxy fit”)
- Custom grading
- Size generation

The LLM should respond “unsupported_instruction” (via error) if an instruction is not in-scope.

---

# 5. Rules Engine Specification

The rules engine receives:
- `pattern_id` ("tshirt", "long_sleeve", or "crop_top")
- `rules[]`

It must:
1. Validate rule names.
2. Validate numeric values.
3. Apply rules **sequentially**.
4. Return the transformed SVG.

## 5.1 Validation Errors
Return unified error:
```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

---

# 6. Geometry Engine Specification

The geometry engine transforms SVG paths/groups through vector math.

### Responsibilities:
- Load base SVG for chosen pattern.
- Apply transformations such as:
  - vertical shortening (crop hem)
  - horizontal widening (ease)
  - sleeve adjustments
  - neckline adjustments
- Ensure output remains valid SVG.
- Maintain consistent coordinate-space logic across all blocks.

### Out of Scope:
- Mesh deformation  
- 3D draping  
- Group-level intelligent transformations  
- Visual “smoothing”  
- Multi-size support  

---

# 7. API Specification

## 7.1 POST `/interpret`
Generates rule JSON.

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

## 7.2 POST `/apply-rules`
Applies rule JSON to a chosen pattern.

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
  "modified_pattern_svg": "<svg>...</svg>"
}
```

---

## 7.3 GET `/patterns/{id}`
Returns the raw base SVG pattern.

Valid IDs:
- tshirt
- long_sleeve
- crop_top

---

# 8. System Constraints

- Deterministic transformations only  
- No stochastic geometry behavior  
- All rules must be numerically defined  
- LLM must not directly generate SVG  
- All transformations must be reversible in theory  

---

# 9. Architecture Requirements

### 9.1 Backend
- Python  
- FastAPI  
- Stateless  
- One endpoint per major function  

### 9.2 Frontend
- Minimal UI  
- Simple form input + SVG preview  
- No need for authentication  

### 9.3 Config
- All operation mappings stored in `prompt_mapping.json`

---

# 10. Error Handling

All endpoints must return:
```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

Errors include:
- Missing fields  
- Unsupported operations  
- Non-numeric values  
- Invalid pattern IDs  
- LLM interpretation failures  

---

# 11. Future Extensions (Post-MVP)

Not part of MVP, but foundational architecture must allow:

- Additional block families  
- Multi-piece garments (hoodies, jackets, pants)  
- Automatic grading  
- Tech pack generation  
- PDF/DXF export  
- Real-time pattern editing  
- 3D visualization  

---

# 12. Approval

This spec defines the complete scope for the MVP.

No additional features should be added until blocks, rule engine, and geometry engine are functional.
