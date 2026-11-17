#!/usr/bin/env python3
"""Generate reel.html + data.json from whisper words.json (claude-reel)."""
import json, pathlib, re

B = pathlib.Path(__file__).parent
VO = B.parent / "vo"
words = json.loads((VO / "words.json").read_text())

COUNTS = [8, 10, 10, 8, 10, 11, 15, 11, 11, 14, 9, 13, 11, 16, 20]  # VO line word counts (Devanagari script)
ROMAN = [
    "Ek line likhi aur poori reel ban gayi",
    "Main Claude Pro lene wala tha, do hazaar rupaye mahina",
    "Socha tha paise dunga to video khud hi ban jayegi",
    "Par ek pehla sach koi batata hi nahi",
    "Claude video nahi banata, wo sirf code hi deta hai",
    "Us code ko chalana aur render karna sab tumhare sar par",
    "Mera dost bola, Pro wale bhaiya, ab editor bhi ban jao! Aur khub has pada",
    "Sach ye hai ki aadhi janta aise hi paise phansati hai",
    "Phir mujhe ek free tool mila, uska naam comment me milega",
    "Hindi me ek line likhi, meri agency ki reel bana do, aur reel taiyaar",
    "Script awaaz visuals teeno bhi usi ne jode, zero rupaye",
    "Andar asal me ye hota hai, tool tumhari line ko scenes me todta hai",
    "Har ek scene par awaaz aur tasveer khud bitha deta hai",
    "Ek sach aur, free plan me chhota sa watermark aata hai, try karna bilkul free hai",
    "Ab tum faisla karo, do hazaar wala Pro, ya free wala dimaag? Comment me VIDEO likho, tool follow karke milega",
]
POSES = ["talking", "thinking", "talking", "surprised", "explaining", "determined",
         "laugh", "talking", "pointing", "explaining", "thumbsup", "explaining",
         "talking", "neutral", "pointing"]
# (line_idx, frac_in_line, emoji)
STK_SPEC = [(0, 0.05, "✍️"), (1, 0.55, "💳"), (4, 0.65, "💻"), (5, 0.40, "😮‍💨"),
            (6, 0.85, "😂"), (8, 0.55, "🔒"), (9, 0.30, "⌨️"), (10, 0.80, "🪙"),
            (13, 0.50, "💧"), (14, 0.15, "🎯")]

# --- segment whisper words into lines by VERIFIED word-index boundaries
# (checked by hand against segments.json; L13/L14 were dropped by whisper VAD -> synthetic spans
#  from the first-pass transcript: L13 ~42.9-45.8, L14 ~46.3-49.95)
INDEX_BOUNDS = [(0, 8), (8, 18), (18, 27), (27, 34), (34, 44), (44, 54), (54, 68),
                (68, 78), (78, 88), (88, 101), (101, 109), (109, 121), None, None, (121, 140)]
SYNTH = {12: (42.90, 45.80), 13: (46.30, 49.95)}
lines_w = []
for i, b in enumerate(INDEX_BOUNDS):
    lines_w.append([] if b is None else words[b[0]:b[1]])
for i, lw in enumerate(lines_w):
    if lw:
        print(f"L{i+1} ({len(lw)}w) {lw[0]['s']:.2f}-{lw[-1]['e']:.2f}:", " ".join(w["w"] for w in lw))
    else:
        print(f"L{i+1} SYNTHETIC span {SYNTH[i]}")

# --- build DATA
lines = []
for i, lw in enumerate(lines_w):
    if lw:
        start = lw[0]["s"]
        end = lw[-1]["e"]
    else:
        start, end = SYNTH[i]
    roman = [w.strip(",.!?—") for w in ROMAN[i].split()]
    disp = []
    for j, rw in enumerate(roman):
        if len(lw) == len(roman):
            s, e = lw[j]["s"], lw[j]["e"]
        else:  # proportional map inside the line span
            span = max(end - start, 0.01)
            s = start + span * j / len(roman)
            e = start + span * (j + 1) / len(roman)
        disp.append({"w": rw, "s": round(s, 3), "e": round(e, 3)})
    lines.append({"start": round(start, 3), "dur": round(end - start, 3), "words": disp})

total = round(lines[-1]["start"] + lines[-1]["dur"] + 0.9, 2)
scenes_t = []
for i, ln in enumerate(lines):
    t0 = 0.0 if i == 0 else round(max(lines[i - 1]["start"] + lines[i - 1]["dur"] - 0.05, ln["start"] - 0.12), 3)
    t1 = total if i == 14 else round(lines[i + 1]["start"] - 0.10, 3)
    scenes_t.append((t0, t1))

expr = [[round(lines[i]["start"] - 0.10 if i else 0.0, 3), POSES[i]] for i in range(15)]
expr.append([round(lines[14]["start"] + lines[14]["dur"] - 0.85, 3), "wink"])
expr.sort(key=lambda x: x[0])
stk = [[round(lines[i]["start"] + f * lines[i]["dur"], 3), e] for (i, f, e) in STK_SPEC]

SCENES = [
    {"pill": "HOOK · EK LINE = EK REEL", "l1": "Ek line likhi…", "l2": "poori reel ban gayi!", "kw": ["line", "reel"],
     "card": {"hero": "✍️", "big": "Ek line = <span class='g'>Poori Reel</span>", "rows": [["🎬", "Script khud"], ["🎙", "Awaaz khud"], ["✂️", "Edit khud"]], "rowAt": [0.35, 0.52, 0.68], "foot": "Kaise? Aage dekho…"}},
    {"pill": "STAKES · PAISA", "l1": "Claude PRO lene wala tha", "l2": "₹2,000 mahina!", "kw": ["Claude", "Pro", "hazaar"],
     "card": {"hero": "💳", "heroAt": 0.45, "big": "₹2,000<span class='g'>/mahina</span>", "bigsub": "Claude Pro — lene hi wala tha", "rows": [["📅", "Har mahine katega"]], "rowAt": [0.7], "foot": "Paise dene se pehle ye sun lo"}},
    {"pill": "UMEED", "l1": "Paise dunga to", "l2": "video khud banegi?", "kw": ["video"],
     "card": {"hero": "🤞", "big": "Video <span class='g'>khud</span> banegi?", "bigsub": "Meri umeed bilkul yahi thi", "rows": [["🎞", "Editor ka jhanjhat khatm"]], "rowAt": [0.55]}},
    {"pill": "SACH #1", "l1": "Par pehla SACH", "l2": "koi batata hi nahi", "kw": ["sach"],
     "card": {"hero": "⚠️", "big": "SACH <span class='g'>#1</span>", "bigsub": "Jo koi khul ke batata hi nahi", "rows": [["🙊", "Tumhe pata tha?"]], "rowAt": [0.6]}},
    {"pill": "SACH · CODE ≠ VIDEO", "l1": "Claude video NAHI banata", "l2": "sirf CODE deta hai", "kw": ["video", "code"],
     "card": {"kind": "code", "hero": "💻", "big": "CODE milega", "bigsub": "Video file NAHI", "rows": [], }},
    {"pill": "ASLI MEHNAT", "l1": "Code chalana, render karna", "l2": "sab TUMHARE sar par", "kw": ["render", "tumhare"],
     "card": {"kind": "bar", "hero": "⏳", "big": "Render <span class='g'>tumhare</span> sar par", "rows": [["🧑‍💻", "Editor bhi tum hi"]], "rowAt": [0.8]}},
    {"pill": "DOST KI HANSI", "l1": "Dost bola — Pro wale bhaiya", "l2": "ab EDITOR bhi ban jao!", "kw": ["editor", "has"],
     "card": {"kind": "quote", "hero": "😂", "rows": [["🗣", "Dost ki salah — bilkul free"]], "rowAt": [0.8], "foot": "Hansi me chhupa sach"}},
    {"pill": "HAQIQAT", "l1": "Aadhi janta aise hi", "l2": "paise phansati hai", "kw": ["paise"],
     "card": {"hero": "💸", "big": "Aadhi <span class='g'>janta</span>", "bigsub": "aise hi paise phansa leti hai", "rows": [["🕳", "Pro liya — video phir bhi nahi"]], "rowAt": [0.55]}},
    {"pill": "FREE TOOL", "l1": "Phir mila ek FREE tool", "l2": "naam comment me milega", "kw": ["free", "tool", "naam"],
     "card": {"kind": "lock", "big": "FREE <span class='g'>TOOL</span>", "bigsub": "Naam comment me milega", "rows": [["🔑", "Follow karke khulta hai"]], "rowAt": [0.65]}},
    {"pill": "EK LINE · HINDI ME", "l1": "Hindi me ek line likhi", "l2": "reel taiyaar!", "kw": ["Hindi", "line", "taiyaar"],
     "card": {"kind": "typing", "hero": "⌨️", "big": "Hindi me <span class='g'>ek line</span>", "rows": [["🎬", "Aur reel taiyaar ho gayi"]], "rowAt": [0.78]}},
    {"pill": "PAYOFF · ₹0", "l1": "Script · Awaaz · Visuals", "l2": "teeno usi ne jode — ₹0", "kw": ["Script", "awaaz", "visuals", "zero"],
     "card": {"hero": "🪙", "big": "₹0 <span class='g'>— Zero rupaye</span>", "rows": [["✓", "Script"], ["✓", "Awaaz"], ["✓", "Visuals"]], "rowAt": [0.08, 0.26, 0.44], "foot": "Teeno usi tool ne jode"}},
    {"pill": "ANDAR KA KAAM", "l1": "Tool line ko todta hai", "l2": "scenes me, andar se", "kw": ["scenes"],
     "card": {"hero": "🧩", "big": "Line → <span class='g'>Scenes</span>", "bigsub": "Tool andar se aise kaam karta hai", "rows": [["✂️", "Har scene — alag tukda"]], "rowAt": [0.6]}},
    {"pill": "AUTO SYNC", "l1": "Har scene par awaaz", "l2": "aur tasveer khud", "kw": ["awaaz", "tasveer"],
     "card": {"hero": "🔊", "big": "Awaaz + <span class='g'>Tasveer</span>", "bigsub": "Har scene par khud baith jati hai", "rows": [["🖼", "Visual bhi khud chunta hai"]], "rowAt": [0.62]}},
    {"pill": "IMANDAARI WALA SACH", "l1": "Ek sach aur — free plan me", "l2": "watermark aata hai", "kw": ["watermark", "free"],
     "card": {"kind": "wm", "hero": "💧", "big": "Ek sach <span class='g'>aur</span>", "bigsub": "Free plan me chhota watermark aata hai", "rows": [], "foot": "Try karna bilkul free hai — ye main chhupata nahi"}},
    {"pill": "FAISLA · VIDEO LIKHO", "l1": "PRO ₹2,000 ya FREE dimaag?", "l2": "VIDEO likho, tool milega", "kw": ["Pro", "free", "VIDEO"],
     "card": {"kind": "versus", "foot": "Comment me VIDEO likho — tool follow karke milega"}},
]
for i, s in enumerate(SCENES):
    s["t0"], s["t1"] = scenes_t[i]

DATA = {"lines": lines, "total": total, "expr": expr, "stk": stk}
html = (B / "reel_template.html").read_text()
html = html.replace("/*DATA*/", json.dumps(DATA, ensure_ascii=False))
html = html.replace("/*SCENES*/", json.dumps(SCENES, ensure_ascii=False))
(B / "reel.html").write_text(html)
(B / "data.json").write_text(json.dumps({"total": total}, indent=1))
print("TOTAL:", total, "| scenes:", len(SCENES), "| html bytes:", len(html))
