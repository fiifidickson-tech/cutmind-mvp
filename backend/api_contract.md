# API Contract – CUTMIND MVP

This file defines the backend API contracts for the CUTMIND MVP.  
All endpoints, request formats, and response formats must remain stable until MVP completion.

The contract ensures consistent communication between:
- backend developers  
- frontend developers  
- future engineers  
- third-party integrations  

---

# 1. Overview of Endpoints

CUTMIND MVP exposes exactly **three** backend endpoints:

1. `POST /interpret`  
2. `POST /apply-rules`  
3. `GET /patterns/{id}`  

No additional endpoints are allowed during the MVP phase.

---

# 2. POST `/interpret`

## Description
Parses a natural-language prompt and turns it into a validated list of structured rules.

## Request (JSON)
```json
{
  "prompt": "crop the hem by 5 cm and widen the sleeves"
}
```

## Successful Response (JSON)
```json
{
  "rules": [
    { "operation": "crop_hem", "value_cm": 5 },
    { "operation": "widen_sleeve", "value_cm": 3 }
  ]
}
```

## Error Response (JSON)
Returned when:
- the prompt cannot be interpreted
- a rule is malformed
- the model returns something unstructured

```json
{
  "error": "unsupported_instruction",
  "details": {}
}
```

Common error codes: `"unsupported_instruction"`, `"invalid_rule_format"`, `"internal_error"`.

---

# 3. POST `/apply-rules`

## Description
Applies validated rules to ONE of the three supported base block families.  
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

## Successful Response (JSON)
```json
{
  "modified_pattern_svg": "<svg>...</svg>"
}
```

## Error Response (JSON)
Returned if:
- pattern_id is invalid  
- a rule is malformed  
- the geometry engine cannot apply the rule  

```json
{
  "error": "invalid_rule_format",
  "details": {}
}
```

Common error codes: `"invalid_pattern_id"`, `"invalid_rule_format"`,
`"geometry_application_failed"`, `"internal_error"`.

---

# 4. GET `/patterns/{id}`

## Description
Returns the **raw** base SVG for a pattern block family.

### Valid IDs:
- `tshirt`
- `long_sleeve`
- `crop_top`

## Successful Response
Raw SVG, **not JSON**:

```
<svg>...</svg>
```

## Error Response (JSON)
```json
{
  "error": "invalid_pattern_id",
  "details": {}
}
```

---

# 5. Unified Error Format

ALL endpoints must return errors with this structure:

```json
{
  "error": "some_error_code",
  "details": {}
}
```

Typical error codes (shared with `mvp_spec.md`):
- "`unsupported_instruction`"
- "`invalid_rule_format`"
- "`invalid_pattern_id`"
- "`geometry_application_failed`"
- "`internal_error`"

### Rules:
- `"error"` must always be a short machine-readable string.  
- `"details"` must always be an object.  
- Never return Python stack traces.  
- Never return raw LLM output on error.

---

# 6. Stability Requirements

The following files MUST be updated whenever API behavior changes:
- `api_contract.md`
- `router.md`
- `DEVELOPERS.md`
- `README.md`

The API must remain predictable so frontend, backend, and future engineers can coordinate without ambiguity.
