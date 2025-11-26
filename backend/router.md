# router.md

## Purpose
This file will outline how backend routing is organized.

It will document:
- The directory structure for route files (if any)
- How routes are imported/registered in `server.py`
- Naming conventions for endpoints
- Guidelines for separating logic into route modules
- Future expansion to additional route groups (e.g., `/patterns`, `/rules`, `/debug`)

## MVP Routing Structure (Planned)

### POST `/interpret`
- Converts natural-language input into structure rules JSON.

### POST   `/apply-rules`
- Applies structured rules to the base SVG pattern.

More detailed routing rules will be defined once implementation begins.
