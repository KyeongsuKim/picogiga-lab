/* ==========================================================================
   picoGIGA Lab — shared layout and page renderers
   Content: data.js (people, news) and publications.js (synced from Scholar).
   ========================================================================== */
(function () {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const page = document.body.dataset.page;
  const PUBS = window.PUBLICATIONS || [];
  const META = window.PUBS_META || {};

  /* ---------- Icons ---------- */
  const svg = (inner) =>
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${inner}</svg>`;
  const ICONS = {
    arrow: svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    external: svg('<path d="M7 17 17 7M8 7h9v9"/>'),
    mail: svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>'),
    close: svg('<path d="M6 6l12 12M18 6 6 18"/>'),
    prev: svg('<path d="m15 5-7 7 7 7"/>'),
    next: svg('<path d="m9 5 7 7-7 7"/>'),
    co2: svg('<circle cx="4.6" cy="12" r="2.6"/><circle cx="12" cy="12" r="2.6"/><circle cx="19.4" cy="12" r="2.6"/><path d="M7.2 10.9h2.2M7.2 13.1h2.2M14.6 10.9h2.2M14.6 13.1h2.2"/>'),
    biomass: svg('<path d="M5 19c0-8.5 5.5-13.5 14.5-14 0 9-5.2 14-13.5 14"/><path d="M5 19 13.5 10.5"/><path d="M9 15h4M11.5 12.5V9"/>'),
    plastic: svg('<path d="M4.5 11a7.5 7.5 0 0 1 12.8-4.8"/><path d="M18 2.8v3.8h-3.8"/><path d="M19.5 13a7.5 7.5 0 0 1-12.8 4.8"/><path d="M6 21.2v-3.8h3.8"/><circle cx="9.5" cy="12" r="1.2"/><circle cx="14.5" cy="12" r="1.2"/><path d="M10.7 12h2.6"/>'),
    dft: svg('<ellipse cx="12" cy="12" rx="9.5" ry="3.6"/><ellipse cx="12" cy="12" rx="9.5" ry="3.6" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="9.5" ry="3.6" transform="rotate(120 12 12)"/><circle cx="12" cy="12" r="1.3" fill="currentColor"/>'),
    ml: svg('<circle cx="4" cy="7" r="1.8"/><circle cx="4" cy="17" r="1.8"/><circle cx="12" cy="4.5" r="1.8"/><circle cx="12" cy="12" r="1.8"/><circle cx="12" cy="19.5" r="1.8"/><circle cx="20" cy="12" r="1.8"/><path d="M5.7 6.4 10.3 5M5.7 7.8l4.6 3.4M5.7 16.2l4.6-3.4M5.7 17.6l4.6 1.4M13.7 5.2l4.7 5.8M13.8 12H18.2M13.7 18.8l4.7-5.8"/>'),
    process: svg('<rect x="3.5" y="3" width="5" height="18" rx="2.5"/><path d="M3.5 8h5M3.5 13h5"/><path d="M8.5 6H13v5.5h2.5"/><path d="M8.5 18h7"/><rect x="15.5" y="9" width="5" height="11" rx="1.2"/>')
  };

  const AREAS = [
    { id: "co2", icon: "co2", c: "#0e9f7a", group: "app", title: "CO₂ Conversion", blurb: "Reactive capture and conversion, direct air capture" },
    { id: "biomass", icon: "biomass", c: "#5b9a2c", group: "app", title: "Biomass Energy", blurb: "Sustainable aviation fuel from biomass" },
    { id: "plastic", icon: "plastic", c: "#d07a26", group: "app", title: "Plastic Upcycling", blurb: "Turning waste plastic into chemicals" },
    { id: "dft", icon: "dft", c: "#7c6cf6", group: "method", title: "DFT", blurb: "Reaction mechanisms from first principles" },
    { id: "ml", icon: "ml", c: "#4a86e8", group: "method", title: "Machine Learning", blurb: "Materials screening and smart plants" },
    { id: "process", icon: "process", c: "#0f766e", group: "method", title: "Process Systems", blurb: "Process design, TEA and LCA" }
  ];

  /* ---------- Header / footer ---------- */
  const NAV = [
    { href: "research.html", label: "Research", key: "research" },
    { href: "people.html", label: "People", key: "people" },
    { href: "publications.html", label: "Publications", key: "publications" },
    { href: "news.html", label: "News", key: "news" },
    { href: "joinus.html", label: "Join us", key: "joinus" }
  ];
  const brand = `<span class="pico">pico</span><span class="giga">GIGA</span><span class="lab">Lab</span>`;

  function renderChrome() {
    const header = $("#site-header");
    if (header) {
      header.innerHTML = `
        <div class="wrap">
          <a class="brand" href="index.html" aria-label="picoGIGA Lab home">${brand}</a>
          <nav class="nav" id="nav" aria-label="Main">
            ${NAV.map((n) => `<a href="${n.href}"${n.key === page ? ' aria-current="page"' : ""}>${n.label}</a>`).join("")}
            <a class="nav-cta" href="contact.html"${page === "contact" ? ' aria-current="page"' : ""}>Contact</a>
          </nav>
          <button class="menu-btn" id="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
        </div>`;
      const btn = $("#menu-btn");
      btn.addEventListener("click", () => {
        const open = document.body.classList.toggle("menu-open");
        btn.setAttribute("aria-expanded", open);
        btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      });
      $$("#nav a").forEach((a) => a.addEventListener("click", () => document.body.classList.remove("menu-open")));
      const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 24);
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }

    const footer = $("#site-footer");
    if (footer) {
      const L = window.LAB;
      footer.innerHTML = `
        <div class="wrap">
          <div class="top">
            <div>
              <a class="brand" href="index.html">${brand}</a>
              <p class="about">${esc(L.fullName)}<br>${esc(L.institute)}</p>
            </div>
            <div>
              <h5>Explore</h5>
              <ul>${NAV.map((n) => `<li><a href="${n.href}">${n.label}</a></li>`).join("")}</ul>
            </div>
            <div>
              <h5>Contact</h5>
              <ul>
                <li>${esc(L.address)}</li>
                <li><a href="mailto:${esc(L.email)}">${esc(L.email)}</a></li>
              </ul>
            </div>
          </div>
          <div class="bottom"><span>© ${new Date().getFullYear()} picoGIGA Lab, KIST</span>${META.updated ? `<span>Last updated ${esc(META.updated)}</span>` : ""}</div>
        </div>`;
    }
  }

  /* ---------- Helpers ---------- */
  const img = (src, alt) =>
    `<img src="${esc(src)}" alt="${esc(alt)}" loading="lazy" decoding="async" onerror="this.closest('[data-img]').classList.add('missing')">`;

  const initials = (name) => name.split(/\s+/).filter((w) => /^[A-Za-z]/.test(w)).map((w) => w[0]).slice(0, 2).join("").toUpperCase();

  // English name -> Korean name (search, inventor lists)
  const KO = {};
  if (window.PI) KO[window.PI.name] = window.PI.ko;
  (window.MEMBERS || []).forEach((g) => g.people.forEach((p) => { KO[p.name] = p.ko; }));
  (window.ALUMNI || []).forEach((p) => { KO[p.name] = p.ko; });
  const koName = (n) => KO[n] || n;

  function reveal() {
    const els = $$(".reveal");
    if (!("IntersectionObserver" in window)) return els.forEach((e) => e.classList.add("in"));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach((e) => io.observe(e));
  }

  /* ---------- Lightbox ---------- */
  function bindLightbox(selector, data) {
    const els = $$(selector);
    const items = els.map((el, i) => ({ el, ...data[i] }));
    let box = $(".lightbox");
    if (!box) {
      box = document.createElement("div");
      box.className = "lightbox";
      box.setAttribute("role", "dialog");
      box.setAttribute("aria-modal", "true");
      box.innerHTML = `<img alt=""><div class="cap"></div>
        <button class="lb-close" aria-label="Close">${ICONS.close}</button>
        <button class="lb-prev" aria-label="Previous">${ICONS.prev}</button>
        <button class="lb-next" aria-label="Next">${ICONS.next}</button>`;
      document.body.appendChild(box);
    }
    let idx = 0, list = [];
    const show = (i) => {
      idx = (i + list.length) % list.length;
      const it = list[idx];
      $("img", box).src = it.src;
      $("img", box).alt = it.title;
      $(".cap", box).innerHTML = `<b>${esc(it.title)}</b>${it.text ? esc(it.text) : ""}`;
    };
    const close = () => { box.classList.remove("open"); document.body.style.overflow = ""; };
    $(".lb-close", box).onclick = close;
    $(".lb-prev", box).onclick = () => show(idx - 1);
    $(".lb-next", box).onclick = () => show(idx + 1);
    box.onclick = (e) => { if (e.target === box) close(); };
    document.addEventListener("keydown", (e) => {
      if (!box.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
    els.forEach((el, i) => el.addEventListener("click", () => {
      list = items.filter((it) => !it.el.classList.contains("missing"));
      const start = list.indexOf(items[i]);
      if (start < 0) return;
      show(start);
      box.classList.add("open");
      document.body.style.overflow = "hidden";
      $(".lb-close", box).focus();
    }));
  }

  /* ======================================================================
     Hero animation: a continuous "powers of ten" zoom
     electrons → molecule on a surface → catalyst particle → reactor
     → chemical plant, and back again.
     Drop an assets/video/hero.mp4 in place and it replaces the drawing.
     ====================================================================== */
  function zoomHero() {
    const box = $("#zoom");
    if (!box) return;
    const video = $("video", box);
    if (video) video.addEventListener("loadeddata", () => box.classList.add("has-video"));

    const cv = $("canvas", box), ctx = cv.getContext("2d");
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const K = 7;           // magnification between neighbouring scenes
    const HOLD = 1.9, MOVE = 1.7;
    let W = 0, H = 0, raf = 0, visible = true, t0 = performance.now(), shown = -1;

    const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
    const O_COL = [242, 139, 130];

    function circle(x, y, r) { ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); }
    function rrect(x, y, w, h, r) { ctx.beginPath(); ctx.roundRect ? ctx.roundRect(x, y, w, h, r) : ctx.rect(x, y, w, h); }

    // Each scene is drawn in unit coordinates (radius ≈ 1) and keeps the
    // previous, smaller scene at its centre (0, 0).
    const SCENES = [
      { name: "Electrons", tools: "DFT", size: "10⁻¹⁰ m", c: [168, 156, 255], draw(t, px, c) {
        const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 1);
        g.addColorStop(0, rgba(c, 0.28)); g.addColorStop(1, rgba(c, 0));
        ctx.fillStyle = g; circle(0, 0, 1); ctx.fill();
        ctx.fillStyle = rgba(c, 0.95);
        [[-0.035, 0.02], [0.04, 0.015], [0, -0.04]].forEach(([x, y]) => { circle(x, y, 0.05); ctx.fill(); });
        for (let k = 0; k < 3; k++) {
          ctx.save(); ctx.rotate(k * Math.PI / 3 + t * 0.12);
          ctx.strokeStyle = rgba(c, 0.55); ctx.beginPath(); ctx.ellipse(0, 0, 0.8, 0.27, 0, 0, Math.PI * 2); ctx.stroke();
          const a = t * 1.5 + k * 2.1;
          ctx.fillStyle = "#fff"; circle(0.8 * Math.cos(a), 0.27 * Math.sin(a), 0.034); ctx.fill();
          ctx.fillStyle = rgba(c, 0.25); circle(0.8 * Math.cos(a), 0.27 * Math.sin(a), 0.09); ctx.fill();
          ctx.restore();
        }
      } },
      { name: "Molecules on a catalyst", tools: "DFT · molecular dynamics", size: "10⁻⁹ m", c: [132, 164, 255], draw(t, px, c) {
        for (let j = 0; j < 4; j++) {
          const y = 0.3 + j * 0.19;
          for (let x = -1.5 + (j % 2) * 0.1; x <= 1.5; x += 0.2) {
            const a = Math.max(0, 1 - Math.abs(x) / 1.5) * (1 - j * 0.18);
            ctx.fillStyle = rgba(c, 0.14 * a); ctx.strokeStyle = rgba(c, 0.85 * a);
            circle(x, y, 0.085); ctx.fill(); ctx.stroke();
          }
        }
        const v = Math.sin(t * 3) * 0.012;
        const Ol = [-0.2 - v, -0.12], Or = [0.2 + v, -0.12];
        ctx.strokeStyle = "rgba(255,255,255,0.7)";
        [Ol, Or].forEach(([x, y]) => {
          const nx = -y, ny = x, l = Math.hypot(nx, ny), o = 0.022;
          for (const s of [-1, 1]) { ctx.beginPath(); ctx.moveTo(s * o * nx / l, s * o * ny / l); ctx.lineTo(x + s * o * nx / l, y + s * o * ny / l); ctx.stroke(); }
        });
        ctx.fillStyle = rgba(O_COL, 0.95); [Ol, Or].forEach(([x, y]) => { circle(x, y, 0.1); ctx.fill(); });
        ctx.fillStyle = "rgba(230,235,245,0.95)"; circle(0, 0, 0.085); ctx.fill();
        [[-0.75 + 0.08 * Math.sin(t * 0.7), -0.55], [0.7, -0.72 + 0.05 * Math.sin(t)], [0.35, -0.45 + 0.04 * Math.cos(t * 0.8)]].forEach(([x, y], i) => {
          ctx.fillStyle = "rgba(255,255,255,0.75)";
          const a = t * 0.5 + i;
          circle(x - 0.04 * Math.cos(a), y - 0.04 * Math.sin(a), 0.035); ctx.fill();
          circle(x + 0.04 * Math.cos(a), y + 0.04 * Math.sin(a), 0.035); ctx.fill();
        });
      } },
      { name: "Catalyst particles", tools: "Kinetic Monte Carlo · MD", size: "10⁻⁸ m", c: [110, 182, 240], draw(t, px, c) {
        ctx.fillStyle = rgba(c, 0.07); ctx.fillRect(-1.6, 0.62, 3.2, 1);
        ctx.strokeStyle = rgba(c, 0.6); ctx.beginPath(); ctx.moveTo(-1.6, 0.62); ctx.lineTo(1.6, 0.62); ctx.stroke();
        ctx.strokeStyle = rgba(c, 0.14);
        for (let x = -1.6; x < 1.6; x += 0.12) { ctx.beginPath(); ctx.moveTo(x, 0.66); ctx.lineTo(x + 0.3, 1.2); ctx.stroke(); }
        for (let j = 0; j < 8; j++) {
          const y = 0.575 - j * 0.078, w = 0.46 - Math.max(0, j - 3) * 0.06;
          for (let x = -w + (j % 2) * 0.045; x <= w + 1e-6; x += 0.09) {
            ctx.fillStyle = rgba(c, 0.22); ctx.strokeStyle = rgba(c, 0.9);
            circle(x, y, 0.04); ctx.fill(); ctx.stroke();
          }
        }
        for (let i = 0; i < 6; i++) {
          const a = t * 0.35 + i * 1.05, x = Math.cos(a) * (0.75 + 0.1 * i % 0.3), y = -0.35 + Math.sin(a * 1.3) * 0.35;
          ctx.fillStyle = "rgba(230,235,245,0.8)"; circle(x, y, 0.022); ctx.fill();
          ctx.fillStyle = rgba(O_COL, 0.85); circle(x - 0.045, y, 0.024); ctx.fill(); circle(x + 0.045, y, 0.024); ctx.fill();
        }
      } },
      { name: "Reactors", tools: "CFD · reaction kinetics", size: "1 m", c: [92, 204, 222], draw(t, px, c) {
        ctx.fillStyle = rgba(c, 0.06); rrect(-0.34, -0.9, 0.68, 1.8, 0.14); ctx.fill();
        ctx.strokeStyle = rgba(c, 0.9); ctx.stroke();
        for (let k = -7; k <= 7; k++) {
          const y = k * 0.11, off = (k % 2) ? 0.06 : 0;
          for (let x = -0.24 + off; x <= 0.24 - off + 1e-6; x += 0.12) {
            const hero = k === 0 && Math.abs(x) < 1e-6;
            ctx.fillStyle = rgba(c, hero ? 0.6 : 0.18); ctx.strokeStyle = rgba(c, hero ? 1 : 0.55);
            circle(x, y, 0.047); ctx.fill(); ctx.stroke();
          }
        }
        ctx.strokeStyle = rgba(c, 0.8);
        ctx.beginPath(); ctx.moveTo(0, -0.9); ctx.lineTo(0, -1.12); ctx.lineTo(0.6, -1.12); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, 0.9); ctx.lineTo(0, 1.12); ctx.lineTo(-0.6, 1.12); ctx.stroke();
        ctx.save(); ctx.setLineDash([0.05, 0.07]); ctx.lineDashOffset = -t * 0.25; ctx.strokeStyle = "rgba(255,255,255,0.55)";
        ctx.beginPath(); ctx.moveTo(0.6, -1.06); ctx.lineTo(0.06, -1.06); ctx.lineTo(0.06, -0.9); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(-0.06, 0.9); ctx.lineTo(-0.06, 1.06); ctx.lineTo(-0.6, 1.06); ctx.stroke();
        ctx.strokeStyle = rgba(c, 0.3);
        for (const x of [-0.44, 0.44]) { ctx.beginPath(); ctx.moveTo(x, -0.8); ctx.lineTo(x, 0.8); ctx.stroke(); }
        ctx.restore();
      } },
      { name: "Chemical plants", tools: "Process simulation · TEA", size: "10² m", c: [84, 214, 182], draw(t, px, c) {
        ctx.strokeStyle = rgba(c, 0.5); ctx.beginPath(); ctx.moveTo(-1.6, 0.62); ctx.lineTo(1.6, 0.62); ctx.stroke();
        ctx.strokeStyle = rgba(c, 0.22); ctx.beginPath(); ctx.moveTo(-1.1, 0.3); ctx.lineTo(1.1, 0.3); ctx.stroke();
        const unit = (x, y, w, h, r, a = 0.9) => { ctx.fillStyle = rgba(c, 0.08); rrect(x, y, w, h, r); ctx.fill(); ctx.strokeStyle = rgba(c, a); ctx.stroke(); };
        unit(-0.055, -0.14, 0.11, 0.28, 0.03, 1);
        ctx.strokeStyle = rgba(c, 0.7);
        ctx.beginPath(); ctx.moveTo(-0.04, 0.14); ctx.lineTo(-0.06, 0.62); ctx.moveTo(0.04, 0.14); ctx.lineTo(0.06, 0.62); ctx.stroke();
        unit(0.32, -0.8, 0.14, 1.42, 0.07);
        ctx.strokeStyle = rgba(c, 0.35);
        for (let y = -0.68; y < 0.55; y += 0.12) { ctx.beginPath(); ctx.moveTo(0.32, y); ctx.lineTo(0.46, y); ctx.stroke(); }
        unit(0.62, -0.45, 0.1, 1.07, 0.05);
        ctx.fillStyle = rgba(c, 0.08); circle(-0.52, 0.44, 0.18); ctx.fill(); ctx.strokeStyle = rgba(c, 0.9); ctx.stroke();
        unit(-1.08, 0.22, 0.26, 0.4, 0.03);
        unit(-0.27, -0.95, 0.06, 1.57, 0.01);
        for (let i = 0; i < 4; i++) {
          const f = ((t * 0.18 + i / 4) % 1);
          ctx.fillStyle = `rgba(255,255,255,${0.22 * (1 - f)})`; circle(-0.24 + f * 0.25, -1 - f * 0.45, 0.05 + f * 0.1); ctx.fill();
        }
        ctx.strokeStyle = rgba(c, 0.75);
        ctx.beginPath(); ctx.moveTo(0, -0.14); ctx.lineTo(0, -0.3); ctx.lineTo(0.32, -0.3); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0.39, -0.8); ctx.lineTo(0.39, -0.92); ctx.lineTo(0.67, -0.92); ctx.lineTo(0.67, -0.45); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(-0.055, 0); ctx.lineTo(-0.34, 0); ctx.lineTo(-0.34, 0.3); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(-0.7, 0.44); ctx.lineTo(-0.82, 0.44); ctx.stroke();
        ctx.save(); ctx.setLineDash([0.03, 0.05]); ctx.lineDashOffset = -t * 0.12; ctx.strokeStyle = "rgba(255,255,255,0.6)";
        ctx.beginPath(); ctx.moveTo(0, -0.17); ctx.lineTo(0, -0.33); ctx.lineTo(0.32, -0.33); ctx.stroke();
        ctx.restore();
      } }
    ];
    const N = SCENES.length;

    const smooth = (x) => x * x * (3 - 2 * x);
    function levelAt(sec) {
      if (reduce) return Math.floor(sec / 4) % N;
      const seg = HOLD + MOVE, half = (N - 1) * seg;
      let u = sec % (2 * half);
      const back = u >= half;
      if (back) u -= half;
      const i = Math.min(N - 2, Math.floor(u / seg)), r = u - i * seg;
      const z = i + (r < HOLD ? 0 : smooth((r - HOLD) / MOVE));
      return back ? N - 1 - z : z;
    }

    function resize() {
      const r = box.getBoundingClientRect();
      W = r.width; H = r.height;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    }

    const label = $(".zoom-label", box), dots = $$(".zoom-dots i", box);
    function setLabel(i) {
      if (i === shown) return;
      shown = i;
      const s = SCENES[i];
      label.innerHTML = `<div><div class="name">${s.name}</div><div class="tools">${s.tools}</div></div><div class="size">${s.size}</div>`;
      dots.forEach((d, k) => d.classList.toggle("on", k === i));
    }

    const fixedZ = parseFloat(new URLSearchParams(location.search).get("zoom")); // e.g. ?zoom=2.5 to inspect a frame
    function frame(now) {
      const t = (now - t0) / 1000;
      const z = isNaN(fixedZ) ? levelAt(t) : fixedZ;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      const R = Math.min(W, H) * 0.4;
      const zz = z * (N - 0.85) / (N - 1); // ease out a little further so the last scene fits
      for (let i = 0; i < N; i++) {
        const d = zz - i;
        if (d > 1.25 || d < -1) continue;
        const f = Math.pow(K, -d);
        const a = d >= 0 ? 1 - smooth(Math.min(1, d / 1.25)) : 1 - smooth(Math.min(1, -d));
        if (a <= 0.001) continue;
        ctx.save();
        ctx.translate(W / 2, H / 2 - H * 0.04);
        ctx.scale(R * f, R * f);
        ctx.globalAlpha = a;
        ctx.lineWidth = 1.3 / (R * f);
        SCENES[i].draw(t, 1 / (R * f), SCENES[i].c);
        ctx.restore();
      }
      setLabel(Math.round(z));
      if (visible) raf = requestAnimationFrame(frame);
    }

    resize();
    raf = requestAnimationFrame(frame);
    window.addEventListener("resize", resize);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(([en]) => {
        visible = en.isIntersecting;
        cancelAnimationFrame(raf);
        if (visible) raf = requestAnimationFrame(frame);
      }).observe(box);
    }
  }

  /* ======================================================================
     Publications
     ====================================================================== */
  const TYPE_LABEL = { journal: "Journal", patent: "Patent", preprint: "Preprint" };

  const KO_NAMES = new Set(Object.values(KO));

  function authorsHTML(p, hl) {
    const h = hl || esc;
    if (p.inv) {
      return "Inventors: " + p.inv.split(/\s*,\s*/).map((n) => (KO_NAMES.has(n) ? `<b>${h(n)}</b>` : h(n))).join(", ");
    }
    const parts = (p.a || []).map((a, i) => {
      if (!a.lab) return h(a.n);
      const lead = i === 0 || a.f || a.c;
      return `<b>${h(a.n)}</b>${lead ? `<span class="corr" title="First or corresponding author">*</span>` : ""}`;
    });
    return parts.join(", ") + (p.trunc ? ", …" : "");
  }

  const TOPIC = Object.fromEntries(AREAS.map((a) => [a.id, a.title]));

  // "KR registered 2026.09 · US filed 2024.11 (US 18/955,625)"
  const filingsText = (p) => (p.filings || []).map((f) =>
    `${f.c} ${f.s === "registered" ? "registered" : "filed"} ${(f.d || "").slice(0, 7).replace("-", ".")}${f.no ? ` (${f.no})` : ""}`).join(" · ");

  function venueHTML(p, h) {
    if (p.filings) return esc(filingsText(p));
    if (p.type === "patent") return `${p.j ? `<i>${h(p.j)}</i> · ` : ""}${p.y || ""}`;
    const j = p.j || (p.type === "preprint" ? "Preprint" : "");
    return `${j ? `<i>${h(j)}</i> · ` : ""}${p.y || ""}`;
  }

  function pubHTML(p, hl) {
    const h = hl || esc;
    const title = p.u ? `<a class="pub-title" href="${esc(p.u)}" target="_blank" rel="noopener">${h(p.t)}</a>` : `<span class="pub-title">${h(p.t)}</span>`;
    return `
      <li class="pub">
        <div>
          ${title}
          ${p.en ? `<div class="pub-venue">${h(p.en)}</div>` : ""}
          <div class="pub-venue">${venueHTML(p, h)}</div>
          <div class="pub-authors">${authorsHTML(p, hl)}</div>
        </div>
        <div class="pub-side">
          ${p.u ? `<a class="pub-link" href="${esc(p.u)}" target="_blank" rel="noopener" aria-label="Open">${ICONS.external}</a>` : ""}
        </div>
      </li>`;
  }

  function pubCard(p) {
    const title = p.u ? `<a href="${esc(p.u)}" target="_blank" rel="noopener">${esc(p.t)}</a>` : esc(p.t);
    return `
      <article class="pub-card reveal">
        <h3>${title}</h3>
        <div class="pub-venue">${venueHTML(p, esc)}</div>
      </article>`;
  }

  function publications() {
    const counts = (f) => PUBS.filter(f).length;
    const s = META.scholar || {};
    $("#pub-stats").innerHTML = `
      <span><b>${counts((p) => p.type === "journal")}</b>journal papers</span>
      <span><b>${counts((p) => p.type === "patent")}</b>patents</span>
      ${counts((p) => p.type === "preprint") ? `<span><b>${counts((p) => p.type === "preprint")}</b>preprints</span>` : ""}
      ${s.url ? `<a href="${esc(s.url)}" target="_blank" rel="noopener">Google Scholar</a>` : ""}`;

    // Two views: journal papers (with preprints) and patents
    const SECTIONS = {
      journal: { label: "Journal", types: ["journal", "preprint", "other"] },
      patent: { label: "Patents", types: ["patent"] }
    };
    const inSection = (p, sec) => SECTIONS[sec].types.includes(p.type);
    const initial = location.hash.slice(1);
    const qTopic = new URLSearchParams(location.search).get("topic");
    const state = { sec: SECTIONS[initial] ? initial : "journal", year: "all", topic: TOPIC[qTopic] ? qTopic : "all", q: "" };

    const tabs = $("#type-chips");
    tabs.classList.add("tabs");
    tabs.setAttribute("role", "tablist");
    tabs.innerHTML = Object.entries(SECTIONS).map(([k, v]) =>
      `<button class="tab" type="button" role="tab" data-sec="${k}" aria-selected="${k === state.sec}">${v.label} <span class="count">${counts((p) => inSection(p, k))}</span></button>`).join("");
    tabs.addEventListener("click", (e) => {
      const b = e.target.closest(".tab"); if (!b) return;
      state.sec = b.dataset.sec; state.year = "all";
      $$(".tab", tabs).forEach((t) => t.setAttribute("aria-selected", t === b));
      history.replaceState(null, "", state.sec === "journal" ? location.pathname : "#" + state.sec);
      setup(); draw();
    });

    const tsel = $("#topic-select");
    tsel.innerHTML = `<option value="all">All topics</option>` + AREAS.map((a) => `<option value="${a.id}">${a.title}</option>`).join("");
    tsel.value = state.topic;
    tsel.addEventListener("change", () => { state.topic = tsel.value; draw(); });
    const sel = $("#year-select");
    sel.addEventListener("change", () => { state.year = sel.value; draw(); });
    const input = $("#pub-search");
    input.addEventListener("input", () => { state.q = input.value.trim(); draw(); });

    function setup() {
      const pool = PUBS.filter((p) => inSection(p, state.sec));
      const years = [...new Set(pool.map((p) => p.y).filter(Boolean))].sort((a, b) => b - a);
      sel.innerHTML = `<option value="all">All years</option>` + years.map((y) => `<option value="${y}">${y}</option>`).join("");
      input.placeholder = state.sec === "patent" ? "Title, inventor" : "Title, journal, author";
    }

    function draw() {
      const q = state.q.toLowerCase();
      const re = q ? new RegExp(state.q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi") : null;
      const hl = (s) => { const t = esc(s); return re ? t.replace(re, (x) => `<mark>${x}</mark>`) : t; };
      const pool = PUBS.filter((p) => inSection(p, state.sec));
      const list = pool.filter((p) =>
        (state.year === "all" || String(p.y) === state.year) &&
        (state.topic === "all" || (p.topics || []).includes(state.topic)) &&
        (!q || [p.t, p.j, p.en, p.inv, ...(p.a || []).map((a) => a.n + " " + (a.lab ? a.lab + " " + koName(a.lab) : ""))].join(" ").toLowerCase().includes(q)));
      const ys = [...new Set(list.map((p) => p.y || "—"))];
      const filtered = state.year !== "all" || state.topic !== "all" || q;
      $("#pub-note").textContent = filtered ? `${list.length} of ${pool.length}` : "";
      $("#pub-groups").innerHTML = list.length
        ? ys.map((y) => {
          const l = list.filter((p) => (p.y || "—") === y);
          return `<section class="year-block"><div class="year-head"><h2>${y}</h2><span>${l.length}</span></div><ul class="pub-list">${l.map((p) => pubHTML(p, hl)).join("")}</ul></section>`;
        }).join("")
        : `<p class="lede">Nothing matches.</p>`;
      $("#sync-note").textContent = META.updated
        ? `Updated ${META.updated}.` + (state.sec === "patent" ? " Lab members are in bold." : " Lab members are in bold; * first or corresponding author.")
        : "";
    }
    setup();
    draw();
  }

  /* ======================================================================
     Pages
     ====================================================================== */
  function home() {
    zoomHero();

    const row = (a) => `
      <a class="area-row reveal" href="research.html#${a.id}" style="--c:${a.c}">
        <span class="name">${a.title}</span>
        <span class="desc">${a.blurb}</span>
        ${ICONS.arrow}
      </a>`;
    $("#areas-app").innerHTML = AREAS.filter((a) => a.group === "app").map(row).join("");
    $("#areas-method").innerHTML = AREAS.filter((a) => a.group === "method").map(row).join("");

    // newest group photo that actually exists (GROUP_PHOTOS is newest first)
    const fig = $("#team-photo");
    const photos = (window.GROUP_PHOTOS || []).slice();
    const tryNext = () => {
      const g = photos.shift();
      if (!g) { fig.classList.add("missing"); return; }
      const im = new Image();
      im.onload = () => {
        im.alt = "picoGIGA Lab group photo" + (g.caption ? ", " + g.caption : "");
        fig.insertBefore(im, fig.firstChild);
        $("figcaption", fig).textContent = g.caption || "";
      };
      im.onerror = tryNext;
      im.src = g.src;
    };
    tryNext();

    $("#recent-pubs").innerHTML = PUBS.filter((p) => p.type === "journal" || p.type === "preprint").slice(0, 4).map(pubCard).join("");

    const latest = (window.NEWS || []).filter((n) => n.text).slice(0, 3);
    $("#latest-news").innerHTML = latest.map((n) => `
      <a class="news-row reveal" href="news.html" data-img>
        <div class="ph"><div class="pattern"></div>${img("assets/img/news/" + n.img, n.title)}</div>
        <div class="body"><div class="ny">${n.y}</div><h3>${esc(n.title)}</h3><p>${esc(n.text)}</p></div>
      </a>`).join("");
  }

  function research() {
    $$("[data-icon]").forEach((el) => { el.innerHTML = ICONS[el.dataset.icon] || ""; });
    const PROJ = window.PROJECTS || [];
    const now = new Date().toISOString().slice(0, 7);
    const ongoing = (x) => x.e >= now;
    const period = (x) => `${x.s.replace("-", ".")} – ${x.e.replace("-", ".")}`;
    const projItem = (x) => `<li><b>${esc(x.t)}</b><span>${esc(x.p)} · ${period(x)}</span></li>`;

    $$(".area[id]").forEach((area) => {
      const papers = PUBS.filter((p) => p.type !== "patent" && (p.topics || []).includes(area.id));
      const patents = PUBS.filter((p) => p.type === "patent" && (p.topics || []).includes(area.id));
      const projs = PROJ.filter((x) => (x.topics || []).includes(area.id))
        .sort((x, y) => (ongoing(y) - ongoing(x)) || (y.s > x.s ? 1 : -1));
      if (!papers.length && !projs.length) return;
      const box = document.createElement("div");
      box.className = "related reveal";
      box.innerHTML = `
        ${papers.length ? `<div>
          <div class="related-head">
            <h3>Related papers</h3>
            <a class="link-arrow" href="publications.html?topic=${area.id}">All ${papers.length}${patents.length ? ` · ${patents.length} patents` : ""} ${ICONS.arrow}</a>
          </div>
          <ul>${papers.slice(0, 3).map((p) => `<li><a href="${esc(p.u || "publications.html?topic=" + area.id)}"${p.u ? ' target="_blank" rel="noopener"' : ""}>${esc(p.t)}</a><span>${esc(p.j || "")}${p.j ? " · " : ""}${p.y || ""}</span></li>`).join("")}</ul>
        </div>` : ""}
        ${projs.length ? `<div>
          <div class="related-head">
            <h3>Related projects</h3>
            <a class="link-arrow" href="#projects">All ${projs.length} ${ICONS.arrow}</a>
          </div>
          <ul>${projs.slice(0, 3).map(projItem).join("")}</ul>
        </div>` : ""}`;
      area.appendChild(box);
    });

    const list = $("#project-list");
    if (list && PROJ.length) {
      const on = PROJ.filter(ongoing), done = PROJ.filter((x) => !ongoing(x));
      list.innerHTML = `
        <h3 class="proj-group">Ongoing <span>${on.length}</span></h3><ul class="proj-list">${on.map(projItem).join("")}</ul>
        <h3 class="proj-group">Completed <span>${done.length}</span></h3><ul class="proj-list">${done.map(projItem).join("")}</ul>`;
    }

    const links = $$(".subnav a");
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    if (!("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        links.forEach((l) => l.classList.remove("active"));
        const a = map.get(en.target.id);
        if (a) {
          a.classList.add("active");
          if (window.innerWidth <= 960) a.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
        }
      });
    }, { rootMargin: "-35% 0px -60% 0px" });
    $$(".area[id], #projects, #resources").forEach((s) => io.observe(s));
  }

  function people() {
    const P = window.PI;
    $("#pi").innerHTML = `
      <div class="portrait reveal"><div class="initials">KK</div><img src="${esc(P.photo)}" alt="${esc(P.name)}" onerror="this.remove()"></div>
      <div class="reveal">
        <div class="eyebrow">Principal Investigator</div>
        <h2>Dr. ${esc(P.name)}<span class="ko">${esc(P.ko)}</span></h2>
        <p class="role">${esc(P.title)}, ${esc(P.affiliation)}</p>
        <a class="link-arrow" href="mailto:${esc(P.email)}">${esc(P.email)} ${ICONS.arrow}</a>
        <ul class="timeline">
          ${P.career.map((c) => `<li><div class="when">${esc(c.period)}</div><div class="what">${esc(c.role)}</div><div class="where">${esc(c.place)}</div></li>`).join("")}
        </ul>
      </div>`;

    $("#members").innerHTML = window.MEMBERS.map((g) => `
      <div class="member-group">
        <h3>${esc(g.group)}<span>${g.people.length}</span></h3>
        <div class="members">
          ${g.people.map((m) => `
            <article class="member reveal">
              <div class="portrait"><div class="initials">${initials(m.name)}</div><img src="assets/img/people/${esc(m.photo)}" alt="${esc(m.name)}" loading="lazy" onerror="this.remove()"></div>
              <div class="member-body">
                <h4>${esc(m.name)}<span class="ko">${esc(m.ko)}</span></h4>
                ${m.role ? `<div class="mrole">${esc(m.role)}</div>` : ""}
                ${m.interests ? `<div class="interests">${m.interests.map(esc).join(" · ")}</div>` : ""}
                ${m.email ? `<a class="mail" href="mailto:${esc(m.email)}">${ICONS.mail}${esc(m.email)}</a>` : ""}
              </div>
            </article>`).join("")}
        </div>
      </div>`).join("");

    const al = $("#alumni");
    if (al) al.innerHTML = (window.ALUMNI || []).map((m) => `
      <li class="reveal"><span class="who">${esc(m.name)}<span class="ko">${esc(m.ko)}</span></span><span class="was">${esc(m.was)}</span><span class="now">${esc(m.now)}</span></li>`).join("");

    const photos = window.GROUP_PHOTOS;
    $("#group-photos").innerHTML = photos.map((g) => `
      <button class="shot reveal" data-img type="button">
        <div class="ph pattern">${img(g.src, "Group photo, " + g.caption)}</div>
        <figcaption>${esc(g.caption)}</figcaption>
      </button>`).join("");
    bindLightbox("#group-photos .shot", photos.map((g) => ({ src: g.src, title: "picoGIGA Lab", text: g.caption })));
  }

  function news() {
    const items = window.NEWS;
    const years = [...new Set(items.map((n) => n.y))];
    $("#news-groups").innerHTML = years.map((y) => `
      <section class="year-block">
        <div class="year-head"><h2>${y}</h2></div>
        <div class="news-grid">
          ${items.filter((n) => n.y === y).map((n) => `
            <button class="news-card reveal" type="button" data-img>
              <div class="ph">${n.img ? img("assets/img/news/" + n.img, n.title) : ""}</div>
              <div class="body"><h3>${esc(n.title)}</h3>${n.text ? `<p>${esc(n.text)}</p>` : ""}</div>
            </button>`).join("")}
        </div>
      </section>`).join("");
    const ordered = years.flatMap((y) => items.filter((n) => n.y === y));
    bindLightbox(".news-card", ordered.map((n) => ({ src: "assets/img/news/" + n.img, title: n.title, text: n.text })));
  }

  /* ---------- Boot ---------- */
  renderChrome();
  ({ home, research, people, publications, news }[page] || (() => {}))();
  reveal();
})();
