/**
 * Raj IG Comment Agent — apna khud ka webhook system (koi third-party service nahi)
 * ----------------------------------------------------------------------------------
 * Kaam: Instagram par comment aate hi (Meta webhook se, kuch seconds me)
 *   1. Public reply (comment ke neeche) — har comment par, ghumte hue templates se
 *   2. Comment me "STICK" keyword ho to usi bande ko private DM me GitHub repo link
 *   3. Koi DM me "STICK" likhe to wahan bhi repo link auto-reply
 *
 * Chalta hai: Cloudflare Worker (free) par. Data/secrets sirf Raj ke apne infra me.
 * IG credentials KV me rehte hain (keys: ig_token, ig_user_id, ig_app_secret) —
 * /admin/ingest form se bhare jate hain taaki chat/report me kabhi na aayein.
 * Cloudflare secrets: sirf VERIFY_TOKEN (Meta webhook + admin pages ki chabi).
 * Vars (wrangler.toml): DRY_RUN ("true" = sirf log, kuch send nahi), APP_NAME, CONTACT_EMAIL
 */

// ============================================================================
// CONFIG — rules yahin badlo. Dobara deploy karne par live ho jayega.
// ============================================================================
const CONFIG = {
  graphVersion: "v25.0",
  // Token System User (EAB...) hai jo Meta ke Unified Login se bana hai —
  // ye sirf graph.facebook.com par chalta hai, graph.instagram.com par NAHI.
  graphHost: "graph.facebook.com",

  // ---- Rewards (v11): har reel ka apna inaam ----
  // Comment kis media (reel/post) par aaya, usi hisaab se greeting + delivery
  // badalta hai. Media -> reward ki mapping KV key "media_rewards" (JSON) me
  // rehti hai — /admin/mapmedia se bina redeploy ke badal sakte hain.
  // Koi mapping na mile to defaultReward wala jata hai.
  defaultReward: "stickman",
  rewards: {
    stickman: {
      greeting:
        "Hey there! 🙏 Comment ke liye dhanyavaad.\n" +
        "FREE Stickman Video Skill ke details chahiye to neeche wala button dabao 👇",
      cardTitle: "Ye lo, jaise vaada tha! 🎉",
      cardSubtitle:
        "FREE Stickman Video Skill — neeche wala button dabao, seedha GitHub repo khulega. Script likho, apne AI agent ko do, aur MP4 ready. — Raj",
      buttonTitle: "GitHub Repo 🔗",
      link: "https://github.com/i-amraj/free_stick_man_video_skill",
      deliverText:
        "Ye lo, jaise vaada tha! 🎉\n\nFREE Stickman Video Skill ka GitHub repo:\n{link}\n\n" +
        "Script likho, apne AI agent ko do, aur MP4 ready. Koi dikkat aaye to isi DM me reply kar dena. — Raj",
    },
    tools: {
      greeting:
        "Hey there! 🙏 Comment ke liye dhanyavaad.\n" +
        "FREE AI Tools (Qwen AI + Fliki AI) ke pure links aur poora process chahiye to neeche wala button dabao 👇",
      cardTitle: "Ye lo, jaise vaada tha! 🎉",
      cardSubtitle:
        "FREE AI Tools — Qwen AI aur Fliki AI ke official links + poora step-by-step process ek hi jagah. Button dabao 👇",
      buttonTitle: "AI Tools Guide 🔗",
      link: "https://github.com/i-amraj/free-ai-tools",
      deliverText:
        "Ye lo, jaise vaada tha! 🎉\n\nFREE AI Tools (Qwen AI + Fliki AI) ke links aur poora process:\n{link}\n\n" +
        "Koi dikkat aaye to isi DM me reply kar dena. — Raj",
    },
    captions: {
      greeting:
        "Hey there! 🙏 Comment ke liye dhanyavaad.\n" +
        "FREE Auto Captions tool (Edits by Instagram) ka naam, link aur poora 3-step process chahiye to neeche wala button dabao 👇",
      cardTitle: "Ye lo, jaise vaada tha! 🎉",
      cardSubtitle:
        "FREE Auto Captions Guide — Edits by Instagram (Meta ka free app, Hindi captions, no watermark) ka official link + poora process. Button dabao 👇",
      buttonTitle: "Captions Tool Guide 🔗",
      link: "https://github.com/i-amraj/free-auto-captions",
      deliverText:
        "Ye lo, jaise vaada tha! 🎉\n\nFREE Auto Captions (Edits by Instagram) ka poora guide:\n{link}\n\n" +
        "Koi dikkat aaye to isi DM me reply kar dena. — Raj",
    },
  },

  // Keyword rule: DM me ye shabd aaye to wahi follow-gate flow shuru hoga
  keyword: "STICK",
  keywordPublicReplies: [
    "Hello! Main Bunty hoon, Raj ka personal agent 🤖 DM me details bhej diye hain, check karo 📩",
    "Hi! Bunty here, Raj ka personal agent 🤖 Details tumhare DM me hain 🔗",
  ],

  // ---- Follow-gate flow (ManyChat style, apna system) ----
  // Comment -> greeting DM (button: "Send me the details")
  // Button -> follow check (API se sach me check hota hai)
  // Follow hai -> repo link deliver; nahi hai -> profile wala nudge, dobara check
  profileUrl: "https://www.instagram.com/i.raj1801",
  gateButtonText: "Send me the details",
  gateNotFollowing:
    "Oh no! 😅 Lagta hai tum mujhe abhi follow nahi kar rahe.\n" +
    "Pehle follow kar lo, phir neeche \"I'm following ✅\" dabao — link turant bhej dunga 👇",

  // Baaki saare comments ke liye public replies (rotation me chalenge)
  // Raj ka order: har reply me Bunty ka short intro (Raj ka personal agent)
  generalPublicReplies: [
    "Hello! Main Bunty hoon, Raj ka personal agent 🤖 Dhanyavaad comment ke liye! 🙏",
    "Hi! Bunty here, Raj ka personal agent 🤖 Thank you so much! ❤️",
    "Hello dost! Main Bunty hoon, Raj ka personal agent 🤖 Shukriya! 🙌",
    "Hey! Bunty bol raha hai, Raj ka personal agent 🤖 Bahut badhiya! 🔥",
  ],

  cooldownHours: 24, // ek hi bande ko keyword-DM dobara itne ghanto tak nahi
  hourlyPublicReplyCap: 60, // suraksha cap: ek ghante me isse zyada public reply nahi
};

// ============================================================================
// Helpers
// ============================================================================
const enc = new TextEncoder();

async function hmacSha256Hex(secret, bodyText) {
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(bodyText));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function pick(list, seedStr) {
  let h = 0;
  for (let i = 0; i < seedStr.length; i++) h = (h * 31 + seedStr.charCodeAt(i)) >>> 0;
  return list[h % list.length];
}

// IG credentials: pehle KV, phir env fallback
async function igConfig(env) {
  if (env._cfg) return env._cfg;
  let kv = {};
  try {
    kv = {
      token: await env.STATE.get("ig_token"),
      userId: await env.STATE.get("ig_user_id"),
      secret: await env.STATE.get("ig_app_secret"),
    };
  } catch (_) {}
  env._cfg = {
    token: kv.token || env.IG_ACCESS_TOKEN || "",
    userId: kv.userId || env.IG_USER_ID || "",
    secret: kv.secret || env.IG_APP_SECRET || "",
  };
  return env._cfg;
}

async function graphPost(env, path, jsonBody) {
  const cfg = await igConfig(env);
  const res = await fetch(`https://${CONFIG.graphHost}/${CONFIG.graphVersion}${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${cfg.token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(jsonBody),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Graph ${path} -> ${res.status}: ${text.slice(0, 300)}`);
  return text;
}

// Public reply: comment ke neeche jawab
async function publicReply(env, commentId, message) {
  return graphPost(env, `/${commentId}/replies`, { message });
}

// Private reply: comment karne wale ko ek DM (Meta ka niyam: per comment sirf 1, 7 din ke andar)
async function privateReplyToComment(env, commentId, messageObj) {
  const cfg = await igConfig(env);
  return graphPost(env, `/${cfg.userId}/messages`, {
    recipient: { comment_id: commentId },
    message: messageObj,
  });
}

// Normal DM (jab banda khud DM kare aur 24h window khuli ho)
async function dmSend(env, userId, messageObj) {
  const cfg = await igConfig(env);
  return graphPost(env, `/${cfg.userId}/messages`, {
    recipient: { id: userId },
    message: messageObj,
  });
}

// ---- Rewards: media/user ke hisaab se sahi inaam chunna ----
async function rewardKeyForMedia(env, mediaId) {
  if (mediaId) {
    try {
      const map = JSON.parse((await env.STATE.get("media_rewards")) || "{}");
      if (map[mediaId] && CONFIG.rewards[map[mediaId]]) return map[mediaId];
    } catch (_) {}
  }
  return CONFIG.defaultReward;
}

async function rewardForMedia(env, mediaId) {
  return CONFIG.rewards[await rewardKeyForMedia(env, mediaId)];
}

// User ne aakhri baar kis media par comment kiya tha — wahi reward DM me milega
async function rewardForUser(env, userId) {
  let mediaId = "";
  try {
    mediaId = (await env.STATE.get(`usermedia:${userId}`)) || "";
  } catch (_) {}
  return rewardForMedia(env, mediaId);
}

// ---- Follow-gate flow ke messages ----
function gateGreetingMessage(reward) {
  return {
    text: reward.greeting,
    quick_replies: [
      { content_type: "text", title: CONFIG.gateButtonText, payload: "GET_DETAILS" },
    ],
  };
}

function gateDeliverMessage(reward) {
  // Link button ki tarah jayega — dabate hi seedha document khulega
  return {
    attachment: {
      type: "template",
      payload: {
        template_type: "generic",
        elements: [
          {
            title: reward.cardTitle,
            subtitle: reward.cardSubtitle,
            buttons: [
              { type: "web_url", url: reward.link, title: reward.buttonTitle },
            ],
          },
        ],
      },
    },
  };
}

function gateDeliverFallbackMessage(reward) {
  return { text: reward.deliverText.replace("{link}", reward.link) };
}

function gateNudgeMessage() {
  // Card (template) do button ke saath: Visit Profile (link) + I'm following (postback).
  // Postback pehle nahi aata tha kyunki Meta app subscription me messaging_postbacks
  // field hi on nahi tha — 2026-11-14 ko on + live-verify ho gaya, ab card chalega.
  // Saath me quick-reply chip bhi hai (backup rasta).
  return {
    quick_replies: [
      { content_type: "text", title: "I'm following ✅", payload: "IM_FOLLOWING" },
    ],
    attachment: {
      type: "template",
      payload: {
        template_type: "generic",
        elements: [
          {
            title: "Ek chhota sa step bacha hai 👀",
            subtitle: CONFIG.gateNotFollowing,
            buttons: [
              { type: "web_url", url: CONFIG.profileUrl, title: "Visit Profile" },
              { type: "postback", title: "I'm following ✅", payload: "IM_FOLLOWING" },
            ],
          },
        ],
      },
    },
  };
}

function gateNudgeFallbackMessage() {
  // Card kisi wajah se fail ho to saada text + chip (profile URL text me)
  return {
    text:
      "Ek chhota sa step bacha hai 👀\n\n" +
      CONFIG.gateNotFollowing +
      "\n\n👉 Profile: " +
      CONFIG.profileUrl,
    quick_replies: [
      { content_type: "text", title: "I'm following ✅", payload: "IM_FOLLOWING" },
    ],
  };
}

// Sach me check: kya ye banda account ko follow karta hai?
// Meta ke User Profile API ka field: is_user_follow_business
async function checkFollows(env, userIgsid) {
  const cfg = await igConfig(env);
  const res = await fetch(
    `https://${CONFIG.graphHost}/${CONFIG.graphVersion}/${userIgsid}?fields=is_user_follow_business`,
    { headers: { Authorization: `Bearer ${cfg.token}` } }
  );
  if (!res.ok) {
    console.log(`follow check failed ${res.status}: ${(await res.text()).slice(0, 200)}`);
    return null; // pata nahi chala
  }
  const data = await res.json();
  return data.is_user_follow_business === true;
}

// Button dabne par: follow hai to link, nahi to nudge (baar-baar chalega)
async function runGateStep(env, userId, reward) {
  const follows = await checkFollows(env, userId);
  if (follows === true) {
    try {
      await dmSend(env, userId, gateDeliverMessage(reward));
    } catch (e) {
      console.log(`gate deliver template failed (${e.message}), text fallback bhej raha hoon`);
      await dmSend(env, userId, gateDeliverFallbackMessage(reward));
    }
    console.log(`gate: delivered link to ${userId}`);
  } else {
    try {
      await dmSend(env, userId, gateNudgeMessage());
    } catch (e) {
      console.log(`gate nudge card failed (${e.message}), text fallback bhej raha hoon`);
      await dmSend(env, userId, gateNudgeFallbackMessage());
    }
    console.log(`gate: nudge sent to ${userId} follows=${follows}`);
  }
}

function hasKeyword(text) {
  if (!text) return false;
  const re = new RegExp(`(^|[^A-Za-z])${CONFIG.keyword}([^A-Za-z]|$)`, "i");
  return re.test(text);
}

// ============================================================================
// Event handlers
// ============================================================================
async function handleComment(env, value, dryRun) {
  const cfg = await igConfig(env);
  const commentId = value.id;
  const from = value.from || {};
  const authorId = String(from.id || "");
  const username = from.username || "";
  const text = value.text || "";

  if (!commentId) return;
  if (authorId && cfg.userId && authorId === String(cfg.userId)) {
    console.log(`skip self comment=${commentId}`);
    return; // apne hi comment/reply par dobara reply = loop, isliye skip
  }

  // Dedupe: ek comment par ek hi baar kaam (webhook kabhi-kabhi dobara aata hai)
  const doneKey = `done:${commentId}`;
  if (await env.STATE.get(doneKey)) {
    console.log(`skip duplicate comment=${commentId}`);
    return;
  }

  const keywordHit = hasKeyword(text);
  // Ye comment kis reel/post par aaya — usi ka reward is bande ko milega
  const mediaId = String(value?.media?.id || "");
  const reward = await rewardForMedia(env, mediaId);
  console.log(
    `comment comment=${commentId} media=${mediaId} author=@${username} keyword=${keywordHit} actions=reply+gate text="${text.slice(0, 80)}"${dryRun ? " [DRY_RUN]" : ""}`
  );
  if (dryRun) return;

  // Hourly safety cap (sirf public reply par)
  const hourKey = `cap:${new Date().toISOString().slice(0, 13)}`;
  const used = parseInt((await env.STATE.get(hourKey)) || "0", 10);
  if (used >= CONFIG.hourlyPublicReplyCap) {
    console.log(`cap reached, skip comment=${commentId}`);
    return;
  }

  // 1) Public reply — HAR comment par
  const replyText = keywordHit
    ? pick(CONFIG.keywordPublicReplies, commentId)
    : pick(CONFIG.generalPublicReplies, commentId);
  await publicReply(env, commentId, replyText);
  await env.STATE.put(hourKey, String(used + 1), { expirationTtl: 3700 });

  // 2) Follow-gate ki shuruaat: greeting DM + "Send me the details" button
  //    (har comment par; ek hi bande ko cooldown ke andar dobara nahi)
  if (authorId) {
    // Bande ki aakhri media yaad rakho — DM gate wahi reward dega (7 din)
    if (mediaId) {
      await env.STATE.put(`usermedia:${authorId}`, mediaId, {
        expirationTtl: 7 * 24 * 3600,
      });
    }
    const coolKey = `cool:gate:${authorId}`;
    if (await env.STATE.get(coolKey)) {
      console.log(`gate cooldown active, DM skip author=@${username}`);
    } else {
      try {
        await privateReplyToComment(env, commentId, gateGreetingMessage(reward));
      } catch (e) {
        console.log(`greeting with button failed (${e.message}), plain text bhej raha hoon`);
        await privateReplyToComment(env, commentId, { text: reward.greeting });
      }
      await env.STATE.put(coolKey, "1", {
        expirationTtl: CONFIG.cooldownHours * 3600,
      });
      console.log(`gate greeting sent author=@${username} comment=${commentId}`);
    }
  }

  await env.STATE.put(doneKey, "1", { expirationTtl: 7 * 24 * 3600 });
}

async function handleMessage(env, event, dryRun) {
  const cfg = await igConfig(env);
  const senderId = String(event?.sender?.id || "");
  if (!senderId || (cfg.userId && senderId === String(cfg.userId))) return;
  if (event?.message?.is_echo) return;

  // Button taps: quick reply (message ke andar) ya postback (card button)
  let payload =
    event?.message?.quick_reply?.payload || event?.postback?.payload || "";
  // Kuch taps payload ki jagah sirf button ka text bankar aate hain — unhe bhi pehchano
  const rawText = (event?.message?.text || "").trim();
  if (!payload && rawText === CONFIG.gateButtonText) payload = "GET_DETAILS";
  if (!payload && /i'?m following|i am following/i.test(rawText)) {
    payload = "IM_FOLLOWING";
  }
  if (payload === "GET_DETAILS" || payload === "IM_FOLLOWING") {
    console.log(`gate step payload=${payload} user=${senderId}${dryRun ? " [DRY_RUN]" : ""}`);
    if (dryRun) return;
    await runGateStep(env, senderId, await rewardForUser(env, senderId));
    return;
  }

  // Pehchan na aaye to shape log karo (agli baar ki jaanch ke liye)
  if (!event?.message && !event?.postback) {
    console.log(
      `msg event other user=${senderId} keys=${Object.keys(event || {}).join(",")}`
    );
  } else if (rawText) {
    console.log(`msg event text user=${senderId} text="${rawText.slice(0, 60)}"`);
  }

  // DM me STICK likhe to wahi gate flow (greeting + button) shuru karo
  const text = event?.message?.text || "";
  if (hasKeyword(text)) {
    console.log(`dm keyword user=${senderId}${dryRun ? " [DRY_RUN]" : ""}`);
    if (dryRun) return;
    const coolKey = `cool:gate:${senderId}`;
    if (await env.STATE.get(coolKey)) return;
    await dmSend(env, senderId, gateGreetingMessage(await rewardForUser(env, senderId)));
    await env.STATE.put(coolKey, "1", {
      expirationTtl: CONFIG.cooldownHours * 3600,
    });
    console.log(`gate greeting sent (DM) user=${senderId}`);
  }
  // Baaki DM baaton par auto-reply nahi — wo Raj khud dekhega
}

// ============================================================================
// Token refresh (roz cron se): 60-day token expire hone se pehle naya KV me
// ============================================================================
async function refreshToken(env) {
  const cfg = await igConfig(env);
  if (!cfg.token) return;
  // System User token (EAB...) kabhi expire nahi hota — refresh ki zaroorat nahi
  if (cfg.token.startsWith("EAB")) {
    console.log("token refresh skipped: system user token");
    return;
  }
  const res = await fetch(
    `https://${CONFIG.graphHost}/refresh_access_token?grant_type=ig_refresh_token&access_token=${encodeURIComponent(cfg.token)}`
  );
  if (!res.ok) {
    console.log(`token refresh failed: ${res.status} ${await res.text()}`);
    return;
  }
  const data = await res.json();
  if (data.access_token) {
    await env.STATE.put("ig_token", data.access_token);
    console.log("token refreshed ok");
  }
}

// ============================================================================
// Admin pages
// ============================================================================
function ingestForm(key) {
  return new Response(
    `<!doctype html><meta charset="utf-8"><title>IG credentials ingest</title>` +
      `<h2>Raj IG Comment Agent — credentials</h2>` +
      `<form method="POST" action="/admin/ingest?key=${encodeURIComponent(key)}">` +
      `<p>Instagram User ID (digits)<br><input name="ig_user_id" size="40" required></p>` +
      `<p>Instagram Access Token (long-lived)<br><textarea name="ig_access_token" rows="3" cols="60" required></textarea></p>` +
      `<p>Instagram App Secret (32 hex)<br><input name="ig_app_secret" size="40" required></p>` +
      `<p><button type="submit">Save to Worker</button></p></form>`,
    { headers: { "Content-Type": "text/html; charset=utf-8" } }
  );
}

// ============================================================================
// Worker entry
// ============================================================================
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const dryRun = String(env.DRY_RUN || "true") === "true";

    if (url.pathname === "/health") {
      const cfg = await igConfig(env);
      return Response.json({
        ok: true,
        dryRun,
        instagram: Boolean(cfg.userId && cfg.token && cfg.secret),
        rule: `keyword=${CONFIG.keyword}`,
        rewards: Object.keys(CONFIG.rewards),
        defaultReward: CONFIG.defaultReward,
      });
    }

    if (url.pathname === "/privacy" || url.pathname === "/terms" || url.pathname === "/data-deletion") {
      const name = env.APP_NAME || "Raj IG Comment Agent";
      const email = env.CONTACT_EMAIL || "";
      const kind = url.pathname.slice(1);
      return new Response(
        `<!doctype html><meta charset="utf-8"><title>${name} — ${kind}</title>` +
          `<h1>${name}</h1><p>This app automatically replies to comments and keyword DMs on the owner's own Instagram account. ` +
          `It stores no personal data beyond short-lived deduplication keys that expire automatically. ` +
          `To request deletion of any data, contact: ${email}. Requests are honoured by clearing the stored keys for your account.</p>`,
        { headers: { "Content-Type": "text/html; charset=utf-8" } }
      );
    }

    // Admin: IG credentials ko chat/report me laaye bina Worker ke KV me daalna
    if (url.pathname === "/admin/ingest") {
      if (url.searchParams.get("key") !== env.VERIFY_TOKEN) {
        return new Response("forbidden", { status: 403 });
      }
      if (request.method === "GET") return ingestForm(env.VERIFY_TOKEN);
      if (request.method === "POST") {
        const form = await request.formData();
        const uid = String(form.get("ig_user_id") || "").trim();
        const tok = String(form.get("ig_access_token") || "").trim();
        const sec = String(form.get("ig_app_secret") || "").trim();
        if (!uid || !tok || !sec) return new Response("missing fields", { status: 400 });
        await env.STATE.put("ig_user_id", uid);
        await env.STATE.put("ig_token", tok);
        await env.STATE.put("ig_app_secret", sec);
        return new Response("Saved. Ab /health par instagram:true dikhna chahiye.", {
          headers: { "Content-Type": "text/plain; charset=utf-8" },
        });
      }
    }

    // Admin: token ko chat me bheje bina account ko webhook subscribe karwana
    // GET /admin/subscribe?key=<VERIFY_TOKEN>
    if (url.pathname === "/admin/subscribe") {
      if (url.searchParams.get("key") !== env.VERIFY_TOKEN) {
        return new Response("forbidden", { status: 403 });
      }
      const cfg = await igConfig(env);
      const res = await fetch(
        `https://${CONFIG.graphHost}/${CONFIG.graphVersion}/${cfg.userId}/subscribed_apps?subscribed_fields=comments,messages,messaging_postbacks&access_token=${encodeURIComponent(cfg.token)}`,
        { method: "POST" }
      );
      return new Response(await res.text(), {
        status: res.status,
        headers: { "Content-Type": "application/json" },
      });
    }

    // Admin: kisi reel/post ki media id ko reward se jodna (bina redeploy)
    // GET /admin/mapmedia?key=<VERIFY_TOKEN>&media=<media_id>&reward=<stickman|tools>
    // reward hataana ho to reward=none bhejo. Bina params ke current map dikhega.
    if (url.pathname === "/admin/mapmedia") {
      if (url.searchParams.get("key") !== env.VERIFY_TOKEN) {
        return new Response("forbidden", { status: 403 });
      }
      let map = {};
      try {
        map = JSON.parse((await env.STATE.get("media_rewards")) || "{}");
      } catch (_) {}
      const media = (url.searchParams.get("media") || "").trim();
      const reward = (url.searchParams.get("reward") || "").trim();
      if (media && reward) {
        if (reward === "none") delete map[media];
        else if (CONFIG.rewards[reward]) map[media] = reward;
        else return new Response(`unknown reward: ${reward}`, { status: 400 });
        await env.STATE.put("media_rewards", JSON.stringify(map));
      }
      return Response.json({ ok: true, media_rewards: map });
    }

    if (url.pathname !== "/webhook") return new Response("not found", { status: 404 });

    // Webhook verification handshake (Meta GET bhejta hai)
    if (request.method === "GET") {
      const mode = url.searchParams.get("hub.mode");
      const token = url.searchParams.get("hub.verify_token");
      const challenge = url.searchParams.get("hub.challenge");
      if (mode === "subscribe" && token && token === env.VERIFY_TOKEN) {
        return new Response(challenge || "", { status: 200 });
      }
      return new Response("verification failed", { status: 403 });
    }

    if (request.method !== "POST") return new Response("method not allowed", { status: 405 });

    // Signature check: Instagram webhooks IG app secret se sign hote hain (KV/env se)
    const cfg = await igConfig(env);
    const rawBody = await request.text();
    const given = (request.headers.get("x-hub-signature-256") || "").replace(/^sha256=/, "");
    if (!given || !cfg.secret) return new Response("no signature", { status: 403 });
    const expected = await hmacSha256Hex(cfg.secret, rawBody);
    if (given.length !== expected.length) return new Response("bad signature", { status: 403 });
    let diff = 0;
    for (let i = 0; i < expected.length; i++) diff |= given.charCodeAt(i) ^ expected.charCodeAt(i);
    if (diff !== 0) {
      console.log("rejected: bad signature");
      return new Response("bad signature", { status: 403 });
    }

    let payload;
    try {
      payload = JSON.parse(rawBody);
    } catch (_) {
      return new Response("bad json", { status: 400 });
    }
    if (payload.object !== "instagram") return Response.json({ ok: true, ignored: true });

    const work = (async () => {
      for (const entry of payload.entry || []) {
        for (const change of entry.changes || []) {
          if (change.field === "comments") {
            try {
              await handleComment(env, change.value || {}, dryRun);
            } catch (e) {
              console.log(`comment error: ${e.message}`);
            }
          }
        }
        for (const ev of entry.messaging || []) {
          try {
            await handleMessage(env, ev, dryRun);
          } catch (e) {
            console.log(`dm error: ${e.message}`);
          }
        }
      }
    })();
    ctx.waitUntil(work);

    // Meta ko turant 200 do; asli kaam background me hota hai
    return Response.json({ ok: true });
  },

  async scheduled(event, env, ctx) {
    ctx.waitUntil(refreshToken(env));
  },
};
