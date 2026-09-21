---
name: cognitive-warfare-manim-pitch
description: Create, refine, render, and validate an evidence-bound scientific pitch about cognitive warfare or cognitive influence technologies. Use whenever the user is preparing the Victory Neurones CIT final project, a three-minute cognitive-warfare presentation, a 10-page PDF pitch, or scientific slide visuals that should be produced with Manim Community Edition. This skill is Manim-first, timing-constrained, defensive/public-safe, and designed for research credibility rather than generic fundraising.
compatibility: Requires Manim Community Edition, Python, a PDF assembly workflow, and a PDF renderer for visual QA.
---

# Cognitive Warfare Manim Pitch

Build a concise scientific argument that can survive expert questions. Treat slides as visual evidence and the speaker as the narrative channel.

## Fixed contract

- Deliver exactly 10 pages as a PDF.
- Fit the complete spoken pitch, transitions, and pauses inside 180 seconds.
- Target 165–175 seconds during rehearsal to preserve a small live-delivery margin.
- Use Ukrainian unless the user requests another language.
- Use Manim Community Edition (`from manim import *`), never ManimGL syntax.
- Do not impose a fundraising deck or fixed slide sequence. The user will provide the final structure.

Read [references/research-and-visual-standard.md](references/research-and-visual-standard.md) before researching or drawing. Use [templates/slide-plan.md](templates/slide-plan.md) when the project structure becomes available.

## Workflow

### 1. Lock the brief

Record the audience, decision sought, project maturity, allowed disclosure level, central claim, evidence available, and success criteria. Preserve unresolved items as explicit placeholders. Do not invent traction, market size, outcomes, partners, or classified context.

### 2. Build an evidence ledger

Use the installed research stack for discovery, then verify decisive claims with primary or authoritative sources. For each claim record: wording, source, date, evidence type, limitation, confidence, and destination page. Prefer official doctrine/standards and peer-reviewed work; label preprints, estimates, simulations, and project hypotheses.

### 3. Design the narrative

Translate the user-approved structure into ten page-level claims. For each page specify the audience question, one-sentence answer, evidence, visual, spoken line, transition, and seconds. The total must not exceed the rehearsal target. Remove material before shrinking type or accelerating speech.

### 4. Design Manim assets

Choose visuals that expose mechanism rather than decorate:

- causal graphs for influence pathways and confounders;
- network diagrams for actors, channels, and propagation;
- timelines for intervention and response;
- state-space or feedback-loop diagrams for resilience;
- plots for measured data with units, uncertainty, and sample size;
- equations only when the speaker explains every symbol.

Create one scene per reusable visual. Use a shared palette, typography, stroke widths, margins, and 16:9 coordinate system. Use deterministic seeds. Add concise source labels in the slide composition, not inside dense data marks.

Render rough animations at low quality for review. Render final PDF assets as high-quality stills at the decisive state; the official CLI supports `-s`/`--save_last_frame`. Use:

```powershell
python "$SKILL_PATH/scripts/render_manim_assets.py" src/manim/scenes.py --scene ThreatModel --mode still --quality high --media-dir assets/generated
```

If `manim` is not on `PATH`, pass its executable with `--manim`. Do not install or upgrade Manim without approval.

### 5. Assemble and verify

Assemble the ten pages to PDF, render the PDF back to images, and inspect the complete deck and a thumbnail grid. Check page count, 16:9 geometry, hierarchy, contrast, clipping, citation readability, factual consistency, and visual continuity. Review each Manim visual against its underlying evidence.

### 6. Rehearse against the timer

Run at least three timed rehearsals. Log actual duration per page and total duration. Tighten the spoken script rather than rushing. Prepare a one-sentence answer for the strongest likely objection and the most important limitation.

## Quality gates

Do not finalize until all are true:

- Every substantive claim is sourced, measured, or explicitly labeled as a hypothesis.
- Every chart preserves scale, units, denominator, uncertainty, and provenance.
- The PDF has exactly 10 pages and the rehearsed delivery stays under 180 seconds.
- Every page communicates one claim at presentation distance.
- Manim source and rendered assets are reproducible.
- The deck avoids operational targeting guidance, fabricated precision, and “AI truth detector” claims.

## Output package

Return the PDF, timed script, slide plan, evidence ledger, Manim source, rendered assets, and a short validation report. Clearly identify any remaining placeholders or unverified claims.
