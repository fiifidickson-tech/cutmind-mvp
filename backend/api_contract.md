# API Contract – CUTMIND MVP

This file defines the backend API contracts for the CUTMIND MVP.  
All endpoints, request formats, and response formats must remain stable until MVP completion.

The contract ensures consistent communication between:
- backend developers  
- frontend developers  
- anyone integrating with the system  

---

# 1. Overview of Endpoints

CUTMIND MVP exposes only **three** API endpoints:

1. `POST /interpret`  
2. `POST /apply-rules`  
3. `GET /patterns/{id}`  

No additional endpoints are allowed during the MVP phase.

---

# 2. POST `/interpret`

## Description
Converts a natural-language prompt into structured rule JSON.

## Request (JSON)
```json
{
  "prompt": "crop the hem by 5 cm and widen the sleeves"
}
```

## Response (JSON)
```json
{
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 },
    { "operation": "widen_sleeve", "value_cm": 3 }
  ]
}
```

## Errors
Returned when:
- rules are missing
- value_cm is missing or not numeric
- operations not supported

```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

---

# 3. POST `/apply-rules`

## Description
Applies validated rules to a selected base SVG pattern (one of the three block families).  
Returns **only** the transformed SVG.

### Valid pattern_id values:
- `"tshirt"`
- `"long_sleeve"`
- `"crop_top"`

## Request (JSON)
```json
{
  "pattern_id": "tshirt",
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 }
  ]
}
```

## Response (JSON)
```json
{
  "modified_pattern_svg": "<svg>...</svg>"
}
```

## Errors
Returned if:
- pattern_id is invalid
- rule structure is invalid
- geometry engine fails

```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

---

# 4. GET `/patterns/{id}`

## Description
Returns the raw base SVG for the requested block family.

### Valid IDs:
- `tshirt`
- `long_sleeve`
- `crop_top`

## Response
This endpoint returns raw SVG, not JSON.

Example:
```
<svg>...</svg>
```

## Errors
```json
{
  "error": "Invalid pattern ID",
  "details": {}
}
```

---

# 5. Unified Error Format

All API errors must follow the same structure:

```json
{
  "error": "Invalid rule format",
  "details": {}
}
```

### `error`
- A stable machine-readable string.
- Never include stack traces or internal info.

### `details`
- Optional explanations such as:
  - `"unsupported_operation"`
  - `"non_numeric_value"`
  - `"missing_field"`
- Should always be an object.

---

# 6. Stability Requirements

- All endpoints, fields, and response shapes must remain unchanged until MVP completion.  
- Any change must update:
  - `api_contract.md`
  - `router.md`
  - `DEVELOPERS.md`
  - `README.md`

Endpoints must remain predictable so frontend, backend, and future engineers can coordinate without ambiguity.
