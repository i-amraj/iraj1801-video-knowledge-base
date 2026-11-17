import json, pathlib
SRC = json.load(open(pathlib.Path.home() / "workspace/gfx-v1/gfx_full_data.json"))
lines = SRC["lines"][:4]
data = {"lines": [{"start": L["start"], "dur": L["dur"], "env": L["env"],
                   "words": [{"w": w["w"], "s": w["s"], "e": w["e"]} for w in L["words"]]} for L in lines],
        "total": 15.0}
html = r"""<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:540px;height:960px;overflow:hidden;background:#F3E9DF;
 font-family:"Noto Sans",sans-serif;color:#16120F}
#stage{position:relative;width:540px;height:960px;
 background:
  radial-gradient(420px 300px at 18% 12%, rgba(217,191,166,.55), rgba(217,191,166,0) 70%),
  radial-gradient(520px 380px at 85% 30%, rgba(232,214,196,.6), rgba(232,214,196,0) 70%),
  radial-gradient(700px 500px at 50% 88%, rgba(201,162,126,.35), rgba(201,162,126,0) 70%),
  #F3E9DF}
#stage:before{content:"";position:absolute;inset:0;opacity:.5;
 background:repeating-conic-gradient(from -90deg at 50% 34%, rgba(184,103,74,.045) 0deg 4deg, transparent 4deg 9deg)}
#stage:after{content:"";position:absolute;inset:0;opacity:.35;
 background-image:radial-gradient(rgba(22,18,15,.13) 1px, transparent 1.4px);background-size:22px 22px}
.scene{position:absolute;inset:0;opacity:0;z-index:1}
#capzone{z-index:2}
#brand{z-index:2}
.pill{position:absolute;top:64px;left:50%;transform:translateX(-50%);white-space:nowrap;
 font-size:12.5px;font-weight:700;letter-spacing:2.6px;color:#5d4a38;
 border:1.4px solid rgba(93,74,56,.55);border-radius:999px;padding:7px 16px;background:rgba(255,255,255,.35)}
.head{position:absolute;top:104px;left:0;width:540px;text-align:center;font-family:"Noto Serif",serif}
.head .l1{font-size:41px;font-weight:800;line-height:1.16;color:#16120F}
.head .l2{font-size:41px;font-weight:800;line-height:1.16;font-style:italic;color:#B8674A;position:relative;display:inline-block}
.head .l2 .und{position:absolute;left:2%;bottom:-7px;width:96%;height:8px}
.head .w{display:inline-block}
.card{position:absolute;top:262px;left:50%;width:452px;height:392px;margin-left:-226px;
 background:rgba(255,255,255,.6);border:1px solid rgba(255,255,255,.85);border-radius:36px;
 box-shadow:0 24px 50px rgba(120,84,50,.20), inset 0 1px 0 rgba(255,255,255,.9);overflow:hidden}
.card .inner{position:absolute;inset:0;padding:26px 28px}
/* S1 phone */
.phone{width:172px;height:308px;margin:14px auto 0;border-radius:24px;background:#14161a;
 box-shadow:0 14px 30px rgba(20,20,20,.35);padding:12px 10px;position:relative}
.phone .notch{width:56px;height:7px;border-radius:4px;background:#2c2f36;margin:0 auto 10px}
.phone .pline{font-family:"Noto Serif",serif;font-size:16.5px;line-height:1.5;color:#5c6068;font-weight:600}
.phone .pline b{color:#fff;font-weight:800}
.phone .pline .hot{color:#ff9d5c}
.autobadge{position:absolute;right:-52px;top:118px;background:#B8674A;color:#fff;font-weight:800;
 font-size:13px;letter-spacing:1.4px;padding:8px 13px;border-radius:999px;box-shadow:0 8px 18px rgba(184,103,74,.45)}
/* S2 diagram */
.dia-t{font-size:12px;font-weight:800;letter-spacing:2.2px;color:#8a6f52;text-align:center;margin-bottom:16px}
.microw{display:flex;align-items:center;gap:16px}
.mic{width:58px;height:58px;border-radius:50%;background:#16120F;color:#fff;display:flex;align-items:center;justify-content:center;font-size:27px;flex:none}
.wave{display:flex;align-items:center;gap:3.5px;height:64px;flex:1}
.wave i{flex:1;background:#B8674A;border-radius:3px;min-height:4px}
.arrow{font-size:26px;color:#B8674A;font-weight:900;text-align:center;margin:12px 0 10px}
.chips{display:flex;flex-wrap:wrap;gap:7px;justify-content:center}
.chip{background:#16120F;color:#fff;font-size:14.5px;font-weight:700;padding:6px 11px;border-radius:9px;opacity:0}
.chip.hot{background:#B8674A}
.capstrip{margin-top:20px;background:#16120F;border-radius:13px;padding:12px 14px;font-family:"Noto Serif",serif;font-size:16.5px;font-weight:700;color:#fff;text-align:center;opacity:0}
.capstrip .hot{color:#ff9d5c}
/* S3 upload */
.upbox{border:2px dashed rgba(138,111,82,.5);border-radius:20px;padding:22px 18px;text-align:center;background:rgba(255,255,255,.5)}
.upicon{width:62px;height:62px;margin:0 auto;border-radius:50%;background:#B8674A;color:#fff;font-size:34px;display:flex;align-items:center;justify-content:center;font-family:"Noto Serif",serif;font-weight:800}
.filechip{display:inline-block;margin-top:10px;background:#16120F;color:#fff;font-size:14px;font-weight:700;padding:7px 14px;border-radius:9px}
.upbar{height:13px;border-radius:8px;background:rgba(22,18,15,.12);margin-top:20px;overflow:hidden}
.upbar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#d98a63,#B8674A);border-radius:8px}
.uppct{font-family:"Noto Serif",serif;font-size:29px;font-weight:800;margin-top:12px}
.upstat{font-size:13.5px;color:#7a6752;font-weight:700;margin-top:2px}
/* S4 timeline */
.tl-t{font-size:12px;font-weight:800;letter-spacing:2.2px;color:#8a6f52;text-align:center;margin-bottom:14px}
.tlwave{display:flex;align-items:flex-end;gap:3px;height:56px;margin:0 4px}
.tlwave i{flex:1;background:rgba(22,18,15,.28);border-radius:3px;min-height:4px}
.track{position:relative;height:118px;margin-top:16px;background:rgba(22,18,15,.06);border-radius:14px}
.playhead{position:absolute;top:6px;bottom:6px;width:3px;background:#B8674A;border-radius:2px;left:0}
.blk{position:absolute;top:38px;height:42px;background:#16120F;color:#fff;border-radius:8px;
 font-size:12.5px;font-weight:700;display:flex;align-items:center;justify-content:center;opacity:0;padding:0 4px;overflow:hidden;white-space:nowrap}
.blk.hot{background:#B8674A}
.tlcap{text-align:center;font-size:13.5px;color:#7a6752;font-weight:700;margin-top:12px}
/* caption zone */
#capzone{position:absolute;left:0;bottom:118px;width:540px;display:flex;justify-content:center;align-items:flex-end;gap:10px;padding:0 26px}
#avatar{width:54px;height:54px;border-radius:50%;background:#16120F;color:#F3E9DF;flex:none;
 display:flex;align-items:center;justify-content:center;font-family:"Noto Serif",serif;font-size:25px;font-weight:800;
 border:2.5px solid #B8674A;box-shadow:0 8px 18px rgba(120,84,50,.3)}
#bubble{background:#fff;border-radius:18px;box-shadow:0 12px 26px rgba(120,84,50,.18);
 padding:13px 17px;font-family:"Noto Serif",serif;font-size:19.5px;font-weight:700;line-height:1.35;max-width:400px;min-height:56px}
#bubble .cw{display:inline-block}
#bubble .hot{color:#B8674A;font-style:italic}
#brand{position:absolute;bottom:66px;left:0;width:540px;text-align:center;font-size:12px;font-weight:700;letter-spacing:2.2px;color:#8a6f52}
</style></head><body>
<div id="stage"></div>
<script>
const DATA = __DATA__;
const $=s=>document.querySelector(s);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const lerp=(a,b,k)=>a+(b-a)*k;
const eoc=x=>1-Math.pow(1-x,3);
const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const eob=x=>{const c=1.70158,c3=c+1;return 1+c3*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
// spring-ish pop: 0->1 with overshoot to 1.1 settle (damping ~10 feel)
const pop=x=>x<=0?0:x>=1?1:1+ (Math.sin(Math.min(x*2.2,Math.PI)*0.5)*0.0) + (eob(x)-1)*0 + lerp(0,1,eob(x));
const SCENES=[
 {t0:0,t1:2.88,pill:"FREE AUTO CAPTIONS",l1:"Captions haath se",l2:"NAHI likhe!",kw:["NAHI"]},
 {t0:2.88,t1:7.54,pill:"KAAM KAISE KARTA HAI",l1:"Ek FREE tool khud",l2:"captions bana deta hai",kw:["FREE","captions"]},
 {t0:7.54,t1:10.21,pill:"STEP 1 · UPLOAD",l1:"Bas apni video",l2:"upload karo",kw:["upload"]},
 {t0:10.21,t1:15.0,pill:"STEP 2 · AUTO SYNC",l1:"Har shabd apni",l2:"sahi jagah par",kw:["shabd","sahi"]},
];
const stage=$('#stage');
SCENES.forEach((S,i)=>{
 const d=document.createElement('div');d.className='scene';d.id='sc'+i;
 d.innerHTML=`<div class="pill">${S.pill}</div>
 <div class="head"><div class="l1">${S.l1.split(' ').map(w=>`<span class="w">${w}</span>`).join(' ')}</div>
 <span class="l2"><span class="fill">${S.l2}</span><svg class="und" viewBox="0 0 100 8" preserveAspectRatio="none"><path d="M1 5 Q 25 1 50 4 T 99 3" stroke="#B8674A" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".65"/></svg></span></div>
 <div class="card"><div class="inner" id="in${i}"></div></div>`;
 stage.appendChild(d);
});
// card contents
$('#in0').innerHTML=`<div class="phone"><div class="notch"></div><div class="pline" id="pline"></div>
 <div class="autobadge" id="autob">AUTO ✦</div></div>`;
$('#in1').innerHTML=`<div class="dia-t">MIC → AWAAZ → CAPTIONS</div>
 <div class="microw"><div class="mic">🎙</div><div class="wave" id="wv"></div></div>
 <div class="arrow">↓</div><div class="chips" id="chips"></div>
 <div class="capstrip" id="capstrip">Ye captions maine haath se <span class="hot">NAHI</span> likhe!</div>`;
$('#in2').innerHTML=`<div class="upbox"><div class="upicon">↑</div>
 <div class="filechip">🎬 meri-reel.mp4</div>
 <div class="upbar"><i id="upfill"></i></div><div class="uppct" id="uppct">0%</div>
 <div class="upstat" id="upstat">Upload ho raha hai…</div></div>`;
$('#in3').innerHTML=`<div class="tl-t">HAR SHABD → SAHI JAGAH</div>
 <div class="tlwave" id="tlw"></div>
 <div class="track" id="track"><div class="playhead" id="ph"></div></div>
 <div class="tlcap">Tool khud sunke har shabd bitha deta hai</div>`;
// caption zone
const cz=document.createElement('div');cz.id='capzone';
cz.innerHTML=`<div id="avatar">R</div><div id="bubble"></div>`;stage.appendChild(cz);
const br=document.createElement('div');br.id='brand';br.textContent='✳ I.RAJ1801';stage.appendChild(br);
// build chips (S2) from V2 caption words (first 7 of line 2 words minus connectors)
const L=DATA.lines;
const chipWords=["Ek","free","tool","awaaz","sunke","word-by-word","captions"];
chipWords.forEach(w=>{const c=document.createElement('span');c.className='chip'+((w==='free'||w==='captions')?' hot':'');c.textContent=w;$('#chips').appendChild(c)});
// waveform bars S2 from env of line2
const env2=L[1].env, NB=26;
for(let i=0;i<NB;i++){const b=document.createElement('i');b.id='wb'+i;$('#wv').appendChild(b)}
// timeline wave S4 from env of line4
const env4=L[3].env;
for(let i=0;i<NB;i++){const b=document.createElement('i');const v=env4[Math.floor(i*env4.length/NB)]||0.2;b.style.height=(12+v*44)+'px';$('#tlw').appendChild(b)}
// S4 blocks from words 6.. of line 4 (har shabd ko sahi jagah par bitha dega)
const blkWords=L[3].words.slice(6);
blkWords.forEach(w=>{const b=document.createElement('div');b.className='blk'+((w.w==='shabd'||w.w==='sahi')?' hot':'');b.textContent=w.w;$('#track').appendChild(b)});
// S1 phone karaoke words
L[0].words.forEach(w=>{const s=document.createElement('span');s.textContent=w.w+' ';if(w.w==='NAHI')s.dataset.hot='1';$('#pline').appendChild(s)});
// caption phrases: groups of 3 words per line
const phrases=[];
L.forEach((ln,li)=>{for(let i=0;i<ln.words.length;i+=3)phrases.push({li,words:ln.words.slice(i,i+3)})});
const KW=new Set(["NAHI","free","FREE","captions","upload","shabd","sahi","tool"]);
function sceneAt(t){for(let i=SCENES.length-1;i>=0;i--)if(t>=SCENES[i].t0)return i;return 0}
function seek(t){
 const si=sceneAt(t), S=SCENES[si];
 SCENES.forEach((Sx,i)=>{
   const el=$('#sc'+i);let o=0;
   if(i===si){o=eio(clamp((t-Sx.t0)/0.3,0,1)); if(Sx.t1<15)o*=1-eio(clamp((t-(Sx.t1-0.3))/0.3,0,1))*0; }
   else if(i===si-1&&t<Sx.t1+0.3){o=1-eio(clamp((t-Sx.t1+0.02)/0.3,0,1));}
   el.style.opacity=o;
   const sc=1+ (i===si? 0.035*clamp((t-Sx.t0)/(Sx.t1-Sx.t0),0,1):0);
   el.querySelector('.card').style.transform=`scale(${sc})`;
   el.style.visibility=o<=0.001?'hidden':'visible';
 });
 // headline anim
 const lt=t-S.t0, head=$('#sc'+si+' .head');
 head.querySelectorAll('.l1 .w').forEach((w,i)=>{const k=eoc(clamp((lt-0.05-i*0.06)/0.3,0,1));w.style.opacity=k;w.style.transform=`translateY(${(1-k)*10}px)`});
 const l2=$('#sc'+si+' .l2');const gk=clamp((lt-0.35)/0.45,0,1);
 l2.style.opacity=0.25+0.75*eio(gk);
 l2.style.color=gk<1?`rgba(184,103,74,${0.35+0.65*gk})`:'#B8674A';
 l2.style.filter=gk<1?`grayscale(${1-gk})`:'none';
 // S1 karaoke
 if(si===0){const ws=L[0].words;
   document.querySelectorAll('#pline span').forEach((s,i)=>{const on=t>=ws[i].s;s.style.color=on?(s.dataset.hot?'#ff9d5c':'#fff'):'#5c6068';s.style.fontWeight=on?'800':'600'});
   const ab=$('#autob');const k=eob(clamp((t-1.8)/0.35,0,1));ab.style.opacity=k;ab.style.transform=`scale(${0.6+0.4*k})`;
 }
 // S2 wave + chips
 if(si===1){const ln=L[1];const env=ln.env;
   for(let i=0;i<NB;i++){const idx=clamp(Math.floor((t-ln.start)/ln.dur*env.length),0,env.length-1);const v=env[clamp(idx-Math.floor((NB-1-i)*0),0,env.length-1)]||0.15;
     const local=env[clamp(Math.floor(((t-ln.start)/ln.dur)*(env.length)) - (NB-1-i),0,env.length-1)]||0.15;
     $('#wb'+i).style.height=(6+local*56)+'px';$('#wb'+i).style.opacity=t<ln.start?0.35:1}
   const cs=$('#capstrip');const ck=eoc(clamp((t-6.35)/0.4,0,1));cs.style.opacity=ck;cs.style.transform=`translateY(${(1-ck)*10}px)`;
   const chipT=[2.95,3.3,3.62,4.35,4.95,5.6,6.15];
   document.querySelectorAll('#chips .chip').forEach((c,i)=>{const k=eob(clamp((t-chipT[i])/0.3,0,1));c.style.opacity=k;c.style.transform=`scale(${0.5+0.5*k}) translateY(${(1-k)*8}px)`});
 }
 // S3 upload
 if(si===2){const ln=L[2];const p=eio(clamp((t-ln.start-0.15)/(ln.dur-0.3),0,1));
   $('#upfill').style.width=(p*100)+'%';$('#uppct').textContent=Math.round(p*100)+'%';
   $('#upstat').textContent=p>=1?'Upload ho gaya ✓':'Upload ho raha hai…';$('#upstat').style.color=p>=1?'#3d9970':'#7a6752';
 }
 // S4 timeline
 if(si===3){const ln=L[3];const p=clamp((t-ln.start)/ln.dur,0,1);
   $('#ph').style.left=(4+p*94)+'%';
   const bw=100/blkWords.length;
   document.querySelectorAll('#track .blk').forEach((b,i)=>{const w=blkWords[i];const k=eob(clamp((t-w.s)/0.28,0,1));
     b.style.opacity=k;b.style.left=(2+i*bw*0.94)+'%';b.style.width=(bw*0.88)+'%';b.style.transform=`translateY(${(1-k)*-16}px) scale(${0.7+0.3*k})`});
 }
 // caption bubble: current phrase
 let cur=null;for(const p of phrases){if(t>=p.words[0].s-0.02)cur=p}
 const bub=$('#bubble');
 if(cur){const key=cur.li+'-'+cur.words[0].s;
   if(bub.dataset.k!==key){bub.dataset.k=key;bub.innerHTML=cur.words.map(w=>`<span class="cw${KW.has(w.w)?' hot':''}" data-s="${w.s}">${w.w}</span>`).join(' ')}
   bub.querySelectorAll('.cw').forEach(el=>{const s=parseFloat(el.dataset.s);const k=eob(clamp((t-s)/0.32,0,1));
     el.style.transform=`scale(${t>=s?1+0.1*Math.sin(clamp((t-s)/0.32,0,1)*Math.PI):1})`;el.style.opacity=t>=s-0.02?1:0.28});
 } else bub.innerHTML='';
}
window.seek=seek;seek(0);
</script></body></html>"""
out = pathlib.Path.home() / "workspace/gfx-mukku/mukku.html"
out.write_text(html.replace("__DATA__", json.dumps(data)), encoding="utf-8")
print("mukku.html written", out.stat().st_size)
