---
name: gsap-motion
description: "GSAP animation for VIDEO production — timelines, eases, camera-feel moves, text/element animation inside HTML/canvas compositions (HyperFrames, standalone player.html renders, Remotion HTML layers). Use whenever a scene feels static, cuts feel dead, or text/props need performed motion instead of plain fades. Deterministic, seek-driven animation only — built for frame-by-frame rendering on this VM."
---

# GSAP Motion — for rendered video

GSAP is the motion engine under HyperFrames and the easiest way to make HTML/canvas
scenes feel filmed instead of slid. Use it for: camera-feel moves (push-in, pan,
tracking), character/prop performance, text beats, seam transitions between scenes.

## Hard rules for render work

1. **Seek-driven, never wall-clock.** Build ONE master timeline per scene; render by
   `tl.seek(t)` per frame. No `requestAnimationFrame` free-running, no `Date.now()`
   in animation logic — a render must be reproducible frame-for-frame.
2. **Camera never sleeps.** If a shot lasts >1.5s, something with intent moves the
   whole time: slow push-in (scale 1→1.06), drift pan, or a tracked follow. Static
   frames are for <0.5s beats and the stillness-before-climax moment only.
3. **Eases carry emotion.** Defaults: entrances `power3.out`, exits `power2.in`,
   playful pops `back.out(1.7)`, heavy/sad moves `power1.inOut` and slow. Never
   `linear` except for mechanical motion (conveyor, gears) — and never the same
   duration for every element.
4. **Exit vector = entry vector.** What leaves moving left enters the next scene
   still moving left (see `motion-doctrine` — it supersedes this skill on seams).
5. **Animate transforms and opacity only** (x/y/scale/rotation) — layout properties
   (width/height/top) stutter in headless renders.

## Core patterns

- **Master timeline per scene:**
  `const tl = gsap.timeline({ paused: true, defaults: { ease: "power3.out" } });`
  then position tweens with labels (`tl.add("beat2", 1.2)`), never chained delays.
- **Push-in:** `tl.to(".cam", { scale: 1.07, duration: dur, ease: "power1.inOut" }, 0)`
  on a wrapper, with `transformOrigin` set to the subject — the cheapest cinematic move.
- **Waterfall entry:** stagger 0.06–0.09s for grouped elements (see `cut-the-curve` §6).
- **Text beats:** words/lines rise+fade (`y: 24 → 0, opacity 0 → 1`), keyword pops
  `scale 0.8 → 1, back.out(2)`. Captions still follow `captions-overlay` rules.
- **Anticipation + follow-through:** before a jump/move, a 0.1–0.15s squash or
  pull-back; after landing, a 0.1s settle overshoot. This one habit separates
  "animated" from "alive".
- **Shake (sparingly):** 2–3 keyframe x/y jitters over 0.2s for impacts only.

## Where it plugs in

- **HyperFrames comps:** GSAP is native — timelines live in the comp; still obey
  `motion-doctrine` + `seam-craft` gates.
- **GrowKaz studio / player.html renders:** load GSAP from the local bundle or CDN
  at build time, drive by seek in the frame loop; verify with frame grabs at
  0% / 50% / 100% of each scene before a full render.
- **Remotion:** prefer Remotion's own `interpolate/spring` for React comps; use
  GSAP only inside embedded HTML/canvas layers.

## QC before any full render

- Frame-check first, middle, last frame of every scene: motion must READ in stills
  (different framing at start vs end of every shot >1.5s).
- No element may sit perfectly still for a whole scene unless it is set dressing.
- Every ease/duration choice should be answerable: "why this feel for this beat?"
