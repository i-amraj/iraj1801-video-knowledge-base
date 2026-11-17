import json, pathlib, shutil, re

ROOT = pathlib.Path('/home/hatch/workspace/claude-reel-v2')
FILM = ROOT / 'film'
AST = FILM / 'assets'
SRC = pathlib.Path('/home/hatch/workspace/claude-reel-v2-assets')
DATA_ALL = json.load(open(SRC / 'reel_data.json'))
DATA, SCENES = DATA_ALL['DATA'], DATA_ALL['SCENES']

def _san(o):
    if isinstance(o, str):
        return o.replace('—', '·').replace('–', '-')
    if isinstance(o, list):
        return [_san(x) for x in o]
    if isinstance(o, dict):
        return {k: _san(v) for k, v in o.items()}
    return o
DATA, SCENES = _san(DATA), _san(SCENES)
BEATS = json.load(open(SRC / 'beats.json'))['beats']
COINS = json.load(open(SRC / 'coins.json'))
TOTAL = 59.2
TYPED_TEXT = 'मेरी शादी की वीडियो बना दो'

# ---------- assets ----------
(AST / 'poses').mkdir(exist_ok=True)
for p in pathlib.Path('/home/hatch/workspace/identity/poses').glob('*.png'):
    shutil.copy(p, AST / 'poses' / p.name)
(AST / 'vendor').mkdir(exist_ok=True)
TK = pathlib.Path('/home/hatch/workspace/format-v2/toolkit/node_modules')
shutil.copy(TK / 'three/build/three.module.js', AST / 'vendor/three.module.js')
shutil.copy(TK / 'postprocessing/build/index.js', AST / 'vendor/postprocessing.js')
(AST / 'beats.js').write_text('window.MD_BEATS = ' + json.dumps({
    'bpm': 92.29, 'offset': 0.379, 'beatsPerBar': 4, 'length': TOTAL,
    'cues': {'drop': 35.28, 'logo': 49.98}}) + ';\n')
(AST / 'coins.js').write_text('window.COINS = ' + json.dumps(COINS) + ';\n')

POSES = sorted({e[1] for e in DATA['expr']})

def esc(s):
    return s

def wrap_kw(text, kws):
    out = text
    for kw in kws:
        pat = re.compile(r'(?<!\w)' + re.escape(kw) + r'(?!\w)', re.IGNORECASE)
        out = pat.sub(lambda m: f"<span class='md-lit'>{m.group(0)}</span>", out, count=1)
    return out

def rows_html(card, sid):
    rows = card.get('rows') or []
    if not rows:
        return ''
    items = ''.join(
        f"<div class='srow' id='{sid}-row{j}'><span class='ric'>{ic}</span><span>{tx}</span></div>"
        for j, (ic, tx) in enumerate(rows))
    return f"<div class='rows'>{items}</div>"

def generic_inner(card, sid, i):
    h = []
    if card.get('hero'):
        h.append(f"<div class='hero' id='{sid}-hero'>{card['hero']}</div>")
    if card.get('big'):
        h.append(f"<div class='big'>{card['big']}</div>")
    if card.get('bigsub'):
        h.append(f"<div class='bigsub' id='{sid}-bigsub'>{card['bigsub']}</div>")
    h.append(rows_html(card, sid))
    if card.get('foot'):
        h.append(f"<div class='foot' id='{sid}-foot'>{card['foot']}</div>")
    return ''.join(h)

def card_inner(card, sid, i):
    kind = card.get('kind')
    if kind == 'code':
        lines = ["def reel(topic):", "    script = likho(topic)", "    return script  # bas text!",
                 "    video = ???  # yaha atak gaya"]
        lis = ''.join(f"<div class='cline' id='{sid}-cl{j}'><span class='cn'>{j+1}</span>{l}</div>" for j, l in enumerate(lines))
        return (f"<div class='hero' id='{sid}-hero'>{card.get('hero','')}</div>"
                f"<div class='big'>{card['big']}</div>"
                f"<div class='bigsub' id='{sid}-bigsub'>{card.get('bigsub','')}</div>"
                f"<div class='codewin'>{lis}</div>"
                f"<div class='xchip' id='{sid}-chip'>✗ Video file NAHI milegi</div>")
    if kind == 'bar':
        return (f"<div class='hero' id='{sid}-hero'>{card.get('hero','')}</div>"
                f"<div class='big'>{card['big']}</div>"
                f"<div class='track'><div class='fill' id='{sid}-fill'></div></div>"
                f"<div class='xchip' id='{sid}-chip'>⚠ Render Error: limit khatm!</div>"
                + rows_html(card, sid))
    if kind == 'quote':
        line7 = ' '.join(w['w'] for w in DATA['lines'][6]['words'])
        return (f"<div class='hero' id='{sid}-hero'>{card.get('hero','')}</div>"
                f"<div class='quote'>“{line7}”</div>"
                + rows_html(card, sid)
                + (f"<div class='foot' id='{sid}-foot'>{card['foot']}</div>" if card.get('foot') else ''))
    if kind == 'lock':
        return (f"<div class='big'>{card['big']}</div>"
                f"<div class='bigsub' id='{sid}-bigsub'>{card.get('bigsub','')}</div>"
                f"<div class='lockplate'><span class='lockic'>🔒</span><span class='blur-name'>Fliki AI</span>"
                f"<span class='stamp' id='{sid}-stamp'>SECRET</span></div>"
                + rows_html(card, sid))
    if kind == 'typing':
        typed = TYPED_TEXT
        spans = ''.join(f"<span class='tch' id='{sid}-tc{j}'>{c}</span>" for j, c in enumerate(typed))
        return (f"<div class='hero' id='{sid}-hero'>{card.get('hero','')}</div>"
                f"<div class='big'>{card['big']}</div>"
                f"<div class='typewin'><span class='tprompt'>›</span>{spans}<span class='caret' id='{sid}-caret'></span></div>"
                + rows_html(card, sid))
    if kind == 'wm':
        return (f"<div class='hero' id='{sid}-hero'>{card.get('hero','')}</div>"
                f"<div class='big'>{card['big']}</div>"
                f"<div class='bigsub' id='{sid}-bigsub'>{card.get('bigsub','')}</div>"
                f"<div class='reelmock'><span class='play'>▶</span><span class='wmband'>WATERMARK</span></div>"
                f"<div class='foot' id='{sid}-foot'>{card.get('foot','')}</div>")
    if kind == 'versus':
        return (f"<div class='disc' id='{sid}-disc'><img src='assets/mark.png' alt=''></div>"
                f"<div class='versus'>"
                f"<div class='vplate bad' id='{sid}-va'><div class='vname'>CLAUDE PRO</div>"
                f"<div class='vprice'>₹2,000<span>/mahina</span></div><div class='vmark no'>✗ Video NAHI</div></div>"
                f"<div class='vplate good' id='{sid}-vb'><div class='vname'>FREE TOOL</div>"
                f"<div class='vprice'>₹0</div><div class='vmark ok'>✓ Poori Reel</div></div></div>"
                f"<div class='cta' id='{sid}-cta'>Comment me <b>VIDEO</b> likho</div>"
                f"<div class='foot' id='{sid}-foot'>{card.get('foot','')}</div>")
    if i == 10:  # scene 11: payoff coins
        chips = ''.join(f"<span class='pchip' id='{sid}-chip{j}'>✓ {t}</span>" for j, (_, t) in enumerate(card['rows']))
        return (f"<div class='big'>{card['big']}</div>"
                f"<div class='pchips'>{chips}</div>"
                f"<div class='foot' id='{sid}-foot'>{card.get('foot','')}</div>")
    return generic_inner(card, sid, i)

# ---------- sections ----------
sections, scene_js = [], []
WHIP = {4, 9}
for i, s in enumerate(SCENES):
    sid = f's{i+1}'
    t0, t1 = s['t0'], s['t1']
    dur = (TOTAL - t0) if i == len(SCENES) - 1 else (t1 - t0) + 0.45
    l1 = wrap_kw(s['l1'], s['kw']) if s.get('l1') else ''
    l2 = wrap_kw(s['l2'], s['kw']) if s.get('l2') else ''
    coins_canvas = f"<canvas id='coinsGL' width='940' height='660'></canvas>" if i == 10 else ''
    sections.append(f"""
<section id="{sid}" class="clip md-scene" data-start="{t0}" data-duration="{dur:.2f}">
  <div class="md-world"><div class="md-rig" id="{sid}-rig" data-layout-allow-overflow>
    <div class="spill md-glass" id="{sid}-pill">{s['pill']}</div>
    <h1 class="md-line sh" id="{sid}-l1" data-in="words@{t0+0.06:.2f}" data-out="blur@{t1-0.28:.2f}">{l1}</h1>
    <h2 class="md-line sh" id="{sid}-l2" data-in="words@{t0+0.24:.2f}" data-out="blur@{t1-0.28:.2f}">{l2}</h2>
    <div class="md-glass scard" id="{sid}-card">{card_inner(s['card'], sid, i)}</div>
    {coins_canvas}
  </div></div>
</section>""")

    D = t1 - t0
    js = [f"// ---- scene {i+1} ----"]
    js.append(f"tl.fromTo('#{sid}-rig', {{y:6}}, {{y:-10, duration:{D:.2f}, ease:'sine.inOut'}}, {t0:.2f});")
    if i > 0:
        js.append(f"tl.fromTo('#{sid}-rig', {{scale:1.05, filter:'blur(6px)'}}, {{scale:1, filter:'blur(0px)', duration:0.35, ease:'power2.out'}}, {t0:.2f});")
    js.append(f"tl.fromTo('#{sid}-pill', {{y:-26, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:'power3.out'}}, {t0+0.03:.2f});")
    js.append(f"MD.sweep(tl, '#{sid}-pill', {t0+0.5:.2f}, 0.7);")
    js.append(f"MD.fly(tl, '#{sid}-card', {t0+0.12:.2f}, {{z:-1100, ry:-14, dur:0.7}});")
    js.append(f"MD.sweep(tl, '#{sid}-card', {t0+0.78:.2f}, 0.9);")
    card = s['card']
    if card.get('hero') and i != 10:
        hat = t0 + card.get('heroAt', 0.28) * D
        js.append(f"tl.fromTo('#{sid}-hero', {{scale:0.3, opacity:0, rotation:-14}}, {{scale:1, opacity:1, rotation:0, duration:0.45, ease:'back.out(1.9)'}}, {hat:.2f});")
    if card.get('big'):
        bat = t0 + 0.42 * D
        js.append(f"tl.fromTo('#{sid}-card .big', {{scale:1.45, opacity:0}}, {{scale:1, opacity:1, duration:0.38, ease:'expo.out'}}, {bat:.2f});")
        js.append(f"MD.stamp(tl, '#{sid}-card .big', {bat+0.4:.2f}, 0.05);")
    if card.get('bigsub'):
        js.append(f"tl.fromTo('#{sid}-bigsub', {{y:22, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:'power2.out'}}, {t0+0.52*D:.2f});")
    if i != 10:
        for j, frac in enumerate(card.get('rowAt') or []):
            js.append(f"tl.fromTo('#{sid}-row{j}', {{y:34, opacity:0, scale:0.92}}, {{y:0, opacity:1, scale:1, duration:0.4, ease:'back.out(1.7)'}}, {t0+frac*D:.2f});")
    if card.get('foot'):
        js.append(f"tl.fromTo('#{sid}-foot', {{opacity:0}}, {{opacity:1, duration:0.4}}, {t1-0.85:.2f});")
    kind = card.get('kind')
    if kind == 'code':
        for j in range(4):
            js.append(f"tl.fromTo('#{sid}-cl{j}', {{x:-30, opacity:0}}, {{x:0, opacity:1, duration:0.3}}, {t0+0.35*D+j*0.16:.2f});")
        js.append(f"tl.fromTo('#{sid}-chip', {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:'back.out(2)'}}, {t0+0.78*D:.2f});")
    if kind == 'bar':
        js.append(f"tl.fromTo('#{sid}-fill', {{scaleX:0}}, {{scaleX:0.72, duration:{0.55*D:.2f}, ease:'power1.inOut'}}, {t0+0.3*D:.2f});")
        js.append(f"tl.to('#{sid}-fill', {{scaleX:0.69, duration:0.07, yoyo:true, repeat:3}}, {t0+0.85*D:.2f});")
        js.append(f"tl.fromTo('#{sid}-chip', {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:'back.out(2)'}}, {t0+0.88*D:.2f});")
    if kind == 'lock':
        js.append(f"tl.fromTo('#{sid}-stamp', {{scale:2.1, opacity:0, rotation:-18}}, {{scale:1, opacity:1, rotation:-12, duration:0.3, ease:'expo.out'}}, {t0+0.6*D:.2f});")
    if kind == 'typing':
        n = len(TYPED_TEXT)
        for j in range(n):
            js.append(f"tl.set('#{sid}-tc{j}', {{opacity:1}}, {t0+0.3*D+j*0.055:.2f});")
    if kind == 'versus':
        js.append(f"tl.fromTo('#{sid}-disc', {{scale:1.8, opacity:0, filter:'blur(14px)'}}, {{scale:1, opacity:1, filter:'blur(0px)', duration:0.45, ease:'expo.out'}}, {t0+0.08:.2f});")
        js.append(f"MD.stamp(tl, '#{sid}-disc', {t0+0.55:.2f}, 0.07);")
        js.append(f"MD.sweep(tl, '#{sid}-disc', {t0+0.4:.2f}, 0.8);")
        js.append(f"tl.fromTo('#{sid}-va', {{y:-320, z:-500, rotationX:-30, opacity:0}}, {{y:0, z:0, rotationX:0, opacity:1, duration:0.55, ease:'expo.out'}}, {t0+0.25:.2f});")
        js.append(f"tl.fromTo('#{sid}-vb', {{y:-320, z:-500, rotationX:-30, opacity:0}}, {{y:0, z:0, rotationX:0, opacity:1, duration:0.55, ease:'expo.out'}}, {t0+0.55:.2f});")
        js.append(f"MD.sweep(tl, '#{sid}-vb', {t0+1.15:.2f}, 0.8);")
        js.append(f"tl.fromTo('#{sid}-cta', {{scale:0.5, opacity:0}}, {{scale:1, opacity:1, duration:0.4, ease:'back.out(2)'}}, {t0+1.35:.2f});")
        for b in BEATS:
            if t0 + 1.7 < b < 58.3:
                js.append(f"tl.fromTo('#{sid}-cta', {{scale:1}}, {{scale:1.045, duration:0.1, yoyo:true, repeat:1, ease:'power1.out'}}, {b:.2f});")
    if i == 10:
        for j in range(3):
            js.append(f"tl.fromTo('#{sid}-chip{j}', {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:'back.out(2)'}}, {t0+0.15+j*0.35:.2f});")
        for b in BEATS:
            if t0 < b < t1:
                js.append(f"tl.fromTo('#{sid}-card', {{scale:1}}, {{scale:1.014, duration:0.09, yoyo:true, repeat:1, ease:'power1.out'}}, {b:.2f});")
    if i < 14:
        if (i + 1) in WHIP:
            js.append(f"tl.to('#{sid}-rig', {{x:-950, opacity:0, filter:'blur(20px)', duration:0.3, ease:'power3.in'}}, {t1-0.02:.2f});")
        else:
            js.append(f"tl.to('#{sid}-rig', {{scale:2.2, opacity:0, filter:'blur(18px)', duration:0.42, ease:'power3.in'}}, {t1-0.02:.2f});")
    scene_js.append('\n'.join(js))

# ---------- character / bubble / sticker (single elements, draw(t) pattern) ----------
poses_html = ''.join(
    f"<img class='pose' id='pose-{p}' src='assets/poses/{p}.png' alt='' style='opacity:{1 if p == DATA['expr'][0][1] else 0}'>"
    for p in POSES)

phrases = []  # (start, [(word, s, e)])
for line in DATA['lines']:
    ws = line['words']
    for k in range(0, len(ws), 3):
        grp = ws[k:k+3]
        phrases.append((grp[0]['s'], grp))
UI_JSON = json.dumps({
    'phrases': [{'s': ps, 'words': [{'w': w['w'], 's': w['s'], 'e': w['e']} for w in grp]} for ps, grp in phrases],
    'expr': DATA['expr'], 'stk': DATA['stk']}, ensure_ascii=False)

UI_JS = """
// ---- UI layer: character + karaoke bubble + sticker, pure function of t ----
const UI = """ + UI_JSON + """;
const bubEl = document.getElementById('bubble');
const stkEl = document.getElementById('sticker');
const poseEls = {};
document.querySelectorAll('.pose').forEach(im => poseEls[im.id.slice(5)] = im);
let curPhrase = -1;
function drawUI(t) {
  // bubble: active phrase
  let pi = -1;
  for (let i = 0; i < UI.phrases.length; i++) {
    const nx = i + 1 < UI.phrases.length ? UI.phrases[i + 1].s : 58.9;
    if (t >= UI.phrases[i].s && t < nx) { pi = i; break; }
  }
  if (pi !== curPhrase) {
    curPhrase = pi;
    if (pi >= 0) bubEl.innerHTML = UI.phrases[pi].words.map(w => `<span class="bw">${w.w}</span>`).join('');
  }
  if (pi < 0) { bubEl.style.opacity = '0'; }
  else {
    const ph = UI.phrases[pi];
    const pop = Math.min(1, (t - ph.s) / 0.14);
    bubEl.style.opacity = '1';
    bubEl.style.transform = `scale(${0.96 + 0.04 * pop})`;
    const spans = bubEl.children;
    for (let wi = 0; wi < ph.words.length; wi++) {
      const w = ph.words[wi], sp = spans[wi];
      if (!sp) break;
      if (t >= w.e) { sp.style.color = '#0B3D2E'; sp.style.transform = 'scale(1)'; }
      else if (t >= w.s) { sp.style.color = '#0E9F6E'; sp.style.transform = 'scale(1.14)'; }
      else { sp.style.color = '#54655B'; sp.style.transform = 'scale(1)'; }
    }
  }
  // sticker
  let act = null;
  for (const [st, glyph] of UI.stk) if (t >= st && t < st + 1.7) act = [st, glyph];
  if (!act) { stkEl.style.opacity = '0'; }
  else {
    const [st, glyph] = act, u = t - st;
    if (stkEl.textContent !== glyph) stkEl.textContent = glyph;
    let sc, op;
    if (u < 0.32) { const k = u / 0.32; sc = 0.3 + 0.7 * (1 + 2.1 * Math.pow(k - 1, 3) + 1.1 * Math.pow(k - 1, 2) * 1); sc = 0.3 + 0.7 * k * (2 - k) * 1.12; op = k; }
    else if (u > 1.45) { const k = (u - 1.45) / 0.25; sc = 1 - 0.5 * k; op = 1 - k; }
    else { sc = 1; op = 1; }
    const fl = u > 0.35 && u <= 1.45 ? -9 * Math.sin(Math.min(1, (u - 0.35) / 0.55) * Math.PI / 2) : 0;
    stkEl.style.opacity = String(Math.max(0, Math.min(1, op)));
    stkEl.style.transform = `translateY(${fl}px) scale(${sc})`;
  }
  // poses: crossfade 0.22s on schedule
  let cur = UI.expr[0], prev = null;
  for (const e of UI.expr) { if (t >= e[0]) { prev = cur; cur = e; } }
  for (const name in poseEls) poseEls[name].style.opacity = '0';
  if (prev && prev !== cur && t - cur[0] < 0.22) {
    const k = (t - cur[0]) / 0.22;
    poseEls[cur[1]].style.opacity = String(k);
    poseEls[prev[1]].style.opacity = String(1 - k);
  } else {
    poseEls[cur[1]].style.opacity = '1';
  }
}
window.__drawUI = drawUI;
drawUI(0);
"""

CSS = """
.md-grain{display:none!important}
#root *{font-family:'Poppins',sans-serif!important}
:root{ --font-display:'Poppins',sans-serif; --font-body:'Poppins',sans-serif; }
html,body{width:1080px;height:1920px;background:#071410;overflow:hidden}
body{font-family:'Poppins',sans-serif}
#silk{position:absolute;inset:0;width:1080px;height:1920px}
#root{background:radial-gradient(1200px 800px at 50% 18%, #0C3A26 0%, #071410 62%)}
#bgpools{position:absolute;inset:0;opacity:.55;overflow:hidden}
.pool{position:absolute;border-radius:50%}
.p1{width:1050px;height:1050px;left:-260px;top:120px;background:radial-gradient(closest-side, rgba(53,217,154,.20), rgba(53,217,154,0) 72%)}
.p2{width:900px;height:900px;right:-300px;top:820px;background:radial-gradient(closest-side, rgba(20,140,90,.22), rgba(20,140,90,0) 72%)}
.p3{width:760px;height:760px;left:180px;top:1380px;background:radial-gradient(closest-side, rgba(255,201,60,.08), rgba(255,201,60,0) 72%)}
.spill{position:absolute;top:196px;left:76px;padding:16px 30px;border-radius:999px;
  font-size:28px;font-weight:700;letter-spacing:.16em;color:var(--ink)}
.sh{position:absolute;left:76px;width:932px;font-weight:800;font-size:66px;line-height:1.05;
  letter-spacing:-0.02em;color:var(--ink)}
#root .sh{white-space:normal}
h1.sh{top:296px} h2.sh{top:388px;font-size:66px}
.md-lit{color:#8CF5C8;text-shadow:0 0 30px rgba(14,159,110,.9)}
.scard{position:absolute;left:70px;top:560px;width:940px;height:660px;border-radius:34px;
  padding:44px 48px;box-sizing:border-box}
.hero{font-size:96px;line-height:1;text-align:center;margin-top:2px}
.big{font-size:88px;font-weight:800;text-align:center;color:var(--ink);letter-spacing:-0.02em;line-height:1.08;margin-top:10px}
.big .g{color:#8CF5C8}
.bigsub{text-align:center;font-size:36px;color:var(--muted);margin-top:12px;font-weight:600}
.rows{margin-top:30px;display:flex;flex-direction:column;gap:16px}
.srow{display:flex;align-items:center;gap:20px;background:rgba(255,255,255,.07);
  border:1px solid rgba(255,255,255,.13);border-radius:20px;padding:20px 28px;
  font-size:38px;font-weight:600;color:var(--ink)}
.srow .ric{font-size:40px}
.foot{position:absolute;left:48px;right:48px;bottom:34px;text-align:center;font-size:31px;color:var(--muted);font-weight:600}
.codewin{margin-top:26px;background:rgba(0,0,0,.38);border:1px solid rgba(255,255,255,.12);
  border-radius:18px;padding:22px 26px;font-family:'JetBrains Mono',monospace;font-size:31px;line-height:1.5;color:#CFE8DA}
.cline{white-space:nowrap} .cline .cn{display:inline-block;width:44px;color:#5F7A6B}
.xchip{margin:26px auto 0;width:fit-content;background:rgba(198,40,40,.18);border:1.5px solid rgba(255,90,80,.65);
  color:#FF9D94;font-weight:700;font-size:34px;padding:14px 30px;border-radius:999px}
.track{margin-top:44px;height:38px;border-radius:999px;background:rgba(255,255,255,.10);overflow:hidden}
.fill{height:100%;width:100%;transform-origin:left;background:linear-gradient(90deg,#0E9F6E,#35D99A);border-radius:999px}
.quote{font-size:56px;font-weight:700;line-height:1.25;color:var(--ink);text-align:center;margin-top:26px;padding:0 8px}
.lockplate{margin:34px auto 0;width:fit-content;display:flex;align-items:center;gap:22px;
  background:rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.14);border-radius:22px;padding:24px 36px;position:relative}
.lockic{font-size:64px} .blur-name{font-size:52px;font-weight:800;color:var(--ink);filter:blur(9px)}
.stamp{position:absolute;right:-24px;top:-22px;background:#C62828;color:#fff;font-weight:800;font-size:28px;
  letter-spacing:.14em;padding:8px 16px;border-radius:8px;transform:rotate(-12deg)}
.typewin{margin-top:28px;background:rgba(0,0,0,.38);border:1.5px solid rgba(140,245,200,.4);border-radius:18px;
  padding:26px 30px;font-size:44px;font-weight:600;color:var(--ink)}
.tprompt{color:#8CF5C8;margin-right:14px} .tch{opacity:0}
.caret{display:inline-block;width:5px;height:46px;background:#8CF5C8;margin-left:6px;vertical-align:-6px}
.reelmock{margin:30px auto 0;width:300px;height:300px;border-radius:26px;position:relative;overflow:hidden;
  background:linear-gradient(150deg,rgba(255,255,255,.16),rgba(255,255,255,.05));border:1px solid rgba(255,255,255,.16)}
.reelmock .play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:84px;color:rgba(242,251,245,.85)}
.wmband{position:absolute;left:-40px;right:-40px;top:198px;transform:rotate(-18deg);text-align:center;
  background:rgba(198,40,40,.55);color:#fff;font-weight:800;letter-spacing:.3em;font-size:30px;padding:8px 0}
.disc{width:118px;height:118px;border-radius:50%;margin:0 auto 18px;overflow:hidden;
  border:2px solid rgba(140,245,200,.55);box-shadow:0 0 60px -10px rgba(14,159,110,.65)}
.disc img{width:100%;height:100%;object-fit:cover}
.versus{display:flex;gap:22px;margin-top:6px}
.vplate{flex:1;border-radius:26px;padding:30px 22px;text-align:center;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.13)}
.vplate.good{border-color:rgba(140,245,200,.55);box-shadow:0 0 60px -12px rgba(14,159,110,.55)}
.vname{font-size:30px;font-weight:700;letter-spacing:.12em;color:var(--muted)}
.vprice{font-size:74px;font-weight:800;color:var(--ink);margin-top:10px}
.vprice span{font-size:32px;color:var(--muted)}
.vmark{margin-top:14px;font-size:33px;font-weight:700}
.vmark.no{color:#FF9D94} .vmark.ok{color:#8CF5C8}
.cta{margin:34px auto 0;width:fit-content;background:linear-gradient(180deg,#12B981,#0E9F6E);color:#fff;
  font-size:42px;font-weight:700;padding:24px 46px;border-radius:999px;box-shadow:0 24px 60px -14px rgba(14,159,110,.7)}
.pchips{display:flex;gap:16px;justify-content:center;margin-top:26px}
.pchip{background:rgba(140,245,200,.14);border:1.5px solid rgba(140,245,200,.5);color:#8CF5C8;
  font-size:36px;font-weight:700;padding:14px 28px;border-radius:999px}
#coinsGL{position:absolute;left:70px;top:560px;z-index:5;opacity:0;pointer-events:none}
.scard{z-index:2} .scard .big,.scard .pchips,.scard .foot{position:relative;z-index:6}
#brandpill{position:absolute;top:64px;left:50%;transform:translateX(-50%);z-index:40;
  padding:14px 30px;border-radius:999px;font-size:28px;font-weight:700;letter-spacing:.18em;color:var(--ink)}
#charzone{position:absolute;left:26px;top:1396px;width:196px;height:212px;z-index:40}
#charzone .pose{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}
#bubblezone{position:absolute;left:238px;top:1428px;width:792px;z-index:40}
.bubble{position:absolute;left:0;top:0;width:100%;box-sizing:border-box;opacity:0;
  background:rgba(234,247,239,.96);color:#0B3D2E;border-radius:26px;padding:26px 32px;
  font-size:47px;font-weight:600;line-height:1.3;box-shadow:0 30px 60px -20px rgba(0,0,0,.5)}
.bubble::after{content:'';position:absolute;left:-13px;top:52px;width:26px;height:26px;
  background:rgba(234,247,239,.96);transform:rotate(45deg)}
.bw{display:inline-block;margin-right:14px;color:#54655B}
.sticker{position:absolute;left:946px;top:1352px;z-index:41;width:92px;height:92px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-size:46px;opacity:0;
  background:rgba(255,255,255,.14);border:1.5px solid rgba(255,255,255,.35)}
"""

COINS_JS = """
// ---- rapier-baked coins, 2D canvas (cheap, deterministic) ----
const cobj = { t: 0 };
let coinsDraw = null;
try {
  const cv = document.getElementById('coinsGL');
  const ctx = cv.getContext('2d');
  const spr = document.createElement('canvas'); spr.width = spr.height = 128;
  const g = spr.getContext('2d');
  const grad = g.createRadialGradient(64, 58, 8, 64, 64, 62);
  grad.addColorStop(0, '#FFEFB0'); grad.addColorStop(0.55, '#FFC93C'); grad.addColorStop(1, '#D9930D');
  g.fillStyle = grad; g.beginPath(); g.arc(64, 64, 60, 0, 7); g.fill();
  g.lineWidth = 6; g.strokeStyle = '#A86E00'; g.stroke();
  g.fillStyle = '#8A5A00'; g.font = '800 62px Poppins, sans-serif';
  g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('₹', 64, 68);
  const halo = document.createElement('canvas'); halo.width = halo.height = 128;
  const hg = halo.getContext('2d');
  const hgrad = hg.createRadialGradient(64, 64, 10, 64, 64, 64);
  hgrad.addColorStop(0, 'rgba(255,201,60,0.55)'); hgrad.addColorStop(1, 'rgba(255,201,60,0)');
  hg.fillStyle = hgrad; hg.fillRect(0, 0, 128, 128);
  coinsDraw = (t) => {
    ctx.clearRect(0, 0, 940, 660);
    const F = window.COINS.frames, fi = Math.min(F.length - 2, Math.max(0, Math.floor(t * 60))), fr = Math.min(1, Math.max(0, t * 60 - fi));
    for (let k = 0; k < window.COINS.count; k++) {
      const a = F[fi].coins[k], b = F[fi + 1].coins[k];
      const c = a && b ? [a[0] + (b[0] - a[0]) * fr, a[1] + (b[1] - a[1]) * fr, a[2] + (b[2] - a[2]) * fr] : (a || b);
      if (!c) continue;
      const x = 30 + (c[0] + 4.4) * 100, y = 40 + c[1] * 100;
      ctx.save(); ctx.translate(x, y); ctx.rotate(-c[2]);
      ctx.globalAlpha = 0.5; ctx.drawImage(halo, -66, -66, 132, 132);
      ctx.globalAlpha = 1; ctx.drawImage(spr, -44, -44, 88, 88);
      ctx.restore();
    }
  };
} catch (e) { console.warn('coins off', e); }
if (coinsDraw) {
  tl.set('#coinsGL', { opacity: 1 }, 35.26);
  tl.to('#coinsGL', { opacity: 0, duration: 0.4 }, 39.55);
  window.__coinsDraw = (t) => { const lt = t - 35.26; if (lt >= 0 && lt <= 4.4) coinsDraw(lt); };
}
"""

POOL_JS = """
// ---- silk replacement: drifting gradient pools (cheap, seek-safe) ----
tl.fromTo('.p1', { x: 0, y: 0 }, { x: 130, y: 70, duration: 29.6, ease: 'sine.inOut', yoyo: true, repeat: 1 }, 0);
tl.fromTo('.p2', { x: 0, y: 0 }, { x: -110, y: -60, duration: 24.7, ease: 'sine.inOut', yoyo: true, repeat: 1 }, 0);
tl.fromTo('.p3', { x: 0, y: 0 }, { x: 80, y: -50, duration: 19.8, ease: 'sine.inOut', yoyo: true, repeat: 2 }, 0);
tl.to('#bgpools', { opacity: 0.8, duration: 4.0, ease: 'sine.inOut' }, 30.0);
tl.to('#bgpools', { opacity: 0.62, duration: 0.8, ease: 'sine.out' }, 35.28);
tl.to('#bgpools', { opacity: 0.34, duration: 1.2, ease: 'sine.out' }, 49.98);
"""

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/vendor/gsap.min.js"></script>
<link rel="stylesheet" href="assets/vendor/fonts.css">
<link rel="stylesheet" href="assets/brand.css" />
<link rel="stylesheet" href="assets/md.css" />
<link rel="stylesheet" href="assets/md-world.css" />
<link rel="stylesheet" href="assets/theme.css" />
<script src="assets/beats.js"></script>
<script src="assets/coins.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}"
     data-width="1080" data-height="1920" data-fps="50">
  <audio id="score" data-start="0" data-duration="{TOTAL}" data-volume="1" src="assets/final_mix.wav"></audio>
  <div id="bgpools"><div class="pool p1"></div><div class="pool p2"></div><div class="pool p3"></div></div>
  {''.join(sections)}
  <div id="brandpill" class="md-glass">✳ I.RAJ1801</div>
  <div id="charzone">{poses_html}</div>
  <div id="bubblezone"><div class="bubble" id="bubble"></div></div>
  <div class="sticker" id="sticker"></div>
  <div class="md-vignette"></div>
  <div class="md-grain"></div>
</div>
<script src="assets/md.js"></script>
<script src="assets/theme.js"></script>
<script>
const tl = gsap.timeline({{ paused: true }});
MD.lines(tl);
{POOL_JS}
{''.join(scene_js)}
{UI_JS}
{COINS_JS}
MD.finish(tl);
window.__frame = (t) => {{ tl.pause(t); if (window.__drawUI) window.__drawUI(t); if (window.__coinsDraw) window.__coinsDraw(t); }};
tl.eventCallback('onUpdate', () => {{ const t = tl.time(); if (window.__drawUI) window.__drawUI(t); if (window.__coinsDraw) window.__coinsDraw(t); }});
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</body>
</html>"""

(FILM / 'index.html').write_text(html)
print('film/index.html written:', len(html), 'bytes | poses:', len(POSES), '| phrases:', len(phrases))
