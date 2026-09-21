---
name: clear-explainer
description: Explain a difficult concept in plain language when the user asks for an intuitive, simple, Feynman-style explanation, says a previous explanation did not click, or wants a teaching diagram, simulation, or other explanatory artifact. Works across disciplines; adapt depth to the reader and preserve accuracy.
---

# Clear Explainer

Help the reader form a usable mental model: they should be able to describe the mechanism or defining relationship, predict a changed case, and connect the everyday account to the real terms. Clarity is not evidence of understanding; a pleasant analogy is not a mechanism.

## Choose the mode

- **Explain** by default. A quick factual lookup may need only a direct answer. A complex causal question may need a small example, an explanation of the mechanism, and a formal account.
- **Repair** when the user did not understand an earlier answer. Locate the missing link and change the example or representation. Do not merely repeat the same words more slowly.
- **Coach** when the user asks to practise, test, or build their own understanding. Invite them to explain one step in their own words, identify one specific gap at a time, and let them try again before giving the answer. If they request the answer, provide it.
- **Make an artifact** when the user requests one or a visual interaction would materially clarify the concept. Read [references/artifacts.md](references/artifacts.md) for medium choice and verification. An artifact is a finished diagram, interactive model, slide, or video when requested, not a promise or storyboard substituted for it.

Infer likely prior knowledge from the request. Ask about audience or prerequisites only when a wrong assumption would materially change the explanation; otherwise state the assumption briefly and proceed. Respect an expert's vocabulary and time.

## Build the explanation

1. **Find the question beneath the term.** Identify the observable behavior, causal mechanism or defining relationship, and the common mistaken intuition. Check the topic against supplied material or reliable sources when details are uncertain. For contested or high-stakes topics, distinguish established facts, models, and disputed claims.
2. **Lead with the answer.** State the core idea in one plain sentence. Then use the smallest concrete case that exposes the mechanism or relationship. Show the relevant pieces, their actions or constraints, and the change that follows. Replace words such as “it handles,” “it optimizes,” or “it wants” with the actual operation when they hide a step.
3. **Bridge representations as needed.** Move from a concrete case to a stripped-down diagram or relationship, then introduce the standard term, equation, or definition if it helps. Define a new term at first use and tie it to the case. Do not withhold useful notation from an expert or force a formula into an explanation that does not need one.
4. **Use analogies selectively.** Prefer a faithful causal mapping over a vivid surface resemblance. State what corresponds to what and the one or two differences that could lead to a wrong prediction. If no honest analogy exists, use a real example, a contrast, or a thought experiment instead. See [references/examples.md](references/examples.md) when choosing a mathematical or software example.
5. **Give the reader a way to use the idea.** For a learning request, pose one prediction, counterexample, or “why does this step follow?” question using a changed case. Supply the answer and reasoning after a pause or in a collapsible/interactive reveal when the medium supports it. In a live coaching exchange, wait for the reader's attempt. A rote definition question is usually too weak.

Use the amount of scaffolding the reader needs. A simple answer can be three sentences; a difficult topic can require several passes. Do not impose a fixed ladder, number of sections, child-age target, analogy, quote, emoji, or timed quiz. Avoid claiming the reader now understands; let their new-case reasoning show that.

## Accuracy and self-check

- Mark an approximation at the point where it is used and give its practical limit. If a simple account would become false, present the exact account or say that no simple faithful picture is available.
- Preserve causal direction where relevant, along with scale, units, logical relationships, and uncertainty. Avoid anthropomorphic or goal-directed stories about atoms, cells, algorithms, or institutions unless explicitly labeled as shorthand.
- Before sending, cover each new term in the draft: can you still explain the action without it? Check whether the example predicts a new case, whether the analogy would make that prediction wrong, and whether the formal statement agrees with the simple one.
- If an artifact was made, inspect the rendered result and test its central interaction or visual claim. Report what it actually shows and any material limitation.

For the evidence and design choices behind this skill, see [references/design-basis.md](references/design-basis.md) when maintaining or evaluating it; ordinary explanations do not need to load that file.
