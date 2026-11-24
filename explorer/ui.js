/* The explorer's pages (basin, swarm, archive): shared helpers, icons, the sidebar, an agent's stream, following a
   live run (polling /api/events) and watching the server (restarts, new code). */

const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
function tex(s, display = false) {
  if (!window.katex) return esc(s);
  try { return katex.renderToString(s, {displayMode: display, throwOnError: false, strict: "ignore"}); } catch { return esc(s); }
}
const MATH = /\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)|(?<![\\\w$])\$([^$\n]+?)\$(?!\w)/g;
function md(src) {
  const maths = [];
  src = String(src ?? "").split(/(```[\s\S]*?```)/).map((p, i) => i % 2 ? p : p.replace(MATH, (m, a, b, c, d) => {
    maths.push({t: a ?? b ?? c ?? d, d: a != null || b != null});
    return `@@M${maths.length - 1}@@`;
  })).join("");
  const html = window.marked ? marked.parse(src) : esc(src).replace(/\n/g, "<br>");
  return html.replace(/@@M(\d+)@@/g, (_, i) => tex(maths[+i].t, maths[+i].d));
}
// an answer as written: LaTeX without delimiters is math, unless it reads as prose (then only its $...$ is)
const PROSE = /(^|[\s(])[A-Za-z]{3,}[,.;:]?\s+[A-Za-z]{2,}[,.;:]?\s+[A-Za-z]{2,}/;
const ans = a => a == null ? "—" : (/\\\(|\\\[|\$/.test(a) || PROSE.test(String(a).replace(/\\(text|mathrm|operatorname)\{[^}]*\}/g, " ").replace(/\\[A-Za-z]+/g, " ")) ? md(a).replace(/^<p>|<\/p>\s*$/g, "") : tex(a));
// a run's end reason: "proved: e1 (<answer>)" with its answer as math
function reasonHtml(r) {
  const m = String(r ?? "").match(/^(.*?)\((.*)\)\s*$/s);
  return m ? `${esc(m[1])}<span style="text-transform:none">${ans(m[2])}</span>` : esc(r);
}
const shortReason = r => String(r ?? "").replace(/\s*\(.*\)\s*$/s, "");
const money = x => `$${(+x || 0).toFixed(2)}`;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(" ");
function when(name, seconds = false) {  // 20261103-171928-p12 -> Nov 3 17:19
  const m = String(name).match(/^(\d{4})(\d\d)(\d\d)-(\d\d)(\d\d)(\d\d)/);
  return m ? `${MONTHS[+m[2] - 1]} ${+m[3]} ${m[4]}:${m[5]}${seconds ? `:${m[6]}` : ""}` : name;
}
const clock = t => t ? new Date(t * 1000).toLocaleTimeString([], {hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false}) : "—";
const ago = s => { const m = Math.abs(s) / 60; return m < 1 ? `${Math.round(Math.abs(s))}s` : m < 90 ? `${m.toFixed(m < 10 ? 1 : 0)} min` : `${(m / 60).toFixed(1)} h`; };
const bytes = n => n < 1024 ? `${n} B` : n < 2 ** 20 ? `${(n / 1024).toFixed(1)} KB` : `${(n / 2 ** 20).toFixed(1)} MB`;
const store = {
  get(k, d = null) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
};

/* ---------- icons (stroke, 24-unit grid) ---------- */
const ICONS = {
  chev: '<path d="m9 18 6-6-6-6"/>', x: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>', plus: '<path d="M5 12h14"/><path d="M12 5v14"/>',
  play: '<path d="M7 4.5v15l12-7.5z"/>', stop: '<rect x="6" y="6" width="12" height="12" rx="2"/>',
  hash: '<path d="M4 9h16M4 15h16M10 3 8 21M16 3l-2 18"/>',
  file: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h6"/>',
  folder: '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
  run: '<path d="m5 7 5 5-5 5"/><path d="M12 19h7"/>', write: '<path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4z"/>',
  edit: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
  read: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
  flask: '<path d="M9 3h6M10 3v6L4.6 18.2A1.9 1.9 0 0 0 6.2 21h11.6a1.9 1.9 0 0 0 1.6-2.8L14 9V3"/><path d="M7.5 15h9"/>',
  tree: '<circle cx="5" cy="12" r="2.2"/><circle cx="19" cy="5" r="2.2"/><circle cx="19" cy="19" r="2.2"/><circle cx="13" cy="12" r="2.2"/><path d="M7.2 12h3.6M15 11l2.3-4.3M15 13l2.3 4.3"/>',
  sliders: '<path d="M4 6h9M17 6h3M4 12h3M11 12h9M4 18h11M19 18h1"/><circle cx="15" cy="6" r="2"/><circle cx="9" cy="12" r="2"/><circle cx="17" cy="18" r="2"/>',
  book: '<path d="M3 5a2 2 0 0 1 2-2h5a2 2 0 0 1 2 2v15a2 2 0 0 0-2-2H3z"/><path d="M21 5a2 2 0 0 0-2-2h-5a2 2 0 0 0-2 2v15a2 2 0 0 1 2-2h7z"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/>', refresh: '<path d="M20 11a8 8 0 0 0-14.5-4.5L4 8"/><path d="M4 4v4h4"/><path d="M4 13a8 8 0 0 0 14.5 4.5L20 16"/><path d="M20 20v-4h-4"/>',
  check: '<path d="M20 6 9 17l-5-5"/>', alert: '<path d="M10.3 3.9 2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
  spark: '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>', msg: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
  reply: '<path d="m15 10 5 5-5 5"/><path d="M4 4v7a4 4 0 0 0 4 4h12"/>',
  users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
  layers: '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
  archive: '<rect x="3" y="3" width="18" height="5" rx="1"/><path d="M5 8v11a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8M10 12h4"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  bot: '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4"/><circle cx="12" cy="3.5" r="1"/><path d="M9 13v2M15 13v2"/>',
  shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>', clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  zap: '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>', inbox: '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 5.1 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.5-6.9A2 2 0 0 0 16.8 4H7.2a2 2 0 0 0-1.7 1.1z"/>',
  compress: '<path d="M8 3v3a2 2 0 0 1-2 2H3M21 8h-3a2 2 0 0 1-2-2V3M3 16h3a2 2 0 0 1 2 2v3M16 21v-3a2 2 0 0 1 2-2h3"/>',
  pause: '<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/>',
  branch: '<circle cx="6" cy="5" r="2"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="8" r="2"/><path d="M6 7v10M18 10a6 6 0 0 1-6 6H8"/>',
  target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
  dollar: '<path d="M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>', copy: '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
  code: '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>', logo: '<circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M8 6h8M7 8l4 8.5M17 8l-4 8.5"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>', send: '<path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/>',
};
const icon = (n, cls = "") => `<svg class="i ${cls}" viewBox="0 0 24 24" aria-hidden="true">${ICONS[n] || ""}</svg>`;
const tip = text => `<span class="tip" title="${esc(text)}">${icon("info", "sm")}</span>`;
const pill = (text, cls = "", title = "") => `<span class="pill ${cls}" ${title ? `title="${esc(title)}"` : ""}>${text}</span>`;
function fold(summary, body, {open = false, cls = "", meta = "", ico = "", attrs = ""} = {}) {
  return `<details class="fold ${cls}" ${open ? "open" : ""} ${attrs}><summary>${icon("chev", "sm chev")}${ico ? icon(ico, "sm") : ""}<span class="grow">${summary}</span>${meta ? `<span class="meta">${meta}</span>` : ""}</summary>${body}</details>`;
}
function meter(x, of) {
  const f = of ? Math.min(1, (+x || 0) / of) : 0;
  return `<span class="meter ${f >= 1 ? "full" : f > .8 ? "hot" : ""}"><i style="width:${(f * 100).toFixed(1)}%"></i></span>`;
}
const AGENT_COLORS = ["#2a6fdb", "#d9822b", "#1f9d6b", "#b5468a", "#7a5cd6", "#b8941f", "#2b9fb5", "#c4352f"];
function agentColor(name) {
  const m = String(name).match(/(\d+)$/);
  if (name === "lead") return "var(--ink)";
  return AGENT_COLORS[m ? (+m[1] - 1) % AGENT_COLORS.length : [...String(name)].reduce((a, c) => a + c.charCodeAt(0), 0) % AGENT_COLORS.length];
}

/* ---------- the sidebar ---------- */
const SECTIONS = [["swarm", "Swarm", "users"], ["archive", "Archive", "archive"]];
function sidebar({active, newLabel, filterKey}) {
  const nav = document.getElementById("nav");
  nav.className = "side";
  nav.innerHTML = `<div class="brand"><span class="mark">${icon("logo")}</span>Swarm Frontier</div>
    <div class="sections">${SECTIONS.map(([k, l, ic]) => `<a href="${k}.html" class="${k === active ? "on" : ""}">${icon(ic, "sm")}${l}</a>`).join("")}</div>
    ${newLabel ? `<button class="btn full new" data-new="1">${icon("plus", "sm")}${esc(newLabel)}</button>` : ""}
    ${filterKey ? `<div class="filter">${icon("search", "sm")}<input type="search" placeholder="Filter" spellcheck="false"></div>` : ""}
    <div class="runs"></div>`;
  if (filterKey) {
    const input = nav.querySelector(".filter input");
    input.value = store.get(filterKey, "");
    input.addEventListener("input", () => { store.set(filterKey, input.value); applyFilter(); });
  }
}
function applyFilter() {
  const q = (document.querySelector("#nav .filter input")?.value || "").trim().toLowerCase();
  document.querySelectorAll("#nav .runs [data-text]").forEach(el => el.hidden = !!q && !el.dataset.text.toLowerCase().includes(q));
}
function sideRuns(html) {  // the run list, its scroll kept
  const box = document.querySelector("#nav .runs");
  if (!box) return;
  const top = box.scrollTop;
  box.innerHTML = html;
  box.scrollTop = top;
  applyFilter();
}
// one run in the sidebar: {key, on, state: live|proved|stopped|interrupted|failed|done, title, sub, cost, budget}
function runRow(r) {
  const text = `${r.title} ${r.sub || ""} ${r.search || ""}`;
  return `<button class="run ${r.on ? "on" : ""}" data-run="${esc(r.key)}" data-text="${esc(text)}" title="${esc(r.tooltip || "")}">`
    + `<span class="state ${r.state || ""}"></span><span class="t">${esc(r.title)}</span><span class="c num">${r.cost != null ? money(r.cost) : ""}</span>`
    + (r.sub ? `<span></span><span class="s">${esc(r.sub)}</span>` : "")
    + (r.state === "live" && r.budget ? `<span></span><span class="bar"><i style="width:${Math.min(100, 100 * (r.cost || 0) / r.budget).toFixed(1)}%"></i></span>` : "")
    + `</button>`;
}
function runState(reason, live) {
  if (live) return "live";
  const r = String(reason || "");
  if (/^interrupted/.test(r)) return "interrupted";
  if (/^error/.test(r)) return "failed";
  if (/^proved|new result/.test(r)) return "proved";
  if (/stopped|budget|restarted/.test(r)) return "stopped";
  return "done";
}

/* ---------- following a live run ---------- */
// polls /api/events?of=<run|swarm|archive>&id=<id>; onGone when the server no longer holds it (it ended long ago, or the
// server restarted): the page then shows it from disk
function follow(of, id, onEvents, {onGone, onLost, onBack} = {}) {
  let since = 0, alive = true;
  (async () => {
    let fails = 0;
    while (alive) {
      let r;
      try { r = await fetch(`/api/events?of=${of}&id=${encodeURIComponent(id)}&since=${since}`); }
      catch { if (++fails === 1) onLost?.(); await sleep(Math.min(500 * fails, 3000)); continue; }
      if (!alive) return;
      if (r.status === 404) { alive = false; onGone?.(); return; }
      if (!r.ok) { await sleep(1000); continue; }
      if (fails) { fails = 0; onBack?.(); }
      let j;
      try { j = await r.json(); } catch { await sleep(500); continue; }
      if (!alive) return;
      since = j.next;
      if (j.events.length) onEvents(j.events);
      if (j.done) { alive = false; return; }
    }
  })();
  return {close() { alive = false; }};
}

/* ---------- the server: reconnects, new pages, new code ---------- */
const Server = {
  boot: null, version: null, down: false, confirm: false, info: {},
  start(onRestart) {
    if (!location.protocol.startsWith("http") || new URLSearchParams(location.search).get("embed")) return;
    const box = document.body.appendChild(Object.assign(document.createElement("div"), {id: "server"}));
    box.addEventListener("click", async e => {
      const b = e.target.closest("button");
      if (!b) return;
      if (b.dataset.do === "reload") location.reload();
      if (b.dataset.do === "restart") {
        if (this.info.live && !this.confirm) { this.confirm = true; return this.draw(); }
        this.confirm = false; this.info.restarting = true; this.draw();
        try { await fetch("/api/restart", {method: "POST", body: "{}"}); } catch {}
      }
      if (b.dataset.do === "cancel") { this.confirm = false; this.draw(); }
    });
    const tick = async () => {
      try {
        const r = await fetch("/api/health");
        if (!r.ok) throw new Error(r.status);
        const j = await r.json();
        const restarted = this.boot && j.boot !== this.boot;
        if (this.down || restarted) { this.down = false; this.info = j; this.draw(); if (restarted || this.boot) onRestart?.(); }
        this.boot = j.boot; this.version ??= j.static; this.info = j;
      } catch { this.down = true; }
      this.draw();
      setTimeout(tick, this.down ? 1500 : 4000);
    };
    tick();
  },
  draw() {
    const box = document.getElementById("server");
    if (!box) return;
    const j = this.info, out = [];
    if (this.down || j.restarting) out.push(`<div class="toast"><span class="spin"></span>${j.restarting && !this.down ? "Restarting server" : "Reconnecting"}</div>`);
    else {
      if (j.stale === "pending") out.push(this.confirm
        ? `<div class="toast">${icon("alert", "sm")}Stops ${j.live} live run${j.live === 1 ? "" : "s"}<button class="btn sm" data-do="restart">Restart</button><button class="btn sm" data-do="cancel">${icon("x", "sm")}</button></div>`
        : `<div class="toast">${icon("refresh", "sm")}New server code<button class="btn sm" data-do="restart">Restart</button></div>`);
      else if (String(j.stale || "").startsWith("error")) out.push(`<div class="toast bad" title="${esc(j.stale)}">${icon("alert", "sm")}New code fails to import</div>`);
      if (this.version && j.static && j.static !== this.version) out.push(`<div class="toast">${icon("refresh", "sm")}Page updated<button class="btn sm" data-do="reload">Reload</button></div>`);
    }
    const html = out.join("");
    if (box.dataset.html !== html) { box.dataset.html = html; box.innerHTML = html; }
  },
};

/* ---------- an agent's stream ---------- */
const atBottom = () => innerHeight + scrollY >= document.body.scrollHeight - 140;
const unjson = s => s.replace(/\\n/g, "\n").replace(/\\t/g, "\t").replace(/\\"/g, '"').replace(/\\\\/g, "\\");
const TOOLS = {run_scratchpad: ["run", "run"], write_scratchpad: ["write", "write"], edit_scratchpad: ["edit", "edit"],
  read_scratchpad: ["read", "read"], slack_post: ["post", "hash", "slack"], slack_read: ["read", "hash", "slack"], submit_answer: ["submit", "target"]};
function toolChip(name) {
  const [label, ic, cls] = TOOLS[name] || [name.replace("_scratchpad", ""), "code"];
  return `<span class="tool ${cls || label}">${icon(ic, "sm")}${esc(label)}</span>`;
}
const firstLine = s => (String(s ?? "").split("\n").find(l => l.trim() && !/^\[exit code|^\(ran it|^--- std/.test(l)) || "").slice(0, 200);
function noteHtml(text, kind) {
  const t = String(text);
  const [ic, cls] = kind === "idle" ? ["pause", "warn"] : kind === "done" ? ["check", ""] : kind === "working" ? ["play", "good"]
    : /^compaction/.test(t) ? ["compress", ""] : /^would submit/.test(t) ? ["target", "good"] : /^error|failed|refused/.test(t) ? ["alert", "bad"]
    : /^nudge/.test(t) ? ["zap", "warn"] : /^Slack/.test(t) ? ["hash", ""] : ["info", ""];
  return `<div class="note ${cls}"><span title="${esc(t)}">${icon(ic, "sm")}${esc(t.length > 160 ? t.slice(0, 160) + "…" : t)}</span></div>`;
}
// a stream's element and its event handler; `opts.first` names the first message, `opts.tagged` marks @names
function makeStream(opts = {}) {
  const st = {el: Object.assign(document.createElement("div"), {className: "stream"}), blocks: {}, last: null, n: 0};
  const pending = new Set();
  const add = html => {
    const follow = st.el.isConnected && atBottom(), d = document.createElement("div");
    d.innerHTML = html;
    const el = d.firstElementChild;
    st.el.appendChild(el);
    if (follow) scrollTo(0, document.body.scrollHeight);
    return el;
  };
  const redraw = block => {
    pending.add(block);
    if (pending.size === 1) requestAnimationFrame(() => {
      const follow = st.el.isConnected && atBottom();
      pending.forEach(b => b.el.innerHTML = md(b.text));
      pending.clear();
      if (follow) scrollTo(0, document.body.scrollHeight);
    });
  };
  const deco = opts.tagged || (h => h);
  st.on = e => {
    switch (e.k) {
      case "told":
        st.last = null;
        if (!e.first && /^Slack: \d+ unread/.test(e.text)) { add(noteHtml(e.text)); break; }
        add(e.first ? `<div class="ev">${fold(opts.first || "First message", `<div class="body md-body">${md(e.text)}</div>`, {ico: "inbox"})}</div>`
                    : `<div class="ev told">${deco(md(e.text))}</div>`);
        break;
      case "response": st.last = null; st.n = e.n; add(`<div class="turn"><span class="chip">#${e.n}</span></div>`); break;
      case "think": case "say":
        if (st.last?.kind !== e.k) st.last = {kind: e.k, text: "", el: add(`<div class="ev ${e.k === "think" ? "think" : ""}"></div>`)};
        st.last.text += e.text;
        redraw(st.last);
        break;
      case "call":
        st.last = null;
        st.blocks[e.id] = {raw: "", el: add(`<details class="call" open><summary>${icon("chev", "sm chev")}${toolChip(e.name)}<span class="first"></span><span class="res pending"></span></summary><pre class="code"></pre></details>`)};
        break;
      case "args": { const b = st.blocks[e.id]; if (b) { b.raw += e.text; b.el.querySelector("pre").textContent = unjson(b.raw); } break; }
      case "called": {
        const b = st.blocks[e.id]; if (!b) break;
        st.blocks[e.call_id] = b;
        const pre = b.el.querySelector("pre.code");
        if (e.code) pre.textContent = e.code; else pre.remove();
        break;
      }
      case "result": {
        const b = st.blocks[e.call_id]; if (!b) break;
        b.el.querySelector(".first").textContent = firstLine(e.out);
        b.el.querySelector(".res").className = `res ${e.error ? "err" : "ok"}`;
        b.el.insertAdjacentHTML("beforeend", `<pre class="${e.error ? "err" : ""}">${esc(e.out)}</pre>`);
        b.el.open = false;
        break;
      }
      case "state": st.last = null; if (e.why) add(noteHtml(e.state === "working" ? "woken" : `${e.state}: ${e.why}`, e.state)); break;
      case "note": st.last = null; add(noteHtml(e.text)); break;
    }
  };
  return st;
}
