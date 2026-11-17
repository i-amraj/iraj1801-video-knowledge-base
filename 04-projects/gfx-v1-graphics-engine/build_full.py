import json, pathlib
BASE = pathlib.Path.home() / "workspace/gfx-v1"
DATA = json.dumps(json.load(open(BASE / "gfx_full_data.json")), ensure_ascii=False)

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
.tag{position:absolute;top:-17px;left:28px;background:#ff8a3c;color:#14100a;font-size:15px;font-weight:800;letter-spacing:2px;padding:6px 14px;border-radius:8px;z-index:20}
#resCard{top:296px;width:452px;margin-left:-226px;padding:30px 30px 26px}
#vidArea{height:216px;border-radius:16px;background:linear-gradient(135deg,#23304d,#131a2c);position:relative;overflow:hidden}
#vidArea .tri{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:0;height:0;border-left:34px solid rgba(255,255,255,.92);border-top:21px solid transparent;border-bottom:21px solid transparent}
#vidArea .vtag{position:absolute;top:12px;left:14px;background:rgba(0,0,0,.45);color:#ffd9ae;font-size:13px;font-weight:700;padding:4px 10px;border-radius:6px;letter-spacing:1px}
#resCap{margin-top:22px;min-height:88px;text-align:center;font-size:29px;font-weight:800;line-height:1.35;color:#fff}
#resCap .un,#finCap .un{color:#5c6068}
#resCap .acc,#finCap .acc{color:#ff8a3c}
#diaCard{top:288px;width:488px;margin-left:-244px;padding:34px 24px 28px}
#diaRow{display:flex;align-items:center;gap:12px}
#micWrap{text-align:center;width:84px}
#micIco{width:74px;height:74px;border-radius:50%;background:#171a20;border:2px solid #2c313c;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:34px}
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
#tlCard{top:288px;width:488px;margin-left:-244px;padding:36px 28px 30px}
#tlWave{display:flex;align-items:flex-end;gap:3px;height:64px;margin-bottom:22px}
#tlWave i{flex:1;background:#2c3446;border-radius:3px;display:block}
#tlWave i.on{background:#5b6b8c}
#tlTrack{position:relative;height:64px;background:#171a20;border:2px solid #2c313c;border-radius:14px}
#tlHead{position:absolute;top:-8px;bottom:-8px;width:4px;background:#ff8a3c;border-radius:2px;left:0}
.tlBlk{position:absolute;top:10px;height:44px;background:#232833;border:2px solid #3a4152;border-radius:9px;color:#fff;font-size:13.5px;font-weight:700;display:flex;align-items:center;justify-content:center;opacity:0;transform:translateY(-16px)}
.tlBlk.acc{border-color:#ff8a3c;color:#ffb37a}
#tlNote{margin-top:20px;text-align:center;font-size:20px;font-weight:700;color:#c8ccd4}
#tlNote .org{color:#ff8a3c}
#styCard{top:278px;width:472px;margin-left:-236px;padding:36px 30px 30px}
#styPrev{background:#171a20;border:2px solid #2c313c;border-radius:16px;padding:26px 18px;text-align:center;min-height:118px;display:flex;align-items:center;justify-content:center}
#styText{font-size:27px;font-weight:800;color:#fff;line-height:1.35;transition:none}
#styText .acc{color:#ff8a3c}
#styRow{display:flex;gap:10px;justify-content:center;margin-top:22px}
.fchip{background:#1d2129;border:2px solid #343a47;color:#9aa0ad;font-size:16px;font-weight:800;letter-spacing:1px;padding:9px 16px;border-radius:999px}
.fchip.on{border-color:#ff8a3c;color:#fff;background:#2a2118}
#dotRow{display:flex;gap:14px;justify-content:center;margin-top:18px}
.dot{width:30px;height:30px;border-radius:50%;border:3px solid transparent}
.dot.on{border-color:#fff;transform:scale(1.15)}
#finCard{top:262px;width:452px;margin-left:-226px;padding:30px 30px 26px}
#finCap{margin-top:20px;min-height:80px;text-align:center;font-size:27px;font-weight:800;line-height:1.35;color:#fff}
#statRow{display:flex;gap:10px;margin-top:18px}
.stat{flex:1;background:#171c26;border:2px solid #2e4a2a;border-radius:14px;padding:12px 4px;text-align:center;opacity:0;transform:scale(.6)}
.stat b{display:block;font-size:21px;color:#3ddc84}
.stat span{font-size:13.5px;color:#c8ccd4;font-weight:700}
#sumCard{top:272px;width:472px;margin-left:-236px;padding:36px 32px 32px}
#sumTitle{text-align:center;font-size:26px;font-weight:800;color:#fff;margin-bottom:24px}
#sumTitle .org{color:#ff8a3c}
.srow{display:flex;align-items:center;gap:16px;background:#171a20;border:2px solid #2c313c;border-radius:16px;padding:16px 18px;margin-bottom:14px}
.snum{width:40px;height:40px;border-radius:50%;background:#23262e;color:#fff;font-size:19px;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none}
.stxt{font-size:21px;font-weight:700;color:#e8eaf0;flex:1}
.stick{width:34px;height:34px;border-radius:50%;background:#23262e;color:#3ddc84;font-size:19px;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none;opacity:.25}
.srow.done{border-color:#2e4a2a}
.srow.done .snum{background:#ff8a3c;color:#14100a}
.srow.done .stick{opacity:1;background:#17351f}
#ctaHead{position:absolute;top:128px;width:100%;text-align:center;font-size:41px;font-weight:800;color:#fff;line-height:1.25}
#ctaHead .org{color:#ff8a3c}
#ctaCard{top:300px;width:452px;margin-left:-226px;padding:32px 30px 30px}
#cmtRow{display:flex;gap:12px;align-items:center}
#ava{width:46px;height:46px;border-radius:50%;background:linear-gradient(135deg,#ffb37a,#ff8a3c);flex:none;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;color:#14100a}
#cmtBox{flex:1;background:#171a20;border:2px solid #343a47;border-radius:999px;padding:13px 20px;font-size:22px;font-weight:700;color:#fff;min-height:56px}
#cmtBox .ph{color:#5c6068;font-weight:500}
#caret{display:inline-block;width:3px;height:22px;background:#ff8a3c;vertical-align:-3px;margin-left:2px}
#cmtBtn{margin-top:20px;background:#ff8a3c;color:#14100a;text-align:center;font-size:21px;font-weight:800;padding:14px;border-radius:14px}
#folChip{margin:22px auto 0;width:fit-content;background:#1b1d23;border:2px solid #343a47;color:#fff;font-size:19px;font-weight:800;padding:11px 22px;border-radius:999px}
#folChip .org{color:#ff8a3c}
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

<div class="scene" id="scD">
 <div class="card" id="tlCard"><div class="tag">STEP 2</div>
  <div id="tlWave"></div>
  <div id="tlTrack"><div id="tlHead"></div></div>
  <div id="tlNote">Har shabd, <span class="org">sahi jagah</span> par</div>
 </div>
</div>

<div class="scene" id="scE">
 <div class="card" id="styCard"><div class="tag">STEP 3</div>
  <div id="styPrev"><div id="styText">Ye captions maine haath se <span class="acc">NAHI</span> likhe</div></div>
  <div id="styRow"><span class="fchip" id="fc0">BOLD</span><span class="fchip" id="fc1">CLASSIC</span><span class="fchip" id="fc2">OUTLINE</span></div>
  <div id="dotRow"><span class="dot" id="dt0" style="background:#ffffff"></span><span class="dot" id="dt1" style="background:#ff8a3c"></span><span class="dot" id="dt2" style="background:#ffd23c"></span></div>
 </div>
</div>

<div class="scene" id="scF">
 <div class="card" id="finCard"><div class="tag">FINAL RESULT</div>
  <div id="vidArea"><div class="vtag">▶ REEL.mp4</div><div class="tri"></div></div>
  <div id="finCap"></div>
  <div id="statRow">
   <div class="stat"><b>0</b><span>typing</span></div>
   <div class="stat"><b>2 min</b><span>me ready</span></div>
   <div class="stat"><b>100%</b><span>FREE</span></div>
  </div>
 </div>
</div>

<div class="scene" id="scG">
 <div class="card" id="sumCard"><div class="tag">SUMMARY</div>
  <div id="sumTitle">Teen steps <span class="org">yaad kar lo</span></div>
  <div class="srow" id="sr0"><div class="snum">1</div><div class="stxt">Video upload karo</div><div class="stick">✓</div></div>
  <div class="srow" id="sr1"><div class="snum">2</div><div class="stxt">Auto captions banao</div><div class="stick">✓</div></div>
  <div class="srow" id="sr2"><div class="snum">3</div><div class="stxt">Apna style lagao</div><div class="stick">✓</div></div>
 </div>
</div>

<div class="scene" id="scH">
 <div id="ctaHead">Tool ka naam + link<br><span class="org">bilkul FREE</span></div>
 <div class="card" id="ctaCard"><div class="tag">COMMENT KARO</div>
  <div id="cmtRow"><div id="ava">R</div><div id="cmtBox"><span class="ph" id="cmtTxt">Comment likho…</span><span id="caret"></span></div></div>
  <div id="cmtBtn">Comment karo ➤</div>
  <div id="folChip">＋ Follow · <span class="org">@i.raj1801</span></div>
 </div>
</div>

<div id="capZone"><div id="capText"></div></div>

<script>
const DATA = __DATA__;
const $ = id => document.getElementById(id);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const easeOut=p=>1-Math.pow(1-p,3);
const easeIO=p=>p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
const L=DATA.lines, V1=L[0], V2=L[1], V3=L[2], V4=L[3], V5=L[4], V6=L[5], V7=L[6], V8=L[7], TOT=DATA.total;
const wave=$("wave"); const NB=16; const bars=[];
for(let i=0;i<NB;i++){const b=document.createElement("i"); b.style.height="8px"; wave.appendChild(b); bars.push(b);}
const chips=$("chips");
V1.words.forEach(w=>{const s=document.createElement("span"); s.className="chipw"+(w.w==="NAHI"?" acc":""); s.textContent=w.w; chips.appendChild(s);});
const chipEls=[...chips.children];
// Beat D: mini waveform + timeline blocks (V1 words on the track)
const tlW=$("tlWave"); const TB=36; const tbars=[];
for(let i=0;i<TB;i++){const b=document.createElement("i"); b.style.height="8px"; tlW.appendChild(b); tbars.push(b);}
const track=$("tlTrack"); const TW=488-56-4;
const tblks=V1.words.map((w,i)=>{const d=document.createElement("div"); d.className="tlBlk"+(w.w==="NAHI"?" acc":"");
  const bw=Math.max(44,w.w.length*8.2+16); d.style.width=bw+"px"; d.textContent=w.w; track.appendChild(d); return d;});
// distribute block positions across the track
{let x=8; const gap=(TW-16-tblks.reduce((a,d)=>a+parseFloat(d.style.width),0))/Math.max(1,tblks.length-1);
 tblks.forEach(d=>{d.style.left=x+"px"; x+=parseFloat(d.style.width)+gap;});}
const statEls=[...document.querySelectorAll(".stat")];
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
const wStart=(line,txt)=>{const w=line.words.find(w=>w.w.toLowerCase()===txt.toLowerCase()); return w?w.s:line.start+line.dur*0.5;};
window.seek=function(t){
  $("bar").style.width=(t/TOT*100)+"%";
  const vA=sceneVis("scA",t,0,V2.start), vB=sceneVis("scB",t,V2.start,V3.start), vC=sceneVis("scC",t,V3.start,V4.start),
        vD=sceneVis("scD",t,V4.start,V5.start), vE=sceneVis("scE",t,V5.start,V6.start), vF=sceneVis("scF",t,V6.start,V7.start),
        vG=sceneVis("scG",t,V7.start,V8.start), vH=sceneVis("scH",t,V8.start,0);
  const cur=L.find(l=>t>=l.start&&t<=l.start+l.dur)||null;
  if(vA) karaoke($("resCap"),V1,t,"NAHI");
  if(vB){
    const lt=clamp((t-V2.start)/0.05,0,V2.env.length-1)|0;
    bars.forEach((b,i)=>{const e=V2.env[clamp(lt-(NB-1-i),0,V2.env.length-1)]||0;
      b.style.height=(6+e*86)+"px"; b.className=(t>=V2.start&&e>=0.06)?"on":"";});
    const capW=V2.words.find(w=>w.w==="captions"); const wbW=V2.words.find(w=>w.w==="word-by-word");
    const c0=wbW?wbW.s:V2.start+2.2, c1=capW?capW.e:V2.start+3.4;
    chipEls.forEach((c,i)=>{const ct=c0+(c1-c0)*(i/(chipEls.length-1||1));
      const p=clamp((t-ct)/0.16,0,1); c.style.opacity=p; c.style.transform="scale("+(0.6+0.4*easeOut(p))+")";});
  }
  if(vC){ const p=easeIO(clamp((t-V3.start)/1.9,0,1));
    $("fill").style.width=(p*100)+"%";
    $("upStatus").innerHTML=p>=1?'Upload ho gaya <span class="grn">✓</span>':"Upload ho raha hai… "+Math.round(p*100)+"%";
  }
  if(vD){
    const lt=clamp((t-V4.start)/0.05,0,V4.env.length-1)|0;
    tbars.forEach((b,i)=>{const idx=clamp(Math.round(i*(V4.env.length-1)/(TB-1))-(TB-1-lt>0?0:0),0,V4.env.length-1);
      const e=V4.env[clamp(lt-Math.round((TB-1-i)*V4.env.length/TB/8),0,V4.env.length-1)]||0;
      b.style.height=(6+e*54)+"px"; b.className=e>=0.06?"on":"";});
    const p=clamp((t-V4.start)/V4.dur,0,1); $("tlHead").style.left=(8+p*(TW-16))+"px";
    const s0=wStart(V4,"shabd");
    tblks.forEach((d,i)=>{const bt=s0+(V4.start+V4.dur-s0-0.3)*(i/(tblks.length-1||1));
      const q=clamp((t-bt)/0.18,0,1); d.style.opacity=q; d.style.transform="translateY("+(-16*(1-easeOut(q)))+"px) scale("+(0.85+0.15*easeOut(q))+")";});
  }
  if(vE){
    const fT=wStart(V5,"font"), rT=wStart(V5,"rang");
    const st=$("styText");
    if(t>=rT+0.55){ st.style.fontSize="29px"; st.style.letterSpacing="0"; st.innerHTML='Ye captions maine haath se <span class="acc">NAHI</span> likhe'; }
    else if(t>=rT){ st.style.fontSize="29px"; st.innerHTML='Ye captions maine haath se <span style="color:#ffd23c">NAHI</span> likhe'; }
    else if(t>=fT){ st.style.fontSize="29px"; st.innerHTML='Ye captions maine haath se <span class="acc">NAHI</span> likhe'; }
    else { st.style.fontSize="27px"; st.innerHTML='Ye captions maine haath se <span class="acc">NAHI</span> likhe'; }
    $("fc0").className="fchip"+(t>=fT?" on":""); $("fc1").className="fchip"+(t<fT?" on":""); $("fc2").className="fchip";
    $("dt0").className="dot"+(t<rT?" on":""); $("dt1").className="dot"+(t>=rT+0.55?" on":""); $("dt2").className="dot"+(t>=rT&&t<rT+0.55?" on":"");
  }
  if(vF){ karaoke($("finCap"),V6,t,"NAHI");
    statEls.forEach((sEl,i)=>{const st6=V6.start+V6.dur*(0.42+i*0.2); const q=clamp((t-st6)/0.2,0,1);
      sEl.style.opacity=q; sEl.style.transform="scale("+(0.6+0.4*easeOut(q))+")";});
  }
  if(vG){
    const keys=["upload","captions","style"];
    keys.forEach((k,i)=>{const kt=wStart(V7,k); $("sr"+i).className="srow"+(t>=kt?" done":"");});
  }
  if(vH){
    const toolW=V8.words.find(w=>w.w==="TOOL"); const tT=toolW?toolW.s:V8.start+2.4;
    const typed=clamp((t-tT)/0.55,0,1); const n=Math.floor(typed*4);
    const cmt=$("cmtTxt");
    if(t<tT){ cmt.textContent="Comment likho…"; cmt.className="ph"; }
    else { cmt.textContent="TOOL".slice(0,Math.max(1,n)); cmt.className=""; }
    $("caret").style.opacity=(Math.floor(t*2.2)%2===0)?"1":"0.15";
    const folW=V8.words.find(w=>w.w==="Follow"); const fT2=folW?folW.s:V8.start+4.4;
    const pulse=t>=fT2?1+0.05*Math.sin((t-fT2)*6):1;
    $("folChip").style.transform="scale("+pulse+")"; $("folChip").style.borderColor=t>=fT2?"#ff8a3c":"#343a47";
  }
  const zone=$("capText");
  if(vA||vF){zone.innerHTML="";}
  else{ const ph=phrase(cur,t);
    if(ph&&cur) zone.innerHTML=ph.words.map(w=>'<span class="'+(t>=w.e?"":(t>=w.s?"":"un"))+'">'+w.w+"</span>").join(" ");
    else zone.innerHTML="";
  }
};
</script></body></html>'''

html = HTML.replace("__DATA__", DATA)
open(BASE / "full.html", "w", encoding="utf-8").write(html)
print("full.html written", len(html))
