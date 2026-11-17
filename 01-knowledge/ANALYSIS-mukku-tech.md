# @mukku.tech — Frame-by-frame Motion Graphics Analysis (16 Nov 2026)
Videos in this folder: Dfzj5GxThY0 (35s, latest), Dfw9Ncci94i (62s), DfuZsvVsJN1 (45.6s), Dft5JDxsL-z (25.6s), DfSDZSuirJs (48.7s, Raj's linked reel). All downloaded via yt-dlp; every frame decoded (60fps) for diff analysis; contact sheets + 60fps sequences + full-res frames extracted.

## Hard numbers (all 5 videos)
- 1080x1920, **60 fps**, VP9.
- **Hard cuts: ZERO** in all 5. No frame pair crosses the cut threshold — every scene change is a crossfade/blur/slide of ~8-14 frames (0.13-0.23s).
- Motion is gentle: median frame-to-frame change during motion 0.34-0.53 (of 255); p90 only 1.7-3.5. Mean jerk in motion 0.44-0.64 — very low = smooth easing curves, no jitter, no linear steps.
- Longest fully-static hold: 0.48-1.42s. Something always moves within ~1.5s: slow card push-in (scale drift), cursor glide, headline ghost-fade, or UI animating inside the screenshot (chart bars grow, numbers count).
- Frame layout never changes: fixed background, fixed card position, fixed caption zone.

## The system (grammar)
1. Background: fixed cream/beige radial (sunburst + faint doodles) — never changes mid-video. Newest series uses a pale-green variant + sans headlines; brown/serif is the main series.
2. Top: small pill label (section tag, letterspaced caps) + 2-line serif headline: line 1 black upright, line 2 brown/gold ITALIC — line 2 enters as a grey "ghost" then fills (visible in frame sequences).
3. Centre: ONE white rounded card (soft shadow, slight tilt) = the proof. Real UI screenshots inside a browser-window mock (traffic lights + URL bar). An animated white cursor glides and a red/orange highlight box is drawn around the exact element being spoken about. UI inside screenshots is alive (bars grow, counters tick).
4. Bottom: circular avatar badge + white speech bubble; bold serif Hinglish text changes phrase-by-phrase (~1-2s), exactly on the spoken words; key word in italic accent colour.
5. Below card sometimes: a summary stat pill (e.g. struck price -> new price).
6. End: CTA card (logo + "COMMENT <keyword>") — last beat only.
7. Transitions: crossfade + slight scale + blur ghost (~0.2s). One deliberate 1-frame orange flash in the newest video. No whip pans, no camera moves; motion lives inside the card and text.
8. Colour/type discipline: one accent (brown/gold or green), one serif (or one sans in green series), real numbers everywhere (Rs24, 215 pieces style proof), fine-print disclaimer under the card in the ad reel.

## Why it feels smooth (the recipe)
- 60fps delivery + sub-0.25s crossfades instead of cuts.
- Easing everywhere: elements decelerate (low jerk measured), nothing moves linearly, nothing pops without a fade/scale.
- Motion hierarchy: background frozen, card micro-motion (slow push), content crossfades, cursor does the "acting", captions swap on words.
- One idea per beat (~3-6s), sub-motion every 1-2s (caption swap, cursor move, highlight draw).

## MOTION RECIPE — his published kit spec (mukku.tech's own guides, mukkutech.surge.sh) cross-checked with my frame measurements
Pipeline (CONFIRMED from his own free guides): Claude/Claude Code writes code -> **Remotion (React+TS)** renders frame-by-frame -> ffmpeg mixes audio. No After Effects/Premiere/CapCut. Free Reel Studio Kit ZIP on his site. Voice-first: script.txt (1 line = 1 scene) -> voice.wav -> faster-whisper **words.json** {word,start,end,line} -> ALL animation timed from words.json (frame = sec x 60), never hand-placed.
- Format: 1080x1920, 60fps, length = voice + 1.5s end card, <40s typical.
- Colours: bg cream #F3E9DF, warm light pools #E8D6C4/#D9BFA6/#C9A27E; text #16120F; accent terracotta #B8674A (one word per headline + wavy underline).
- Cards: frosted glass white 55-65% opacity, 1px inner border, 36px radius. Headline 84-96px, 2 lines; top step pill; caption pill under card; avatar bottom-right (our downloads show bottom-left badge + bubble in the ad/serif variant).
- Motion values (his): scene fade 0.3s; avatar pose crossfade 0.22s; caption word spring damping 10, scale to 1.1; headline words stagger 0.06s, damping 11; push-in 3-4% per scene; visual change >= 1/sec; freezedetect check: nothing still > 1s.
- Avatar: 20-pose sheet from his photo, mouth driven by per-frame loudness (loudness.json), breath <=2px, blink every 3-4s.
- Render: Remotion --scale=2 -> ffmpeg lanczos downscale, H.264 crf14 preset slow; audio: SFX -10dB, music -25dB ducked, -14 LUFS, AAC 320k.
- Voice options in his kit: own recording (listed first) or Kokoro Hindi male hm_omega; studio kit also lists OpenAI gpt-4o-mini-tts / ElevenLabs. He never names which one HE uses.
MY MEASUREMENTS (this folder's 5 downloads) vs spec: 60fps confirmed; hard cuts 0 (spec: fades only); motion events 1.9-3.4/sec (spec: >=1/sec); longest still 0.48-1.42s (spec: <1s boring-frame rule — the 1.42s outlier is the linked ad reel); visible transition blend ~10-14 frames ≈ 0.2s + ease tails (spec: 0.3s scene fade). MATCH.
