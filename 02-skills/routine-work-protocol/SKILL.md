---
name: routine_work_protocol
description: Nikki ka apna routine-kaam system. Script first-pass review, QC checklist, lessons distillation, lambi file ke summary jaise repeatable kaam ek pakke protocol se Nikki khud karti hai. Hermes 2026-11-17 ko Raj ke order par poori tarah band — ab koi kaam Hermes ke paas nahi jayega. Faisle, production, ChatGPT loop aur Raj Gate iske bahar hain.
---

# Routine Work Protocol — Nikki ka apna system (Hermes backup)

Raj approved 2026-11-17; **usi din ~07:59 Raj ne Hermes ko poori tarah band kar diya** — "ab hum Hermes ke paas nahi jayenge." Iska maksad: third-party (Hermes + free model quota) par nirbharta khatam — routine kaam ka tareeka apni skill me band hai, aur kaam bhi Nikki khud karti hai, Hermes ki seekh aur niyam apna kar.

## Route (pakka)
- **Saara routine kaam ab Nikki khud karti hai** — koi Hermes call nahi, koi bahari model nahi.
- Hermes se jo seekha (Rounds 1–9 ke niyam, neeche) wo is protocol ki reedh hai — kaam karne wala badal gaya, tareeka wahi pakka wala hai.
- Manager-jaanch (Kadam 3) ab apne hi kaam par lagu hoti hai — khud ka kaam bhi saboot se hi pass hoga.

## Protocol (har routine kaam par, dono routes par)
1. **Brief file me likho** — kaam, file paths, quality standard, aur "jawab file me likho" saaf-saaf. Tukdon me brief nahi.
2. **Kaam sirf diye hue steps me** — scope se bahar kuch nahi, apni taraf se kuch jodna nahi.
3. **Manager jaanch (lazmi — skip nahi, dono routes par):**
   - Har number/value **asal file se grep/read** karke milao. Banaya hua number = FAIL.
   - Visual daava sirf **rendered frame** se. Code me hona saboot nahi (Visual Proof Rule).
   - Floating/satah ka hisaab: center − aadhi unchai = neeche wala kinara; world position = group offset + local — dono gin kar dekho.
   - File sach me badli hai ya nahi: **size + content dono** dekho. Purani report chipki ho to FAIL.
4. **Report** — har daave ke saath saboot (file path, size, frame). Jo verify nahi hua, saaf likho "verify nahi hua" — lekin jo khud gin sakte ho use ginna lazmi hai; "verify nahi hua" bhaagne ka bahana nahi.
5. **Seekh darj karo** — jo galti/sudhaar mile, usi time lessons me (lane lessons + daily note). Seekh likhna hi asal "training" hai — model koi bhi ho, seekh file me rehti hai.

## Pakke niyam (Hermes Training Rounds 1–9 se distilled)
- **Quote rule:** number sirf file se; yaad se kabhi nahi.
- **Visual Proof Rule:** PASS = frame me dikhe.
- **Confirmation rule:** pehle file me karke dikhao, phir kaho.
- **Mahaul-badlav = background + props + character** — teeno ginno (din ke scene me character ke haath ka jalta lantern bhi raat ka element hai).
- **Direction lock:** simple 2D character (gol face) + real rich 3D background. Quality standard = Begunkodar `opus_v2` frame.
- **Naam sahi:** Ricks Clips — koi aur naam nahi.
- **Report kabhi purani copy nahi** — har baar naye sire se, maujooda file se mila kar.

## Seema
- Ye protocol ChatGPT approval loop ya Raj Approval Gate ki jagah NAHI hai.
- Publish niyam, Colab niyam, AUTO-PUSH niyam — saare standing rules waise hi lagu.
- Faisle aur production Muse par hi rahenge; ye system sirf routine kaam ki nirbharta khatam karta hai.
