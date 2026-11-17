# Gemini TTS Voiceover

## Prove the connection with a real call

- Prove access with one short real generation call before you report the connection as working.

- Treat a placement or credential check as proof of setup only, never as proof that generation works.

## Verify the model and budget the quota

- Confirm the exact model name against the provider model list before the first call, since a name that worked last week can fail this week.

- Use the model the user last ordered, and update the helper default once when the user orders a different model.

- Count the calls the job needs before you start, and compare that count with the free tier daily limit for the model.

- When the ordered model hits its quota, move to the next fallback the user approved and record which model produced each line.

## Generate the lines and catch bad takes

- Keep one voice name across a whole narration for consistency.

- Group lines into one call only when they share one speaker, one pace and one emotion.

- Reject a take that reads the style direction or the prompt aloud instead of speaking the line.

- Save every successful take at once, and reuse takes already on disk before you call again.

## Verify the delivered file before delivery

- Transcribe the delivered final file and check that every scripted line is present in order.

- Treat a missing line as a failed take, and regenerate that line rather than delivering the file with a gap.

- Never verify a source take, a stem or a mix in place of the delivered file.

- Re-verify the file after any mux, loudness pass or edit, since a later step can drop a line.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Wait for the quota reset when the job is short and the user accepts the delay.

- Test a new voice or model on a short pass before the full job.

- Reuse a verified take from an earlier job when the line and the voice match.
## Hard lesson (2026-11-14, learned by a failed final)

- The helper's output WAV is written at 48000 Hz even though the model source is 24000 Hz. Before any asetrate pitch math, ffprobe the file's actual sample_rate and compute from that (pitch x1.12 on a 48k file = asetrate 53760). Using the source rate instead slows the voice to ~0.56x and ruins the take — only a Whisper check on the FINAL mixed file caught it.

## Hard lesson (2026-11-15, free-ai-tools reel v2)

- Long English style directions make Gemini 3.8 TTS read Hindi ~2.5x too slow (a 5.5s line came back 10.4–11.7s across voices and "VERY FAST" directions; pace instructions are ignored). Sending the RAW line with no direction at all returned natural brisk pace (4.0s). When pace matters, skip the direction or keep it to a couple of words.
- Quotas are per model per day: gemini-3.8-flash-tts free tier = 10 generate requests/day, and test calls burn it. The 3.1 model's real name is `gemini-3.1-flash-tts-preview` (plain `gemini-3.1-flash-tts` 404s); `gemini-3.8-flash-lite-tts` also exists. List models before guessing names, and budget test calls as real spend.

## TAIL GARBAGE + LIMITER LESSON (2026-11-16, Raj: "khir khir ki awaj, jaise TV ka signal chla gya ho")
- Gemini TTS PCM (.pcm sidecar) ke END me, speech khatam hone ke baad, ~0.2-0.45s ka LOUD RANDOM NOISE BURST aata hai (full-scale random samples). silenceremove use nahi kaat pata (burst loud hai, silence nahi) — isliye har line ke tail par static blast reel me chala jata hai. HAR generation ko check karo.
- FIX: raw PCM par speech_end nikalo (10ms windows, rms>0.02 aur non-chaotic ka last window), audio ko speech_end + 0.08s par CUT karo, PHIR resample/atempo. Word timings safe rehte hain (cut hamesha last word ke baad hota hai — Whisper se verify kiya: saare last words intact).
- WAV conversion (24k->48k default resample) peaks overshoot karke clip karti hai (clip% PCM 0.0065% -> WAV 0.066%). soxr resampler + processing ke end me halka peak-cap (alimiter limit=0.7, sirf safety) use karo.
- MIX RULE: VO par alimiter=limit=0.45 + volume boost WALI purani chain KABHI NAHI — wo harshness bursts ko ~8x badha deti hai (measured HF bursts 4 -> 32). Sirf loudnorm (I=-14, TP=-2) kaafi hai.
