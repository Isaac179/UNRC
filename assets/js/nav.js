/* =====================================================================
   nav.js — Genera la navegación persistente desde data.js
   Incluir en cada página:  <script src="/UNRC/assets/js/data.js"></script>
                            <script src="/UNRC/assets/js/nav.js"></script>
   No requiere configuración por página: se ubica sola leyendo la URL.
   ===================================================================== */

(function () {
  "use strict";

  const BASE = (function () {
    // Funciona igual en github.io/UNRC/ y en local
    const p = location.pathname;
    const i = p.indexOf("/semestre_");
    return i === -1 ? p.replace(/[^/]*$/, "") : p.slice(0, i + 1);
  })();

  // ---- Ubicar la página actual dentro del plan -----------------------
  function ubicar() {
    const m = location.pathname.match(/semestre_(\d)\/(\d{2}_[^/]+)\/([^/]+)\.html/);
    if (!m) return null;
    const [, sem, ucaSlug, archivo] = m;
    const semestre = PLAN.semestres.find(s => s.n === +sem);
    const uca = semestre && semestre.ucas.find(u => u.slug === ucaSlug);
    const tm = archivo.match(/^([a-z_]+?)(\d*)$/);
    return { semestre, uca, tipo: tm ? tm[1] : archivo, modulo: tm && tm[2] ? +tm[2] : null };
  }

  const aqui = ubicar();

  // ---- Construir el menú --------------------------------------------
  function construir() {
    const nav = document.createElement("nav");
    nav.className = "nav-persistente";
    nav.setAttribute("aria-label", "Navegación del portafolio");

    const marca = `<a class="nav-marca" href="${BASE}index.html">
        <span class="nav-sigla">LRIN</span>
        <span class="nav-sub">Portafolio</span>
      </a>`;

    const items = PLAN.semestres.filter(s => s.ucas.length).map(s => {
      const abierto = aqui && aqui.semestre && aqui.semestre.n === s.n;
      const ucas = s.ucas.map(u => {
        const activa = aqui && aqui.uca && aqui.uca.slug === u.slug;
        return `<li><a href="${BASE}semestre_${s.n}/${u.slug}/index.html"
                   class="${activa ? "activa" : ""}">
                   <span class="uca-n">${String(u.n).padStart(2, "0")}</span>
                   <span class="uca-nombre">${u.nombre}</span></a></li>`;
      }).join("");
      return `<li class="nav-sem ${abierto ? "abierto" : ""}">
                <button class="nav-sem-btn" aria-expanded="${abierto}">
                  Semestre ${s.n}<span class="nav-estado">${s.estado}</span>
                </button>
                <ul class="nav-ucas">${ucas}</ul>
              </li>`;
    }).join("");

    nav.innerHTML = `${marca}
      <button class="nav-toggle" aria-label="Abrir navegación" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav-lista">${items}</ul>`;

    return nav;
  }

  // ---- Migas de pan ---------------------------------------------------
  function migas() {
    if (!aqui || !aqui.uca) return null;
    const t = TIPOS[aqui.tipo];
    const el = document.createElement("div");
    el.className = "migas";
    el.innerHTML = `
      <a href="${BASE}index.html">Portafolio</a>
      <span aria-hidden="true">›</span>
      <a href="${BASE}semestre_${aqui.semestre.n}/index.html">Semestre ${aqui.semestre.n}</a>
      <span aria-hidden="true">›</span>
      <a href="${BASE}semestre_${aqui.semestre.n}/${aqui.uca.slug}/index.html">UCA ${String(aqui.uca.n).padStart(2, "0")}</a>
      <span aria-hidden="true">›</span>
      <span class="miga-actual">${t ? t.etiqueta : aqui.tipo}${aqui.modulo ? " · Módulo " + aqui.modulo : ""}</span>`;
    return el;
  }

  // ---- Anterior / siguiente dentro de la UCA --------------------------
  function secuencia() {
    if (!aqui || !aqui.uca) return null;
    const orden = [];
    for (let m = 1; m <= 4; m++) PLAN.modulo.forEach(t => orden.push({ tipo: t, modulo: m }));
    orden.push({ tipo: "integradora", modulo: null });

    const i = orden.findIndex(o => o.tipo === aqui.tipo && o.modulo === aqui.modulo);
    if (i === -1) return null;

    const enlace = (o, dir) => {
      if (!o) return `<span class="secuencia-vacia"></span>`;
      const href = BASE + rutaActividad(aqui.semestre.n, aqui.uca.slug, o.tipo, o.modulo);
      const t = TIPOS[o.tipo];
      return `<a class="secuencia-${dir}" href="${href}">
                <span class="secuencia-dir">${dir === "prev" ? "Anterior" : "Siguiente"}</span>
                <span class="secuencia-nombre">${t.etiqueta}${o.modulo ? " " + o.modulo : ""}</span>
              </a>`;
    };

    const el = document.createElement("nav");
    el.className = "secuencia";
    el.setAttribute("aria-label", "Actividad anterior y siguiente");
    el.innerHTML = enlace(orden[i - 1], "prev") + enlace(orden[i + 1], "next");
    return el;
  }

  // ---- Montar ---------------------------------------------------------
  document.addEventListener("DOMContentLoaded", function () {
    const nav = construir();
    document.body.insertBefore(nav, document.body.firstChild);

    const cabecera = document.querySelector(".doc-cabecera");
    const mg = migas();
    if (mg && cabecera) cabecera.insertBefore(mg, cabecera.firstChild);

    const sq = secuencia();
    const cuerpo = document.querySelector(".doc");
    if (sq && cuerpo) cuerpo.appendChild(sq);

    nav.querySelector(".nav-toggle").addEventListener("click", function () {
      const abierta = nav.classList.toggle("abierta");
      this.setAttribute("aria-expanded", abierta);
    });

    nav.querySelectorAll(".nav-sem-btn").forEach(function (b) {
      b.addEventListener("click", function () {
        const li = b.parentElement;
        const abierto = li.classList.toggle("abierto");
        b.setAttribute("aria-expanded", abierto);
      });
    });
  });
})();
