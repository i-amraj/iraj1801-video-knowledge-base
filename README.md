# @i.raj1801 — Video System & Knowledge Base

Raj Soni (@i.raj1801) ke personal Instagram reels ka **poora system ek jagah**: identity, character, skills, scripts, project code, comment-agent aur bani hui reels. Ye repo usi kaam ka backup aur knowledge base hai jo hum roz karte hain.

**Format ek line me:** Mint Sticker identity (gehra mint stage) + glass theme motion + Raj ka apna 3D cartoon character (pose library ke saath) + word-synced graphics + Puck awaaz + comment-gated tool delivery — **50fps**, roz naye tool par 7-beat script.

---

## Folder map

| Folder | Kya hai |
|---|---|
| `01-knowledge/` | Saari seekh aur niyam — daily workflow, 7-beat script recipe, 8-step storyboard framework, Raj ke orders/prompts, dono reference channels ki file, format-v2 stack, mukku + MK ki poori analysis, BG study, designer-mindset research |
| `02-skills/` | Video banane me use hone wali skills — motion-director (266 moves ka code + 9 themes), hyperframes family, gemini-tts-voiceover, gsap-motion, media-use, captions-overlay, ai-video-editor, stickman-video-master, routine-work-protocol |
| `03-character/` | Raj ka 3D cartoon character — emotion sheet (9), acting poses sheet (6), **pose library (15 poses + MANIFEST)**, cutouts, reference photos |
| `04-projects/` | Har reel ka source code — graphics engine (gfx-v1), mukku-style build, Claude-vs-free-tool v1 aur v2 (glass), character demo engine, format-v2 toolkit tests |
| `05-comment-agent/` | Instagram comment agent (Cloudflare Worker) — har comment par reply, follow check ke baad button se tool delivery |
| `06-outputs/` | Bani hui reels aur covers — promo reel, free-ai-tools reel, captions reel (graphics + mukku-style), Claude-vs-free-tool v1, character demo v11, identity demos |

## Pipeline (roz ka kaam)

1. **Watch** — @mukku.tech aur @learnaiwithmk ki nayi reel (sirf dekhna, like/comment/follow nahi)
2. **Research** — tool nikaalo, deep research, verified official URL
3. **Script** — 7-beat recipe par (150–180 shabd, har line = 1 shot, share + comment trigger ke saath)
4. **Voice** — Gemini TTS, Puck awaaz; tail-noise kaatna + gap-silence verify (zero khir-khir)
5. **Build** — Format V2 stack: motion-director (glass) + HyperFrames + three.js + Rapier physics + postprocessing + librosa beat-map; pose library se character
6. **Render** — 50fps, chunked; QC: stills + loudness + gap check
7. **Deliver** — tool ka guide repo + comment-agent me reward; post sirf Raj ke order par

## Pakke niyam

- FPS = **50** (60 nahi) · Har reel me music (fresh, license-safe) + voiceover
- SFX sirf real recorded bundle se · Synth music NAHI
- Link kabhi seedha nahi — pehle follow check, phir button se delivery
- Koi third-party automation NAHI · Publish sirf Raj ke order par

Detail: `01-knowledge/raj-instructions-and-prompts.md`

## Reference channels

- **@mukku.tech** (Abh!) — https://www.instagram.com/mukku.tech/ · site: https://mukkutech.surge.sh
- **@learnaiwithmk** (MK | AI TOOLS & VIDEOS GUIDE) — https://www.instagram.com/learnaiwithmk/

Craft unse seekha hai, identity apni hai. Detail: `01-knowledge/reference-channels.md`

## Is repo me kya NAHI hai (jaan-bujh kar)

- **Secrets/credentials** — ek bhi nahi. Comment-agent ke tokens Cloudflare KV me rehte hain, code me kabhi nahi.
- **Reference creators ki downloaded videos** — sirf unki written analysis hai (hamari apni likhi hui).
- **motion-director ke 266 preview MP4** — moves ka saara code/JSON yahan hai; preview videos upstream repo me hain: https://github.com/sharbelxyz/motion-director
- **Render ke beech wale frames aur bade intermediate audio** — sirf source code aur final outputs rakhe hain.
- Do sabse badi output files (27.5MB + 26.7MB) GitHub ki web-upload limit (25MB) se upar hain — wo is repo ke **Releases** me milengi.

---
*System by Raj Soni × Nikki (Muse) — Kanpur, Nov 2026*
