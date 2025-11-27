# CUTMIND Frontend (MVP)

The frontend for the CUTMIND MVP is intentionally minimal.  
Its goal is to demonstrate the core flow:

1. User enters a natural-language prompt.
2. Frontend calls `POST /interpret` to get structured rules.
3. Frontend calls `POST /apply-rules` with:
   - `pattern_id` (tshirt, long_sleeve, or crop_top)
   - the rules returned from `/interpret`
4. Frontend displays the returned `modified_pattern_svg` in an SVG preview area.

## MVP UI Requirements

- Text input for the prompt.
- Dropdown or buttons for `pattern_id`:
  - `tshirt`
  - `long_sleeve`
  - `crop_top`
- Button: "Generate Rules" → calls `/interpret`.
- Button: "Apply Rules" → calls `/apply-rules`.
- SVG preview region that renders the returned `<svg>...</svg>` string.

## Out of Scope (MVP)

- Tech pack generation.
- Authentication.
- Saving projects or versions.
- Multi-garment library.
- 3D or draping visualization.

## API Endpoints Used

The frontend must only call:

- `POST /interpret`
- `POST /apply-rules`
- `GET /patterns/{id}` (optional, for showing the base pattern)
