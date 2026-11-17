# Raj IG Comment Agent — apna webhook system (koi third-party nahi)

Comment aate hi **kuch seconds me** auto public reply, aur comment/DM me **STICK**
likhne par repo ka link private DM me. ManyChat wala hi tareeka (Meta webhook +
official API), bas server apna hai — Cloudflare Worker (free) par chalta hai,
code aur secrets Raj ke apne GitHub/Cloudflare accounts me rehte hain.

## Kaise kaam karta hai
1. Koi comment karta hai → Meta turant hamare Worker ko webhook bhejta hai
2. Worker signature check karta hai (nakli signal reject)
3. Public reply bhejta hai; STICK ho to private DM me repo link bhi
4. Dedupe + 24h cooldown + hourly cap — loop/spam impossible
5. Token (60 din wala) roz apne aap refresh hota hai

## Raj ke MANUAL steps (sirf ye tumhe karne hain — baaki sab mera)

### Step 1 — Instagram account taiyaar (phone app, 2 minute)
- @i.raj1801 → Settings → **Account type: Creator me switch** karo (isse account public bhi ho jayega — webhook ke liye dono zaroori hain)
- Settings → Messages → **"Allow access to messages" ON**

### Step 2 — Meta app (browser, ~15 minute)
- developers.facebook.com → developer account banao (Facebook login se)
- **Create app** → use case: **Manage messaging & content on Instagram**
- App ke andar **Instagram → API setup with Instagram login**:
  - **Add account** → @i.raj1801 login → 3 permissions do:
    `instagram_business_basic`, `instagram_business_manage_messages`, `instagram_business_manage_comments`
  - Wahi se copy karo: **Instagram user ID**, **Access token**, **Instagram app secret**
- Ek apna **VERIFY_TOKEN** banao (koi bhi random lamba string)
- App Settings → Basic me **Privacy Policy URL** ke liye Worker ke `/privacy` page ka URL lagega (deploy ke baad)

### Step 3 — Cloudflare (free account, ~10 minute)
- cloudflare.com par free account banao
- Is repo ko apne GitHub me daalo, phir Cloudflare → Workers → is repo se deploy
  (ya terminal se `npx wrangler login && npx wrangler deploy`)
- Worker → Settings → Variables and Secrets me 4 secrets daalo:
  `VERIFY_TOKEN`, `IG_APP_SECRET`, `IG_USER_ID`, `IG_ACCESS_TOKEN`
  (ye chat me kisi ko mat bhejna — seedha Cloudflare me daalne hain)
- KV namespace banao aur `wrangler.toml` me uski id daalo

### Step 4 — Webhook jodo (Meta app me)
- Instagram use case → Webhooks: Callback URL = `https://<worker-url>/webhook`,
  Verify token = wahi VERIFY_TOKEN, field: **comments** (+ messages)
- Account-level subscription: browser me ye URL kholo (token chat me nahi jayega):
  `https://<worker-url>/admin/subscribe?key=<VERIFY_TOKEN>`
  → `{"success": true}` aana chahiye

### Step 5 — Test, phir live
- Pehle `DRY_RUN = "true"` hi rahe: dusre account se reel par **STICK** comment karo
  → Cloudflare Logs me match dikhega, kuch send nahi hoga
- Sab sahi lage to `wrangler.toml` me `DRY_RUN = "false"` karke commit → live
- Test comment par DM kuch seconds me aa jana chahiye

## Zaroori niyam/sachai
- **App Review NAHI chahiye** — app sirf Raj ke apne account par chalegi (Standard Access kaafi hai)
- Per comment sirf **1 private reply**, 7 din ke andar (Meta ka niyam)
- DM auto-reply sirf tab jab banda khud pehle message kare (24h window)
- Private/personal account par webhook aata hi nahi — isliye Creator + public zaroori hai
- Graph API version `worker.js` ke CONFIG me hai (`v25.0`); Meta purana version band kare to wahi badalna hai

## Rules badalna
`worker.js` ke upar CONFIG block me: keyword, DM ka text, public reply templates,
cooldown, hourly cap. GitHub par edit → commit → apne aap deploy.
