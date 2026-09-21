# Manim implementation and review

Check the installed Manim Community version and use its [official documentation](https://docs.manim.community/en/stable/) for current APIs. The older local recipes pinned colors, fonts, frame rates, and scene classes without testing them; these are production choices, not teaching invariants.

- Use the [text and formula guide](https://docs.manim.community/en/stable/guides/using_text.html) for Ukrainian or other non-English labels. Render a short sample before building the whole scene; installed fonts and glyph support vary.
- Use `ValueTracker` and `always_redraw` only when a continuously changing value teaches the mechanism. A direct transform is often easier to follow. Reuse an object across changes when its identity matters.
- Camera-frame animations require a scene/camera class that supports them; confirm the [camera API](https://docs.manim.community/en/stable/reference/manim.scene.moving_camera_scene.MovingCameraScene.html) before using `self.camera.frame`.
- For a quick preview, use the official [output settings](https://docs.manim.community/en/stable/tutorials/output_and_config.html): `manim -ql scene.py SceneName`. For a final high-quality render, use `manim -qh scene.py SceneName`, subject to the user's size and time constraints. `-s` produces a last-frame image, not a video. Do not assume `-qh` has a fixed frame rate across versions or configuration.

After rendering, inspect the opening, the mechanism reveal, the first formula or label, and the final prediction beat. Check readability at the actual delivery size, causal direction, correspondence between colors and quantities, clipping, and audio alignment if narration was requested. Verify the output file opens and has the intended duration. Keep scene code editable and record any approximation or illustrative input in the storyboard or narration.
