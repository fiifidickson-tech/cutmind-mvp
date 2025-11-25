# MVP TECH SPEC — Prompt-Based Pattern Editor
**Version 1.0 – Internal Draft**

# **MVP TECH SPEC — Prompt-Based Pattern Editor**
**Version 1.0 – Internal Draft**

---

# **1. Product Overview**

This MVP allows a user to **edit a sewing pattern using natural language prompts**.

Instead of manually drafting or resizing patterns, the user types prompts such as:

- “Crop the shirt by 14 cm.”
- “Make it slightly oversized with a wider neckline.”
- “Make it boxy.”

The system interprets the text → maps it to a limited set of **predefined pattern operations** → applies geometric transformations → outputs an updated **SVG pattern**.

### **Core Proposition**
> Natural language → Pattern transformation (rule-based)

This differentiates CUTMIND from PatternFast, Tailornova, CLO3D, Illustrator, and other manual tools.

---

# **2. High-Level Architecture**

The MVP consists of **five** main components:

### **1. Web Frontend**
- Prompt input box  
- Pattern preview  
- Summary of interpreted edits  

### **2. Backend API**
- Orchestrates the entire workflow  
- Routes prompt + pattern to LLM and geometry engine  

### **3. LLM Interpretation Service**
- Converts free text → **strict JSON**  
- Selects rule types + numeric values  
- Selects ease bundles  
- Flags unsupported operations  
- *(No geometry performed here)*  

### **4. Rules Engine**
- Validates + sanitizes LLM output  
- Clamps values to safe ranges  
- Applies ease bundles  
- Computes transformation parameters  
- Ensures safe & consistent geometry  

### **5. Pattern Engine**
- Moves points (translation)  
- Adjusts curves  
- Smooths seams  
- Outputs updated **SVG**  
- *Does not modify internal markings (darts, notches, etc.)*  
- *Does not independently redraft sleeves unless included in a preset*  

---

# **3. System Workflow Diagram**



[User]
|
v
[Frontend UI]
|
v
[Backend API]
|
+--> [LLM Interpretation Service] ----+
| |
| Structured JSON (rules + values)
| v
+--> [Rules Engine] ---------------> [Pattern Engine]
|
v
Updated SVG Pattern
|
v
[Frontend UI]


---

# **4. LLM Output Format (Strict JSON)**

The LLM must return JSON using **only predefined rule names**:

```json
{
  "fit_preset": "cropped_boxy",
  "operations": [
    { "rule": "change_hem_length", "amount": -14, "unit": "cm" },
    { "rule": "change_shoulder_width", "amount": 1, "unit": "cm" },
    { "rule": "change_neckline_width", "amount": 1.5, "unit": "cm" }
  ],
  "unsupported_requests": [
    "add ruffles",
    "make it backless"
  ]
}


The LLM is not allowed to invent new rule names.

5. Supported Rule Set (MVP v1)

These are the only valid operations for V1.

Pattern Transformation Rules

change_hem_length

change_sleeve_length

change_shoulder_width

change_neckline_width

change_neckline_depth

adjust_armhole_depth

apply_fit_preset

Ease Presets (10 Bundles)

Skin-tight

Tailored/Fitted

Standard fit

Relaxed fit

Classic Boxy

Oversized

Super Oversized

Cropped Fitted

Cropped Boxy

Athleisure

6. Rules Engine Logic
Responsibilities

Validate LLM-generated instructions

Normalize units

Clamp unsafe values

Apply ease bundle rules

Compute final parameters

Maintain geometric stability

Prevent impossible shapes (e.g., negative armholes)

Example Pseudocode
function validate(instructions) {
    preset = instructions.fit_preset;
    ops = instructions.operations;

    // 1. Apply ease preset
    ease = EaseBundles[preset || "standard"];

    // 2. Normalize units to cm
    for (op of ops) {
        op.amount = convertToCm(op.amount);
    }

    // 3. Safety clamps
    for (op of ops) {
        if (op.rule === "change_hem_length") {
            op.amount = clamp(op.amount, -25, 25);
        }
    }

    return { ease, ops };
}

7. Pattern Engine Logic (Geometry)

The T-shirt block is represented using:

Named landmarks

SVG paths

Metadata for:

hem

armhole

side seam

neckline

shoulder

Example: change_hem_length
for (piece of [front, back]) {
    for (point of piece.hem_line) {
        point.y -= amount_cm;
    }
    blendLowerSideSeam(piece.side_seam, newHemPosition);
}

Example: change_shoulder_width
for (piece of [front, back]) {
    for (point of piece.shoulder_line) {
        point.x += amount_cm / 2;
    }
    smoothCurve(piece.armhole_curve);
}

Output

Updated SVG file

(PDF optional in future versions)

Grainlines & notches preserved

8. User Flow (Frontend)

User selects base T-shirt pattern

User types a prompt

LLM produces a structured summary

Backend updates pattern

User previews or downloads the new SVG

User optionally applies more edits

9. Engineering Constraints (MVP Reality Check)

Only 1 garment (T-shirt block)

Only 6–8 rule types

Only SVG output required

No generative geometry

No grading

No 3D simulation

No multi-garment dependencies

Expected dev time:
8–12 weeks with 1–2 engineers.

10. Summary — Why This MVP Is Feasible
✔ AI handles interpretation, not geometry
✔ Geometry engine is rule-based and deterministic
✔ Narrow scope = predictable engineering
✔ Single-garment support massively reduces complexity
✔ Existing formats (SVG) require no new standards
✔ V1 focuses on stability over visual fidelity

This MVP proves the core differentiator of CUTMIND:

AI-powered natural-language editing of sewing patterns.
