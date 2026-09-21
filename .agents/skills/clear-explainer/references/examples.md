# Worked examples and failure checks

Use these examples to calibrate mechanism, notation, and analogy. Do not copy their wording into unrelated answers.

## Mathematics: eigenvector

For the transformation that doubles horizontal distances and leaves vertical distances unchanged, a horizontal arrow stays horizontal and doubles in length; a vertical arrow stays vertical and keeps its length. A diagonal arrow usually changes direction. The arrows that keep their line are **eigenvectors**; the length/sign change is their **eigenvalue**. Formally, `Av = λv` for a nonzero vector `v`. A rubber-sheet picture can show stretching, but it may mislead for negative eigenvalues, rotations with no real eigenvectors, or complex vectors. Do not claim that every diagonal arrow is an eigenvector for every stretch.

A transfer check: if horizontal distances triple instead of double, which arrows keep their direction, and what changes in their eigenvalues?

## Software: race condition

Two workers each read a shared balance of 100, each add 10, and each write 110. The final balance is 110 although two additions should yield 120. The outcome depends on the order of overlapping reads and writes: that is a **race condition**. Two clerks editing one paper ledger is a useful analogy, but computers may interleave smaller operations than a human can see. A lock or atomic update changes which interleavings are allowed; name the exact mechanism being used.

A transfer check: what if one worker finishes its write before the second worker reads the balance?

## When a picture is dishonest

“Electrons orbit a nucleus like planets” supplies a familiar picture but predicts definite paths and classical behavior. For quantum questions, say what the model captures, identify the false prediction, and move to a measured or probabilistic description. If the requested idea cannot be faithfully represented by a household object, use a comparison between experiments instead of forcing a metaphor.
