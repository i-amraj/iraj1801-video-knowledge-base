# Format V2 Toolkit — @i.raj1801 (Raj order, 17 Nov 2026)

Raj ka standing order: har video me in 6 ka use ho — motion, lighting, beats, effects, transitions sab best hon. Frames-cut wali dikkat ka jawab isi stack se aayega (frame-exact engine + physics-based motion).

## Installed (verified 17 Nov 2026)
1. **motion-director skill** — `~/workspace/custom-skills/motion-director/` (SKILL.md, gallery.html, 266 moves, templates). Engine: HyperFrames 0.8.188 (npx cache ready, `--version` verified). **Raj ki pasand: GLASS theme** (themes: glass, glass-folder, studio, product-ui, logo-build, monochrome, retro-print, puppet, safari-collage).
2. **three.js 0.180.0** — `~/workspace/format-v2/toolkit/node_modules` (browser-verified).
3. **awesome-opus5-5-videos** — `~/workspace/format-v2/src/awesome-opus5-5-videos/` (703 prompts, idea library).
4. **Rapier physics** — `@react-three/rapier 2.2.0` + `@react-three/fiber 9.8.2` (React route) AND `@dimforge/rapier3d-compat` (vanilla route, hamari plain three.js pipeline ke liye). Browser test: gravity + collision + resting contact PASS (`toolkit/test/physics.html`).
5. **Postprocessing** — `@react-three/postprocessing 3.2.2` + vanilla `postprocessing 6.39.6` (EffectComposer + Bloom browser-verified). Bloom/DoF/Vignette = lighting finish.
6. **librosa 1.0.1** — ai-video-editor venv (`~/workspace/custom-skills/ai-video-editor/.venv/bin/python`). beat_track + onset_detect verified. Kaam: bg music track → beat-map JSON → scene pops/cuts/SFX beat par.

## Har reel me kaise lagega
- Script → beat-map (librosa, chune hue license-safe track par) + word timings (whisper)
- Motion: physics (rapier) jahan girna/uchhalna/latakna ho; baaki GSAP/motion-director moves
- Lighting/finish: postprocessing Bloom + Vignette (glass theme ke saath khaas)
- Transitions: motion-director/HyperFrames frame-exact renders — koi frame cut nahi
- Music rule wahi: real produced track, har reel fresh, script-matched; SFX sirf Raj ke bundle se

## Paths
- Toolkit: `~/workspace/format-v2/toolkit/` (package.json yahin; node_modules yahin)
- Sources: `~/workspace/format-v2/src/` (motion-director + opus5-5 clones)
- Physics test: `toolkit/test/physics.html` (python http.server + Playwright se chala tha)
