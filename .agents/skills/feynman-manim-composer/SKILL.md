---
name: feynman-manim-composer
description: Plan or produce a Manim explanation when the user asks for a science or mathematics storyboard, narrated teaching animation, Manim code, or rendered video. Turn the core mechanism into aligned voice and visual scenes; deliver the requested artifact and verify any render.
---

# Feynman Manim Composer

Turn a clear causal explanation into scenes the viewer can follow. The animation should reveal the mechanism, not decorate a lecture. Use the local `clear-explainer` skill to repair the underlying explanation when the idea is still vague; do not substitute the storyboard for an explicitly requested video.

## Decide the deliverable

- **Storyboard or `scenes.md` requested:** deliver an editable scene plan with narration, visual action, pedagogical purpose, and approximate timing.
- **Manim code requested:** deliver runnable scene code, with the storyboard embedded in comments or a short companion plan when useful. Check the installed Manim version and relevant official API documentation.
- **Animation or video requested:** produce the code, render the requested output, inspect representative frames and playback, and deliver the actual file. If the runtime is unavailable, identify the missing dependency precisely and complete the scene plan and code that can be prepared locally.

Infer audience, prerequisites, duration, language, and format from the request. Ask only when a missing choice materially changes the lesson. Use a reasonable default for routine production choices and state it in the artifact.

## Compose the lesson

1. Confirm the scientific or mathematical account from supplied material or reliable sources. Mark invented numbers, motion, or situations as illustrative rather than measured. Write one sentence describing what the viewer should be able to predict after watching. Identify the likely wrong intuition and the visual event that can correct it.
2. Choose a small number of scenes according to the concept, not a fixed six-scene sequence. A scene may introduce a question, show a concrete case, strip it down to a diagram, test a changed case, or connect the visible behavior to notation. Include a scene only if it advances understanding.
3. For each scene, align narration with what is visible at that moment. Show a cause before or while naming its effect. Reuse visual objects and colors for the same quantities; reveal new labels only when they are needed. Mark where an analogy fails if its visual form could produce a false prediction.
4. Keep equations as records of relationships the viewer has already seen, when useful. Give enough time to read each change. Prefer a genuine prediction pause or learner challenge over a congratulatory quiz or a claim that the viewer now understands.
5. Use [references/scenes-template.md](references/scenes-template.md) when a storyboard file is useful. Use [references/manim-visual-patterns.md](references/manim-visual-patterns.md) when implementing or rendering. Neither reference requires a fixed palette, voice provider, number of scenes, or duration.

## Verify

For a storyboard, check that the example, narration, animation, and final statement agree, and that the timed beats fit the target duration. For code or video, check that it runs in the available environment, labels remain readable, no object is clipped or obscured, transitions preserve object identity, and any spoken timing matches the visual event. Inspect the requested file before claiming completion.

State clearly whether the result is a storyboard, code, preview render, or finished video. Include the editable source and the rendered artifact when both were requested.
