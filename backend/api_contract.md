# api_contract.md

## Purpose
This file defines the backend API contracts for the MVP.  
It ensures engineers clearly understand the expected request/response formats before implementation begins.

The API contract acts as a shared agreement between:
- Backend developers  
- Frontend developers  
- Anyone integrating with the system  

The contract must remain stable during the MVP unless otherwise noted.

---

## POST `/interpret`

### Description
Converts natural-language instructions into structured rule JSON.

### Request (JSON)
```json
{
  "prompt": "crop the hem by 5 cm and widen the sleeves"
}
```

### Response (JSON)
```json
{
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 },
    { "operation": "widen_sleeve", "value_cm": 3 }
  ]
}
```

---

## POST `/apply-rules`

### Description
Applies structured rules to the base SVG pattern and returns both the modified pattern and a tech pack draft.

### Request (JSON)
```json
{
  "pattern_id": "tshirt_block_v1",
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 }
  ]
}
```

### Response (JSON)
```json
{
  "modified_pattern_svg": "<svg>...</svg>",
  "techpack": {
    "garment_type": "tshirt",
    "pattern_id": "tshirt_block_v1",
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

## GET `/patterns/{id}`

### Description
Returns the raw SVG pattern asset.

### Response
- SVG string

Example:
```text
<svg>...</svg>
```

---

## Error Format (Applies to All Endpoints)

```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

---

## Notes
- All API responses must be stable and documented.  
- Any future changes require updating this file.  
- Request/response examples must be kept in sync with backend logic.  
- The tech pack returned by `/apply-rules` is a **draft** and must be reviewed before use in manufacturing.
