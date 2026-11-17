import json, pathlib
BASE = pathlib.Path.home() / "workspace/gfx-v1"
DATA = json.dumps(json.load(open(BASE / "gfx_data.json")), ensure_ascii=False)

HTML = '''<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:540px;height:960px;overflow:hidden;font-family:"Segoe UI",Arial,sans-serif;background:#060607}
#grid{position:absolute;left:-60px;right:-60px;bottom:0;height:300px;opacity:.5;
 background:linear-gradient(180deg,rgba(38,44,66,0) 0%,rgba(38,44,66,.25) 100%),
 repeating-linear-gradient(90deg,rgba(70,84,130,.20) 0 2px,transparent 2px 54px),
 repeating-linear-gradient(0deg,rgba(70,84,130,.20) 0 2px,transparent 2px 54px);
 transform:perspective(420px) rotateX(58deg);transform-origin:bottom}
#bar{position:absolute;top:0;left:0;height:6px;background:#ff8a3c;width:0;z-index:40}
#pill{position:absolute;top:30px;left:50%;transform:translateX(-50%);background:#1b1d23;color:#e8eaf0;font-size:17px;font-weight:700;letter-spacing:1.5px;padding:9px 20px;border-radius:999px;z-index:30;white-space:nowrap}
#pill .ast{color:#ff8a3c}
.scene{position:absolute;inset:0;opacity:0}
.hookQ{position:absolute;top:118px;width:100%;text-align:center;font-size:47px;font-weight:800;color:#fff;line-height:1.22}
.hookQ .org{color:#ff8a3c}
.card{position:absolute;left:50%;background:#101216;border:2px solid #262a33;border-radius:28px;box-shadow:0 26px 60px rgba(0,0,0,.55)}
.tag{position:absolute;top:-17px;left:28px;background:#ff8a3c;color:#14100a;font-size:15px;font-weight:800;letter-spacing:2px;padding:6px 14px;border-radius:8px}
#resCard{top:296px;width:452px;margin-left:-226px;padding:30px 30px 26px}
#vidArea{height:216px;border-radius:16px;background:linear-gradient(135deg,#23304d,#131a2c);position:relative;overflow:hidden}
#vidArea .tri{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:0;height:0;border-left:34px solid rgba(255,255,255,.92);border-top:21px solid transparent;border-bottom:21px solid transparent}
#vidArea .vtag{position:absolute;top:12px;left:14px;background:rgba(0,0,0,.45);color:#ffd9ae;font-size:13px;font-weight:700;padding:4px 10px;border-radius:6px;letter-spacing:1px}
#resCap{margin-top:22px;min-height:88px;text-align:center;font-size:29px;font-weight:800;line-height:1.35;color:#fff}
#resCap .un{color:#5c6068}
#resCap .acc{color:#ff8a3c}
#diaCard{top:288px;width:488px;margin-left:-244px;padding:34px 24px 28px}
#diaRow{display:flex;align-items:center;gap:12px}
#micWrap{text-align:center;width:84px}
#micIco{width:74px;height:74px;border-radius:50%;background:#171a20;border:2px solid #2c313c;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:40px}
.diaLbl{margin-top:10px;font-size:14px;font-weight:800;letter-spacing:2px;color:#9aa0ad}
#wave{display:flex;align-items:center;gap:2px;height:96px;width:96px;flex:none}
#wave i{width:4px;flex:none;background:#3a4152;border-radius:3px;display:block}
#wave i.on{background:#ff8a3c}
#arrow{font-size:26px;color:#ff8a3c;font-weight:800}
#chipBox{flex:none;width:188px}
#chips{display:grid;grid-template-columns:1fr 1fr;gap:7px;width:188px}
.chipw{background:#1d2129;border:2px solid #343a47;color:#fff;font-size:15.5px;font-weight:700;padding:6px 4px;border-radius:10px;opacity:0;transform:scale(.6);text-align:center}
.chipw.acc{border-color:#ff8a3c;color:#ffb37a}
#diaNote{margin-top:20px;text-align:center;font-size:20px;font-weight:700;color:#c8ccd4}
#diaNote .org{color:#ff8a3c}
#upCard{top:286px;width:452px;margin-left:-226px;padding:36px 34px 32px;text-align:center}
#upIco{font-size:52px}
#fileChip{margin:18px auto 4px;background:#1d2129;border:2px solid #343a47;border-radius:14px;padding:13px 16px;font-size:21px;font-weight:700;color:#e8eaf0}
#trk{height:16px;background:#23262e;border-radius:99px;overflow:hidden;margin-top:20px}
#fill{height:100%;width:0;background:linear-gradient(90deg,#ffb37a,#ff8a3c);border-radius:99px}
#upStatus{margin-top:18px;font-size:22px;font-weight:800;color:#fff;min-height:30px}
#upStatus .grn{color:#3ddc84}
#capZone{position:absolute;left:0;right:0;top:792px;padding:0 36px;text-align:center;z-index:35}
#capText{font-size:31px;font-weight:800;line-height:1.35;color:#fff}
#capText .un{color:#5c6068}
#capText .acc{color:#ff8a3c}
</style></head><body>
<div id="grid"></div><div id="bar"></div>
<div id="pill"><span class="ast">✳</span> i.raj1801</div>

<div class="scene" id="scA">
 <div class="hookQ">Captions <span class="org">FREE</span> me<br>auto bante hain?</div>
 <div class="card" id="resCard"><div class="tag">RESULT</div>
  <div id="vidArea"><div class="vtag">▶ REEL.mp4</div><div class="tri"></div></div>
  <div id="resCap"></div>
 </div>
</div>

<div class="scene" id="scB">
 <div class="card" id="diaCard"><div class="tag">KAAM KAISE KARTA HAI</div>
  <div id="diaRow">
   <div id="micWrap"><div id="micIco">🎙️</div><div class="diaLbl">AWAAZ</div></div>
   <div id="wave"></div>
   <div id="arrow">➜</div>
   <div id="chipBox"><div id="chips"></div><div class="diaLbl">CAPTIONS</div></div>
  </div>
  <div id="diaNote">Awaaz sunke, <span class="org">word-by-word</span> captions</div>
 </div>
</div>

<div class="scene" id="scC">
 <div class="card" id="upCard"><div class="tag">STEP 1</div>
  <div id="upIco">⬆️</div>
  <div id="fileChip">📄 meri-reel.mp4</div>
  <div id="trk"><div id="fill"></div></div>
  <div id="upStatus">Upload ho raha hai…</div>
 </div>
</div>

<div id="capZone"><div id="capText"></div></div>

<script>
const DATA = __DATA__;
const $ = id => document.getElementById(id);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const easeOut=p=>1-Math.pow(1-p,3);
const easeIO=p=>p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
const L=DATA.lines, V1=L[0], V2=L[1], V3=L[2], TOT=DATA.total;
// waveform bars
const wave=$("wave"); const NB=16; const bars=[];
for(let i=0;i<NB;i++){const b=document.createElement("i"); b.style.height="8px"; wave.appendChild(b); bars.push(b);}
// chips = V1 words
const chips=$("chips");
V1.words.forEach(w=>{const s=document.createElement("span"); s.className="chipw"+(w.w==="NAHI"?" acc":""); s.textContent=w.w; chips.appendChild(s);});
const chipEls=[...chips.children];
function sceneVis(id,t,a,b){
  const el=$(id); const fi=easeOut(clamp((t-a)/0.22,0,1)), fo=b?1-easeOut(clamp((t-(b-0.22))/0.22,0,1)):1;
  const o=Math.min(fi,fo); el.style.opacity=o; el.style.transform="scale("+(0.985+0.015*o)+")"; return o>0.02;
}
function karaoke(el,line,t,accWord){
  if(!line){el.innerHTML="";return;}
  el.innerHTML=line.words.map(w=>{
    const cls=t>=w.e?"":(t>=w.s?"":"un");
    const acc=(accWord&&w.w===accWord)?"acc":"";
    return '<span class="'+(acc||cls)+'">'+w.w+"</span>";
  }).join(" ");
}
function phrase(line,t){
  if(!line||t<line.start)return null;
  const ws=line.words; let gi=ws.findIndex(w=>t<w.e); if(gi<0)gi=ws.length-1;
  const gStart=Math.floor(gi/4)*4;
  return {words:ws.slice(gStart,gStart+4)};
}
window.seek=function(t){
  $("bar").style.width=(t/TOT*100)+"%";
  const vA=sceneVis("scA",t,0,V2.start), vB=sceneVis("scB",t,V2.start,V3.start), vC=sceneVis("scC",t,V3.start,0);
  const cur=L.find(l=>t>=l.start&&t<=l.start+l.dur)||null;
  // Beat A: result-card karaoke = V1 itself
  if(vA) karaoke($("resCap"),V1,t,"NAHI");
  // Beat B: waveform from V2 envelope + chips land on "word-by-word captions" span
  if(vB){
    const lt=clamp((t-V2.start)/0.05,0,V2.env.length-1)|0;
    bars.forEach((b,i)=>{const e=V2.env[clamp(lt-(NB-1-i),0,V2.env.length-1)]||0;
      b.style.height=(6+e*86)+"px"; b.className=t>=V2.start? "on":""; if(e<0.06)b.className="";});
    const capW=V2.words.find(w=>w.w==="captions"); const wbW=V2.words.find(w=>w.w==="word-by-word");
    const c0=wbW?wbW.s:V2.start+2.2, c1=capW?capW.e:V2.start+3.4;
    chipEls.forEach((c,i)=>{const ct=c0+(c1-c0)*(i/(chipEls.length-1||1));
      const p=clamp((t-ct)/0.16,0,1); c.style.opacity=p; c.style.transform="scale("+(0.6+0.4*easeOut(p))+")";});
  }
  // Beat C: upload progress over V3
  if(vC){ const p=easeIO(clamp((t-V3.start)/1.9,0,1));
    $("fill").style.width=(p*100)+"%";
    $("upStatus").innerHTML=p>=1?'Upload ho gaya <span class="grn">✓</span>':"Upload ho raha hai… "+Math.round(p*100)+"%";
  }
  // Bottom karaoke: current phrase (skip during Beat A — the card carries it)
  const zone=$("capText");
  if(vA){zone.innerHTML="";}
  else{ const ph=phrase(cur,t);
    if(ph&&cur) zone.innerHTML=ph.words.map(w=>'<span class="'+(t>=w.e?"":(t>=w.s?"":"un"))+'">'+w.w+"</span>").join(" ");
    else zone.innerHTML="";
  }
};
</script></body></html>'''

html = HTML.replace("__DATA__", DATA)
open(BASE / "gfx.html", "w", encoding="utf-8").write(html)
print("gfx.html written", len(html))
