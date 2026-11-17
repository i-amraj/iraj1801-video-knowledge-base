# Mukku Tech (@mukku.tech) — Production Pipeline Research

Research date: 2026-11-16. Sources read in full where noted; flags are `verified live` (opened in research browser window) or `index` (search-index / text fetch).

## Summary

**The short answer is unusually well-documented — by Mukku himself.** @mukku.tech does not primarily hand-edit in After Effects, Premiere or CapCut. He has published, on his own site, the literal master prompt and the downloadable kit he uses, and both are **programmatic, code-rendered video**:

- **Claude / Claude Code writes the code → Remotion (React + TypeScript) renders it frame-by-frame → ffmpeg mixes audio and encodes the MP4.**
- His own “Mukku Style” spec is published verbatim: cream background `#F3E9DF`, frosted-glass central card, step pill + 2-line headline, word-timed caption pill, locked cartoon avatar, **1080×1920 at 60 fps**, **0.3 s scene fades, 0.22 s avatar pose cross-fades**, spring word-pops, no hard cuts, no shake.
- Voice and timing come *before* drawing: script (one line = one scene) → voice file → **faster-whisper word timestamps (`words.json`)** → every visual pops in on its spoken word.
- What is **not** publicly confirmed: (a) the exact serif-headline / real-screenshot + animated-cursor variant described in the mission as a named preset — it is best explained as the same Remotion engine with a different scene type and `brand.ts` font/colour config; and (b) which voice *he personally* uses on his flagship reels — his guides offer own-voice, Kokoro `hm_omega`, OpenAI `gpt-4o-mini-tts` and ElevenLabs as interchangeable options and never name his own choice.

Profile, verified live 2026-11-16: Instagram `@mukku.tech`, display name “Abh!”, **19,095 followers, 1 following**, bio “Exploring the digital world / Tech • AI • Cool discoveries”, link `mukkutech.surge.sh` — https://www.instagram.com/mukku.tech/ (`verified live`). His site, https://mukkutech.surge.sh/ (`verified live`), lists **16 free guides**, including KIT, STUDIO, REEL, FACELESS, FILM, CLAY, EDIT and SHORTS.

---

## Findings

### 1. Has mukku.tech himself shared his tools/workflow? — YES, extensively

There is no need to guess from the visuals alone. His distribution model is: Instagram reel → comment a keyword → DM → free PDF guide on `mukkutech.surge.sh`. Several of those guides are *about his own production method*, not just about third-party tools. No interview, paid course or YouTube “how I edit” video was found — the PDFs + the kit ZIP are the disclosure. (Searches in English and Hindi, 2026-11-16, `index`.)

#### 1a. The KIT guide — “mera master prompt” (his own words)

Source: **KIT guide**, https://mukkutech.surge.sh/guides/KIT_Mukku_Free_Reel_Kit_mukku.tech.pdf — read in full, 2026-11-16 (`index`, full text fetch).

He states, in Hinglish: *“Ye teeno frames isi KIT reel ke hain, isi guide wale tareeke se bane. Koi paid app nahi.”* — the frames in the guide are from the KIT reel itself, made by this method; no paid app. The 7-step flow is:

`avatar → script → voice → timings → Claude + master prompt → sound → check`

| Step | What he specifies |
|---|---|
| Kit / machine | Laptop (Win/Mac/Linux), 8 GB RAM enough; **Claude (free plan writes the code)**, **Node.js + ffmpeg** (both free); Gemini app once, for the avatar reference photo. First reel ~1 hour; after that only new script + voice. |
| 1. Avatar | One front photo → image-AI prompt: 2D cartoon avatar, clean bold outline, soft warm shading, **5×4 grid = 20 poses** in one image (idle, point right/left/down, 1/2/3/5 fingers, thumbs-up, OK, thinking, shrug, wave, holding phone, arms crossed, presenting…), waist crop, **mouth CLOSED in every pose**, flat pure green `#00FF00` background. Claude then cuts it into 20 transparent PNGs with the head aligned to the same position. Mouth is closed because **code animates the mouth from voice loudness**. |
| 2. Script | `script.txt`, **one line = one scene**, 30–40 s total. Hook in 0–2 s and that same line is the on-screen headline; small payoff at ~7 s; end card “Comment KEYWORD”. |
| 3. Voice | See §4 below. Output is `voice.wav`. |
| 4. Timings | **faster-whisper** (`WhisperModel("small")`, `word_timestamps=True`) → `words.json`: `{word, start, end, line, key}` where `key` marks the accent word of the line. |
| 5. Build | Paste Master Prompt Parts 1+2 into Claude with `script.txt`, `words.json` and pose names. Claude builds a **Remotion (React + TypeScript)** project and renders MP4. |
| 6. Sound | Mixed in **ffmpeg, not Remotion**: render muted, then `make_audio.py` adds voice + SFX + optional music bed. Free SFX from Pixabay (whoosh / pop / click / typing / ding). |
| 7. Check | ffmpeg `freezedetect` “boring-frame” check + 1 fps contact sheet; fix any still moment >1 s. |

**The Master Prompt’s published “Mukku Style” spec (Part 1 + 2, verbatim numbers):**

- Output: **1080 × 1920, 60 fps**, length = voice length + 1.5 s end card, total under 40 s. One composition, `Reel`. *All timing comes from `words.json` (frame = seconds × 60). Never hard-code times.*
- Background: **cream `#F3E9DF`** with soft blurred warm light pools (`#E8D6C4`, `#D9BFA6`, `#C9A27E`). Text near-black `#16120F`, Title Case on every on-screen word. Accent **terracotta `#B8674A`**, one accent word per headline, with a hand-drawn wavy underline under that word only.
- Cards: **frosted glass, white at 55–65%, 1 px white inner border, 36 px corner radius, large soft shadow.**
- Layout: top = small step pill (e.g. “Step 3 · Voice”); under it a **2-line centred headline, 84–96 px**; middle = **one glass card per script line, centred**, showing a *literal visual* of that line (typing text, counter, waveform, tick list, **UI mock**), each element popping in exactly on its spoken word; under the card = the caption pill; bottom = avatar, waist-up, on the right. Safe zones: keep text out of the right 140 px and the bottom 15%.
- Font named in the KIT prompt: **Nunito ExtraBold** (free) — see the serif caveat in §2.
- Captions: white rounded pill, groups of 1–3 words; new group when the group passes 19 characters, the line changes, or the word gap is >0.35 s. The spoken word pops at its `start` frame (**spring, scale up to 1.1, damping 10**, then settles); `key` words in terracotta.
- Headlines: words pop in one by one, **0.06 s apart (spring, damping 11)**.
- Avatar: **position locked** — no bobbing, sliding, shaking, scale pulses or entrance jumps. Allowed only: mouth open/close driven by voice loudness (precomputed per frame into `loudness.json`), a slow breath of at most 2 px, a blink every 3–4 s. **Pose change = 0.22 s cross-fade in place**, at the start of each line.
- Motion / scenes: **scene change = 0.3 s soft fade. No shake, no whip-pan, no flashes.** Something must change at least once per second (new word, pose change, pop, tick, or a gentle **3–4% zoom**); never leave a frame still for more than 1 s.
- Sound mix: whoosh at every scene start, pop when a card element appears, click on buttons/ticks; **SFX ~10 dB under voice, music ~25 dB under voice and ducked while talking**, music fade-out over the last 0.6 s; **normalise to −14 LUFS, true peak under −1.5 dB**, mux as AAC 320k.
- Deliverables Claude must produce: `package.json`, `src/Root.tsx`, `src/Reel.tsx`, `src/Captions.tsx`, `src/Avatar.tsx`, `make_loudness.py`, `make_audio.py`, `render.sh`, `check.sh`. `render.sh`: **render at `--scale=2` (smooth edges), downscale to 1080×1920 with ffmpeg lanczos**, encode H.264 `-preset slow -crf 14 -pix_fmt yuv420p`, bt709, `+faststart`.
- Final checklist in the guide: 1080×1920, **60 fps, file under 16 MB**; post 7–8 pm, one reel a day, *“wahi engine baar baar”* — the same engine again and again.

#### 1b. The Reel Studio Kit (STUDIO / REEL guides) — the downloadable version of the same engine

Sources: https://mukkutech.surge.sh/guides/STUDIO_Reel_Studio_Kit_mukku.tech.pdf and https://mukkutech.surge.sh/guides/REEL_Zip_Claude_Reel_mukku.tech.pdf — read in full / in search full-text, 2026-11-16 (`index`).

- A free folder, **MIT licence, ZIP 825 KB** at `mukkutech.surge.sh/files/reel-studio-kit.zip`, containing `CLAUDE.md`, `README.md`, `package.json`, `.claude/skills/reels/`, `src/`, `tools/` — skill, scenes, render, self-check.
- Workflow: open the folder in **Claude Code** (Claude desktop app, Code tab; paid Pro/Max plan) and type one line — `reel banao: [topic]`. Claude writes the script (hook / beats / twist / CTA / sources, then pauses for approval), generates voice, syncs captions with **local Whisper** (Python 3.11–3.13, Whisper `small` model ~480 MB, one-time), builds scenes, renders, self-checks frames, and writes caption + hashtags to `projects/<id>/post.md`. Output: `out/<id>.mp4`.
- Stack table in the guide: Node.js 18+ + ffmpeg (render, free); **Remotion is explicitly named as the video engine** (“Remotion (video engine, npm install se aata hai)”); demo he rendered himself: `out/Demo.mp4`, **1080×1920, 15 s, 1.5 MB**, placeholder hum instead of a voice.
- Looks in this kit: **3 presets — `cleanLight`, `boldDark`, `softPastel`**. Brand customisation is one file: **`src/brand.ts` — colours (6-digit hex), font, corner radius and handle** drive all scenes, captions and the end card.
- Commands: `npm run new -- my-reel`, `npm run voice -- my-reel --provider openai / elevenlabs / own`, `npm run sync -- my-reel --lang hi`, `npm run check`, `npm run render`, `npm run studio` (live preview). Revisions are by chat: “hook aur punchy karo”, “captions bade karo”, “reel banao: topic, dark preset, handle @…”.
- Self-check: frames are overlaid with Instagram’s no-go zones in red; overflow and overlap are measured; a contact sheet is inspected before delivery.
- His Instagram reels announcing this are themselves in the format: e.g. the STUDIO reel (posted 2026-10-30, https://www.instagram.com/reel/DfHwNlQMC7O/, `index` summary) and the REEL reel (posted 2026-10-31, https://www.instagram.com/reel/DfKU_VdzCBd/, `index` summary), the latter described in the index summary as *“clean, beige-themed graphics with screen recordings of a phone and computer interface, and a cartoon avatar of the creator”*, with an example run showing voiceover 42.5 s, captions 95% matched, final video 4.1 MB. That description is the closest published match to the mission’s screenshot-card format.

#### 1c. His other workflow guides (same philosophy, different looks)

All on https://mukkutech.surge.sh/ (`verified live` list, 2026-11-16):

- **FILM** — https://mukkutech.surge.sh/guides/FILM_Claude_Film_Repo_mukku.tech.pdf : Lemo OpusCar, 66 film styles for Claude Code. Explicit principle: *“Video AI model nahi. Claude canvas / WebGL pages likhta hai, unko frame-by-frame render karta hai, phir ffmpeg se MP4 banata hai.”* (No video AI model; Claude writes canvas/WebGL pages, renders frame-by-frame, ffmpeg makes the MP4.) That variant renders 1080×1920 at **30 fps**.
- **CLAY** — https://mukkutech.surge.sh/guides/CLAY_Clay_Animation_mukku.tech.pdf : clay look built in code with Python (numpy + Pillow, 1080×1920 frames, height-map → normals → soft lighting) + ffmpeg; explicitly *not* Blender / real 3D. Voice via ElevenLabs or own recording. CapCut is mentioned only as a final place to check the voice sync — the only CapCut mention found in his guides.
- **FACELESS** — https://mukkutech.surge.sh/guides/FACELESS_Guide_mukku.tech.pdf : a third-party “Faceless Shorts Skill” (nafay3d.com, 10.4 MB) for Claude Code; script, voice, word-synced captions, animation, sound and music → MP4; local Kokoro voice (~340 MB) + Whisper (~0.5 GB); 6 styles. He is candid that he read its `SKILL.md` but did **not** himself render a full short with it, and that its Kokoro voice is English-only.
- **SHORTS** — https://mukkutech.surge.sh/guides/SHORTS_Faceless_Shorts_mukku.tech.pdf : a beginner, phone-only recipe he recommends to others (Gemini/ChatGPT script → ElevenLabs voice → Meta AI images/animate → YouTube Create edit + auto-captions). This is a *recommendation for beginners*, not a claim about his own flagship pipeline.
- **EDIT** — https://mukkutech.surge.sh/guides/EDIT_AI_Video_Editing_mukku.tech.pdf : FavStash Creator Skills, an open-source repo that teaches Claude Code / Codex / Cursor to cut, caption and add motion graphics (Node 22+, FFmpeg, Git, yt-dlp).

**Tools he does NOT name for his own reels in any guide found:** After Effects, Premiere Pro. No AE/Premiere claim exists in the material indexed from his site. CapCut appears once, as a checking app in the CLAY guide.

### 2. Is this style a known template/format? Which pipeline produces it most plausibly?

#### What is confirmed

- The cream background, pill, two-line headline, central glass card, caption pill and avatar are **not an off-the-shelf CapCut/Canva template** in his case — they are a **published, named house style (“Mukku Style”)** with hex values, pixel sizes and motion timings, implemented as a reusable Remotion composition whose look is driven by `src/brand.ts` (colours, font, corner radius, handle) and by scene components. Re-using “the same engine again and again” is his stated posting system (KIT guide, above).
- The broader *method* — Claude Code + a code renderer + voice-first word timing — is a **recognised, fast-spreading faceless-explainer format in late 2026**, used independently by other creators:
  - An independent creator (Keyframes folder, `getkeyframes.com`) describes the identical workflow in “How My Faceless Videos Got 43.4M Views In One Month”, Medium, 2026-11-14, https://medium.com/@hugues.bouiss/how-my-faceless-videos-got-43-4m-views-in-4-weeks-009d4d4a50b4 (`index`, full text): *“I make these with Claude Code. Claude has no video model. It writes every scene as code, and Remotion renders that code into an MP4 on my computer.”* His four habits match Mukku’s kit point-for-point: voice first, then a timestamp for every word; one idea per beat; draw the real thing instead of a text box; check stills/contact sheets and render once (his timed render: 11 min 17 s for a 117 s reel).
  - Industry explainers now list three routes for “videos with Claude”, Route 3 being **Claude Code with Remotion or HyperFrames** — https://clippie.ai/blog/how-to-make-videos-with-claude (`index`).
  - The two code-rendering engines are directly compared by HeyGen’s HyperFrames docs and others: both open headless Chrome, step frame-by-frame and encode with ffmpeg, deterministically. **Remotion = React/TypeScript, timing in frames, `interpolate()`/`spring()`; HyperFrames = plain HTML/CSS + a paused GSAP timeline, timing in seconds.** — https://github.com/heygen-com/hyperframes/blob/711c4ff9f9cad16bc1ce4d0a9a05deb917206621/docs/guides/hyperframes-vs-remotion.mdx and https://www.growthcab.com/hyperframes-vs-remotion (`index`). Mukku’s kits are Remotion, not HyperFrames/GSAP — GSAP is only the plausible *alternative* engine for an identical look, and his FILM guide uses the related canvas/WebGL frame-by-frame route.

#### Comparison of the candidate pipelines

| Pipeline | How the look would be built | Fit with the evidence |
|---|---|---|
| **Programmatic Remotion (Claude Code) — CONFIRMED for his KIT/STUDIO reels** | React components: fixed layout from `brand.ts`; scenes as components; screenshots/UI mocks as `<Img>` inside a glass card; cursor/highlight as frame-driven divs; all timing from `words.json` (`frame = sec × 60`) | Matches every published number: 60 fps, 0.22 s pose cross-fade, 0.3 s scene fade, spring damping 10/11, `--scale=2` render, contact-sheet + freezedetect self-check. Also matches why an AI agent can revise a reel from a chat line. |
| HTML/CSS/JS + GSAP (HyperFrames-style) | Same DOM look, paused GSAP timeline seeked frame-by-frame | Visually indistinguishable in principle; **no evidence Mukku uses it for these reels** — his prompts, ZIP structure (`Root.tsx`, `Reel.tsx`) and npm scripts are React/Remotion. His FILM guide’s canvas/WebGL route is the nearest GSAP-adjacent thing he publishes. |
| Hand-keyframed After Effects / Premiere | Timeline project, manual keyframes per reel, .mogrt-style template reuse | Possible for a skilled editor, but contradicted as *his* method: he publishes code, prompts and an MIT ZIP instead, names Remotion explicitly, and never names AE/Premiere. Comparative sources note the structural difference: Remotion is “a function of the frame number”, one template renders many variations from props/data, UI text stays crisp DOM/CSS, and coding agents can write/edit it, whereas AE is “a timeline you drag”, strongest for character animation, VFX and compositing filmed footage — https://snapcn.dev/remotion-vs-after-effects and https://notes.aingyal.com/remotion-vs-video-editors/ (`index`). |
| AI video generators (Runway/Sora-style, CapCut auto-edit) | Generated pixels per clip | Ruled out by him explicitly for the FILM pipeline (“koi video AI model nahi” — no video AI model) and by the nature of the format: real website UI screenshots, exact text and a reusable layout cannot be held stable by generative video. His SHORTS guide recommends AI tools only for a beginner phone workflow. |

#### Inference — the specific screenshot-card / serif / cursor variant in the mission

Labelled **INFERENCE**, not a confirmed quote:

1. **Same engine, different scene type.** The KIT prompt already requires the central card to show a “literal visual” of each line, including a **UI mock**, with elements popping in on their spoken words. Replacing the generated UI mock with a **real screenshot** (captured at 2× so zooms stay sharp) and adding an animated cursor + highlight box is a standard Remotion scene pattern, documented independently in screenshot-demo pipelines: Playwright captures each screen state at `deviceScaleFactor: 2`; a frame-driven cursor glides between targets; a highlight/zoom reveals the focal region — e.g. https://github.com/iart-ai/ecommerce-video-skills/blob/HEAD/skills/product-demo-video/references/screenshot-demo.md and https://ai.georgeliu.com/p/how-i-built-polished-demo-videos (`index`). Mukku’s REEL/STUDIO announcement reels are described as beige graphics + screen recordings + avatar, i.e. this scene type inside the same kit.
2. **Serif headline = a `brand.ts` font swap, not a different editor.** The KIT prompt names Nunito ExtraBold, but the STUDIO kit explicitly makes font a brand variable, and Mukku’s own website headline (verified live) is set in a serif display face on the same cream background. A serif preset (`cleanLight`-style) therefore needs only a font change in `brand.ts` / the prompt. No source found names that serif preset.
3. **“Ghost-fade” of headline line 2 / speech-bubble text changing phrase-by-phrase** is exactly what a word-timed caption/headline component does when the outgoing group fades while the incoming group springs in: at 60 fps a 0.22–0.3 s overlap leaves a brief double-image (“ghost”). His published values — pose cross-fade 0.22 s, scene fade 0.3 s, caption groups of 1–3 words split on a >0.35 s gap or a line change — produce phrase-by-phrase bubble/pill changes synced to the voiceover by construction. The mission’s “speech bubble at the bottom” is the avatar-adjacent variant of his “caption pill under the card / avatar at the bottom” layout.
4. **Perfect layout consistency across reels** is the signature of code, not of hand editing: layout is a component with fixed safe zones (right 140 px, bottom 15% kept clear), and his self-check programmatically measures overflow/overlap and Instagram no-go zones on every render.

### 3. Technical ingredients of the smoothness — his values vs recognised standards

His numbers sit squarely inside recognised motion-design ranges, with one deliberate exception (bouncy word pops).

| Ingredient | Mukku’s published value (confirmed) | Recognised standard / reference value (independent sources) |
|---|---|---|
| Frame rate | **60 fps**, 1080×1920; render at 2× scale then lanczos-downscale, H.264 `-crf 14 -preset slow` | 60 fps halves the frame interval vs 30 fps (**16.67 ms vs 33.33 ms**), halving per-frame displacement, reducing temporal aliasing/jitter in pans and cursor moves, and needing *less* artificial motion blur because temporal sampling is already high — https://animost.com/ideas-inspirations/is-60fps-or-30fps-better-for-animation/ (`index`). Caveat from the same source: platforms may re-encode/drop to 30 fps on delivery, so 60 fps also acts as headroom. His FILM variant, by contrast, is 30 fps. |
| Scene transition | **0.3 s soft fade, no hard cuts**, no shake/whip/flash | Material Design 3 duration tokens: short 50–200 ms, **medium 250 / 300 / 350 / 400 ms**; transitions over ~400 ms feel too slow — https://github.com/danieldevfull/material-design-3-skill/blob/HEAD/material-design-3/references/motion.md (`index`). A 300 ms cross-fade is the textbook “medium” value. |
| Avatar pose change | **0.22 s cross-fade in place** | Falls in the common UI band: default transition **200 ms ease-out**, micro-interactions 120–180 ms, routine transitions never >300 ms; cross-fades specifically paired with ease-in-out `cubic-bezier(0.4, 0, 0.2, 1)` — https://github.com/modernui-io/clinicalsageai-2-replit/blob/HEAD/.claude/skills/motion-discipline/SKILL.md (`index`). The mission’s hypothesised 0.15–0.25 s cross-fade range is therefore correct in scale — his documented values are 0.22 s (pose) and 0.3 s (scene). |
| Word / headline pops | **Spring, damping 10** (caption word, scale to 1.1) and **damping 11** (headline words, staggered **0.06 s** apart) | Deliberately *playful*, not corporate-smooth. Generic Remotion presets are: smooth `{damping: 200}` (no bounce, default for text/cards and for `springTiming` transitions), snappy `{damping: 20, stiffness: 200}`, bouncy `{damping: 8, stiffness: 200}`, gentle `{damping: 200, stiffness: 50}` for large elements — https://www.typingmind.com/skills/anastasiyaw-remotion-production-guide and the Remotion reference mirrors in §Sources (`index`). Damping 10–11 ≈ the “bouncy” family, used by Mukku only for small word pops, while layout/scene motion stays calm — the standard advice is to reserve bounce for at most one element family per scene. |
| Cursor easing (screenshot scenes) | Not separately published by Mukku; his general rule is spring/interpolate-driven, frame-locked motion | Screenshot-demo reference implementations use **smoothstep / easeOutCubic** for the cursor (accelerate out of rest, decelerate into the target; “a linear cursor reads as robotic”), fire the click ripple *and* the screen-state change on the exact same `clickAt` frame, ripple as a spring (`damping 18`, 18 frames), press micro-scale 0.9 for ~6 frames, and a zoom that starts ~6 frames after the click and completes in ~30 frames with easeOutCubic; only one motion at a time (camera *or* cursor) — https://github.com/iart-ai/ecommerce-video-skills/blob/HEAD/skills/product-demo-video/references/screenshot-demo.md (`index`). |
| Easing curves generally | Implied by Remotion `spring()` / `interpolate(..., Easing)`; no explicit cubic-bezier published by Mukku | Canonical curves: Material standard `cubic-bezier(0.2, 0, 0, 1)` (legacy `0.4, 0, 0.2, 1`), decelerate/entrance `(0, 0, 0.2, 1)`, accelerate/exit `(0.4, 0, 1, 1)`, emphasized-decelerate `(0.05, 0.7, 0.1, 1)`; Apple-style `(0.25, 0.1, 0.25, 1)`; crisp UI entrance `(0.16, 1, 0.3, 1)` — Material token mirrors above and Remotion production guides (`index`). Rule across sources: never linear for position/scale; ease-out for entrances, ease-in for exits, ease-in-out for on-screen moves. |
| Slow push-in | **Gentle 3–4% zoom** as one of the allowed “something changes every second” devices; nothing may stay still >1 s (enforced by ffmpeg `freezedetect=n=0.003:d=1`) | The same device appears in independent Remotion demo pipelines as a slow, barely-noticeable Ken Burns zoom on screenshots, combined with spring-based fades between steps — https://ai.georgeliu.com/p/how-i-built-polished-demo-videos (`index`). |
| Motion blur / ghosting | No explicit motion-blur effect is published in his prompt. The visible ghosting is the **cross-fade overlap itself** (0.22–0.3 s), plus 2×-scale rendering for edge smoothness | At 60 fps, synthetic blur is less necessary (see frame-rate row). In code renderers, “blur/ghost” transitions are typically built as opacity/blur interpolations or wrapped fade presentations rather than AE-style directional blur; Remotion’s `@remotion/transitions` provides `fade()` with `linearTiming` / `springTiming({config:{damping:200}})` — Remotion reference mirrors, §Sources (`index`). **Inference:** do not attribute an AE motion-blur effect to his reels; the cross-fade + 60 fps sampling fully explains the look. |
| Audio finish (part of the perceived polish) | SFX −10 dB vs voice, music −25 dB + ducking, **−14 LUFS**, peak <−1.5 dB, AAC 320k | −14 LUFS is the conventional social/YouTube loudness target; included here because his guide specifies it as part of the same render script. |

### 4. Voiceover: AI TTS or his own voice?

**Confirmed:** He never, in any guide found, states “this is the voice I use on my own reels.” Every guide presents voice as a *choice the follower makes*, and the options differ by kit — which itself tells you the engine is voice-agnostic (it only needs a `voice.wav` + word timings).

| Guide | Voice options he gives | Notes |
|---|---|---|
| KIT (his own master prompt) | **Option A — your own voice** (phone recorder, mic a hand’s width away, quiet room, record line-by-line, re-take only the failed line) listed *first*; **Option B — free open-source AI voice: Kokoro**, running locally, Hindi male voice **`hm_omega`** (prompt: “Kokoro install karo aur script.txt ki har line se ek WAV banao, Hindi male voice hm_omega”). Tip: write English words in Devanagari (रील, कैप्शन्स) so the Hindi voice pronounces Hinglish correctly; make 2–3 takes per line. | The KIT workflow is built around a recorded voice file whose loudness drives the avatar’s mouth — it works identically for a human recording or a TTS WAV. |
| STUDIO / REEL (Reel Studio Kit) | **OpenAI `gpt-4o-mini-tts`** (paid, per use, API key in `.env`) **or ElevenLabs** (paid, key + voice ID) **or your own recording** (free; kit converts any format to clean WAV). Demo render uses a placeholder hum, not a real voice. | `npm run voice -- <id> --provider openai / elevenlabs / own` |
| SHORTS (beginner guide) | ElevenLabs (free account, 10,000 credits/month; commercial licence from paid Starter plan) | A recommendation to beginners, not a self-disclosure. |
| CLAY | ElevenLabs — “ek confident voice chuno” (pick a confident voice) — or record your own. | No voice name/ID given. |
| FACELESS (third-party skill) | Kokoro **English** voice built into that skill; for Hindi, record your own or swap in another TTS (untested by him, he says). | Local Kokoro ~340 MB + Whisper ~0.5 GB downloads. |

**Which Hindi TTS voices exist that could sound like this (background, independent sources):**

- **Kokoro (open-weight, 82M params, runs locally):** only **four Hindi voices exist** — female `hf_alpha`, `hf_beta`; male **`hm_omega`, `hm_psi`** — and all four are graded **C** (the lowest tier) in the official `VOICES.md`, reflecting limited Hindi training data — https://github.com/danielcorsano/reader/blob/HEAD/docs/KOKORO_SETUP.md and https://docs.jambonz.org/guides/features/tts-vendor-settings/kokoro (`index`). If his voice were Kokoro `hm_omega`, it would be a very specific, recognisable, somewhat flat Hindi male read; his guide presents it as the *free follower* option.
- **ElevenLabs:** the Hindi library is vast — mirrors list **~598 Hindi voices** (607 counting Azure) — with popular male narrator voices such as Raju (clear, natural, warm), Viraj (energetic, clear narrator), Raghav (calm, confident storyteller) and Kamal (deep and clear, marketed for YouTube explanations; voice ID `EppcM8bFS2tfl4Xu0tpj`) — https://json2video.com/ai-voices/languages/hindi/?gender=male (`index`). **No public source ties any ElevenLabs voice ID to mukku.tech.**
- **OpenAI `gpt-4o-mini-tts`:** 11 built-in voices, officially “optimized for English” while following Whisper’s language list (including Hindi); independent Hindi-short pipelines use e.g. `ash` (“warm male, good for Hindi”) at speed 0.88 with Hinglish delivery instructions — https://github.com/thakyanamtumhara/yt-shorts-bot/commit/7cbf3814eab28e3646155542088fa6f441c7f7d2 (`index`).

**Inference on his own voice:** The balance of his own published material leans toward **his own recorded voice being a first-class, likely primary input for the KIT-style reels** — it is Option A, the avatar/loudness system is designed around a personal recording, and the avatar is a cartoon of *himself* (20 poses from his own photo). But that is inference from ordering and design, **not a statement by him**. An AI voice (ElevenLabs or OpenAI, per the STUDIO kit he sells/gives away as his production kit) is equally compatible with the published pipeline, and a listener cannot distinguish the two routes from the guides alone. Any claim naming a specific TTS voice as “Mukku’s voice” would be unsourced.

---

## Confirmed vs Inference — at a glance

**CONFIRMED (his own published material):**
- Engine: Claude/Claude Code → **Remotion (React + TypeScript)** → ffmpeg; Node.js, Python/Whisper, Pixabay SFX.
- Spec: 1080×1920, **60 fps**, cream `#F3E9DF`, terracotta `#B8674A`, frosted card (white 55–65%, radius 36 px), pill + 84–96 px 2-line headline, caption pill (1–3 words, spring damping 10, scale 1.1), headline stagger 0.06 s / damping 11, avatar pose cross-fade **0.22 s**, scene fade **0.3 s**, 3–4% push-in, change at least every 1 s, `--scale=2` render, CRF 14, −14 LUFS.
- Avatar: 20-pose green-screen sheet from his photo, transparent PNGs, head locked, mouth from loudness, blink 3–4 s.
- Timing: faster-whisper word timestamps drive *all* animation; nothing hard-coded.
- Distribution: free PDF guides + MIT Reel Studio Kit ZIP (825 KB) via comment-keyword DM funnel; 3 looks `cleanLight / boldDark / softPastel`; brand in `src/brand.ts`.
- No AE/Premiere in his workflow disclosures; no video-AI generation in the FILM pipeline, by his explicit statement.

**INFERENCE (labelled, with reasoning in §2/§4):**
- The mission’s serif + real-screenshot + animated-cursor variant = same Remotion engine, different scene component + `brand.ts` font preset. No named preset or prompt for that exact variant was found.
- Ghost-fading = cross-fade overlap at 60 fps, not an AE motion-blur effect.
- His personal voice choice (own recording vs a specific TTS voice) is **not disclosed**; own-voice is the best-supported guess, not a fact.

## Could not verify

- No YouTube channel, interview, podcast or paid course by mukku.tech was found in English/Hindi searches on 2026-11-16; if one exists, it is not indexed under “mukku.tech / Mukku Tech”.
- The actual contents of `reel-studio-kit.zip` were not downloaded (research policy: no downloads); its structure and behaviour are taken from his STUDIO/REEL guides, which quote its file tree, npm scripts and demo output.
- Individual Instagram reels could not be frame-analysed in the browser (thumbnails did not render logged-out); reel-level claims rely on Instagram’s indexed summaries for the STUDIO (2026-10-30) and REEL (2026-10-31) posts plus his PDFs, whose frames he states are from the reels themselves.
- Whether Instagram delivers his uploads at 60 fps or re-encodes to 30 fps for most viewers could not be verified from his material.

## Sources

Primary (his own):
- KIT guide (master prompt, “Mukku Style”) — https://mukkutech.surge.sh/guides/KIT_Mukku_Free_Reel_Kit_mukku.tech.pdf — read in full 2026-11-16, `index`
- STUDIO guide (Reel Studio Kit) — https://mukkutech.surge.sh/guides/STUDIO_Reel_Studio_Kit_mukku.tech.pdf — read in full 2026-11-16, `index`
- REEL guide — https://mukkutech.surge.sh/guides/REEL_Zip_Claude_Reel_mukku.tech.pdf — search full-text 2026-11-16, `index`
- FILM guide — https://mukkutech.surge.sh/guides/FILM_Claude_Film_Repo_mukku.tech.pdf — read in full 2026-11-16, `index`
- CLAY guide — https://mukkutech.surge.sh/guides/CLAY_Clay_Animation_mukku.tech.pdf — search full-text 2026-11-16, `index`
- FACELESS guide — https://mukkutech.surge.sh/guides/FACELESS_Guide_mukku.tech.pdf — read in full 2026-11-16, `index`
- SHORTS guide — https://mukkutech.surge.sh/guides/SHORTS_Faceless_Shorts_mukku.tech.pdf — search full-text 2026-11-16, `index`
- EDIT guide — https://mukkutech.surge.sh/guides/EDIT_AI_Video_Editing_mukku.tech.pdf — search full-text 2026-11-16, `index`
- His site (16 guides list) — https://mukkutech.surge.sh/ — `verified live` 2026-11-16
- His Instagram profile (19,095 followers) — https://www.instagram.com/mukku.tech/ — `verified live` 2026-11-16
- STUDIO announcement reel, 2026-10-30 — https://www.instagram.com/reel/DfHwNlQMC7O/ — `index` summary
- REEL announcement reel, 2026-10-31 — https://www.instagram.com/reel/DfKU_VdzCBd/ — `index` summary

Independent / technical:
- Medium, Keyframes creator, faceless workflow — https://medium.com/@hugues.bouiss/how-my-faceless-videos-got-43-4m-views-in-4-weeks-009d4d4a50b4 — read in full 2026-11-16, `index`
- Clippie, “How to Make Videos With Claude” (Route 3: Remotion/HyperFrames) — https://clippie.ai/blog/how-to-make-videos-with-claude — `index`
- HyperFrames vs Remotion (HeyGen) — https://github.com/heygen-com/hyperframes/blob/711c4ff9f9cad16bc1ce4d0a9a05deb917206621/docs/guides/hyperframes-vs-remotion.mdx — `index`
- HyperFrames vs Remotion (growthcab, IG-reels-on-Remotion author) — https://www.growthcab.com/hyperframes-vs-remotion — `index`
- Remotion vs After Effects — https://snapcn.dev/remotion-vs-after-effects — `index`; also https://notes.aingyal.com/remotion-vs-video-editors/ — `index`
- Screenshot-demo pipeline (cursor smoothstep, ripple, zoom values) — https://github.com/iart-ai/ecommerce-video-skills/blob/HEAD/skills/product-demo-video/references/screenshot-demo.md — `index`
- Remotion demo videos with Claude Code (Ken Burns zoom, cursor, spring fades) — https://ai.georgeliu.com/p/how-i-built-polished-demo-videos — `index`
- Remotion spring/easing presets — https://www.typingmind.com/skills/anastasiyaw-remotion-production-guide — `index`; https://github.com/anastasiyaw/knowledge-space/blob/HEAD/docs/web-frontend/remotion-programmatic-video.md — `index`
- Material Design 3 motion tokens — https://github.com/danieldevfull/material-design-3-skill/blob/HEAD/material-design-3/references/motion.md — `index`; https://github.com/cgallic/design-os/blob/HEAD/design_os/canon/motion-design.md — `index`
- UI motion discipline (200 ms default, cross-fade curves) — https://github.com/modernui-io/clinicalsageai-2-replit/blob/HEAD/.claude/skills/motion-discipline/SKILL.md — `index`
- 60 fps vs 30 fps (frame interval, aliasing, motion blur) — https://animost.com/ideas-inspirations/is-60fps-or-30fps-better-for-animation/ — `index`
- Kokoro Hindi voices / grades — https://github.com/danielcorsano/reader/blob/HEAD/docs/KOKORO_SETUP.md — `index`; https://docs.jambonz.org/guides/features/tts-vendor-settings/kokoro — `index`
- ElevenLabs Hindi voices — https://json2video.com/ai-voices/languages/hindi/?gender=male — `index`
- OpenAI TTS Hindi usage example (`ash`) — https://github.com/thakyanamtumhara/yt-shorts-bot/commit/7cbf3814eab28e3646155542088fa6f441c7f7d2 — `index`

Working notes: `notes/kit-guide.md`, `notes/studio-reel-guides.md`, `notes/other-sources.md`.
