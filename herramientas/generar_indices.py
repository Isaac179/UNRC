#!/usr/bin/env python3
"""Genera el index.html de cada UCA a partir de lo que realmente hay en disco.

Regla: el índice solo enlaza trabajo real. Los cascarones generados en lote
(los que traen el marcador "[Tema del módulo]") se listan como "sin publicar"
y no reciben enlace, para no mandar a nadie a trabajo falso.

Se vuelve a correr cuantas veces haga falta; es idempotente.

    python herramientas/generar_indices.py

Lee el plan de estudios de assets/js/data.js, que sigue siendo la fuente única
de verdad: si una UCA no está ahí, no se le genera índice.
"""

import html
import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA_JS = RAIZ / "assets" / "js" / "data.js"

# Marcadores de los lotes de cascarones generados automáticamente (may-jun 2026).
# El segundo lote (los *_moodle.html de unos 5 KB) no trae "[Tema del módulo]":
# trae un texto de relleno genérico firmado "UNRC · Mayo 2026".
MARCAS_CASCARON = (
    "[Tema del módulo]",
    "Esta actividad del módulo",
)
# Un PDF solo cuenta como trabajo propio si lleva el apellido del autor en el
# nombre: así los contenidos nucleares y lecturas nunca se enlazan.
FIRMA_PDF = "moctezuma"
# Marcador de las páginas ya migradas a la plantilla del portafolio.
MARCA_MIGRADA = "portafolio.css"


def _ignorados():
    """Archivos que git ignora (.gitignore): están en el disco pero nunca se
    publican, así que el índice no debe enlazarlos (p. ej. *_compressed.pdf)."""
    try:
        salida = subprocess.run(
            ["git", "ls-files", "--others", "--ignored", "--exclude-standard", "-z"],
            cwd=RAIZ, capture_output=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return set()
    return {(RAIZ / r.decode("utf-8")).resolve() for r in salida.split(b"\0") if r}


IGNORADOS = _ignorados()


def publicable(ruta):
    return ruta.resolve() not in IGNORADOS

TIPOS = [
    ("foro", "Foro", "F"),
    ("tarea", "Tarea", "T"),
    ("ta", "Tarea auténtica", "TA"),
]
INTEGRADORA = ("integradora", "Actividad integradora", "AI")


def leer_plan():
    """Extrae semestres y UCA de data.js sin necesidad de un intérprete JS."""
    fuente = DATA_JS.read_text(encoding="utf-8")
    semestres = []
    for bloque in re.finditer(
        r"\{\s*\n?\s*n:\s*(\d+),\s*estado:\s*\"([^\"]+)\",\s*\n\s*ucas:\s*\[(.*?)\]",
        fuente,
        re.S,
    ):
        n, estado, cuerpo = int(bloque.group(1)), bloque.group(2), bloque.group(3)
        ucas = [
            {"n": int(m.group(1)), "slug": m.group(2), "nombre": m.group(3)}
            for m in re.finditer(
                r"\{\s*n:\s*(\d+),\s*slug:\s*\"([^\"]+)\",\s*nombre:\s*\"([^\"]+)\"\s*\}",
                cuerpo,
            )
        ]
        if ucas:
            semestres.append({"n": n, "estado": estado, "ucas": ucas})
    return semestres


def limpiar(texto):
    """Quita etiquetas internas y normaliza espacios de un título."""
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = html.unescape(texto)
    return re.sub(r"\s+", " ", texto).strip()


def clasificar(ruta):
    """Devuelve (estado, titulo) de un archivo de actividad.

    estado: "publicada" (migrada), "anterior" (real, formato viejo),
            "cascaron" o "ausente".
    """
    if not ruta.exists():
        return "ausente", None

    if ruta.suffix.lower() == ".pdf":
        titulo = ruta.stem.replace("_", " ").strip()
        return "pdf", titulo

    contenido = ruta.read_text(encoding="utf-8", errors="replace")

    if any(marca in contenido for marca in MARCAS_CASCARON):
        return "cascaron", None

    if MARCA_MIGRADA in contenido:
        m = re.search(r'<h1 class="doc-titulo">(.*?)</h1>', contenido, re.S)
        return "publicada", limpiar(m.group(1)) if m else None

    # Trabajo real que todavía no pasa por la plantilla del portafolio.
    m = re.search(r"<title>(.*?)</title>", contenido, re.S)
    titulo = limpiar(m.group(1)).split("·")[0].strip() if m else None
    return "anterior", titulo or None


def candidatos(carpeta, tipo, modulo):
    """Nombres de archivo posibles para una casilla del plan.

    La integradora aparece en el repo como integradora.html y, en algunas UCA,
    como integradora5.html (heredado de la numeración por módulo).

    Orden de preferencia: página migrada a la plantilla, versión tal como se
    pegó en Moodle (*_moodle.html) y, al final, el PDF entregado.
    """
    pdfs = sorted(
        p for p in carpeta.glob("*.pdf") if FIRMA_PDF in p.name.lower() and publicable(p)
    )
    if tipo == "integradora":
        return (
            [carpeta / "integradora.html", carpeta / "integradora5.html"]
            + [p for p in pdfs if re.search(r"integradora|_ai[_.]", p.name, re.I)]
        )
    html_cands = [carpeta / f"{tipo}{modulo}.html", carpeta / f"{tipo}{modulo}_moodle.html"]
    if tipo != "ta":
        return html_cands
    patron_modulo = re.compile(rf"(?:_U|_M|Modulo_?){modulo}(?:[_.\s]|$)", re.I)
    patron_ta = re.compile(r"_EA[_.]|_TA[_.]|Tarea_Autentica|Infografia", re.I)
    return html_cands + [
        p for p in pdfs if patron_modulo.search(p.name) and patron_ta.search(p.name)
    ]


def casilla(carpeta, tipo, etiqueta, sigla, modulo):
    for ruta in candidatos(carpeta, tipo, modulo):
        estado, titulo = clasificar(ruta)
        if estado in ("publicada", "anterior", "pdf"):
            return {
                "sigla": sigla,
                "etiqueta": etiqueta,
                "estado": estado,
                "titulo": titulo or etiqueta,
                "archivo": ruta.name,
            }
    return {
        "sigla": sigla,
        "etiqueta": etiqueta,
        "estado": "sin publicar",
        "titulo": None,
        "archivo": None,
    }


def fila(c):
    if c["archivo"]:
        nombre = (
            f'<a href="{html.escape(c["archivo"])}">{html.escape(c["titulo"])}</a>'
        )
        marca = "publicada" if c["estado"] == "publicada" else "anterior"
        estado = {
            "publicada": "Publicada",
            "anterior": "Formato anterior",
            "pdf": "PDF entregado",
        }[c["estado"]]
    else:
        nombre = f'<span class="indice-vacia">{html.escape(c["etiqueta"])}</span>'
        marca, estado = "", "Sin publicar"
    return (
        "        <li>\n"
        f'          <span class="indice-sigla">{c["sigla"]}</span>\n'
        f"          {nombre}\n"
        f'          <span class="indice-estado {marca}">{estado}</span>\n'
        "        </li>"
    )


PUBLICADAS = {}   # "sem|slug|tipo|modulo" -> ruta relativa a la raíz


def registrar(semestre, uca, tipo, modulo, c):
    if c["archivo"]:
        clave = f"{semestre['n']}|{uca['slug']}|{tipo}|{modulo or ''}"
        PUBLICADAS[clave] = f"semestre_{semestre['n']}/{uca['slug']}/{c['archivo']}"


def otros(carpeta, usados):
    """Trabajos propios que no ocupan una casilla del plan (mapas, tableros,
    foros de reforzamiento, respuestas). Se enlazan aparte, con su título."""
    filas = []
    for ruta in sorted(carpeta.iterdir()):
        if ruta.name in usados or ruta.name == "index.html" or not ruta.is_file():
            continue
        if not publicable(ruta):
            continue
        if ruta.suffix.lower() == ".pdf" and FIRMA_PDF not in ruta.name.lower():
            continue
        if ruta.suffix.lower() not in (".html", ".pdf"):
            continue
        estado, titulo = clasificar(ruta)
        if estado not in ("publicada", "anterior", "pdf"):
            continue
        filas.append({
            "sigla": "PDF" if estado == "pdf" else "·",
            "etiqueta": titulo or ruta.stem,
            "estado": estado,
            "titulo": titulo or ruta.stem,
            "archivo": ruta.name,
        })
    return filas


def construir(semestre, uca, carpeta):
    modulos, publicadas, total = [], 0, 0
    usados = set()

    for m in range(1, 5):
        filas = []
        for tipo, etiqueta, sigla in TIPOS:
            c = casilla(carpeta, tipo, etiqueta, sigla, m)
            total += 1
            if c["archivo"]:
                publicadas += 1
                usados.add(c["archivo"])
            registrar(semestre, uca, tipo, m, c)
            filas.append(fila(c))
        modulos.append(
            f'      <section class="indice-modulo">\n'
            f"        <h2>Módulo {m}</h2>\n"
            f'        <ul class="indice-lista">\n'
            + "\n".join(filas)
            + "\n        </ul>\n      </section>"
        )

    tipo, etiqueta, sigla = INTEGRADORA
    c = casilla(carpeta, tipo, etiqueta, sigla, None)
    total += 1
    if c["archivo"]:
        publicadas += 1
        usados.add(c["archivo"])
    registrar(semestre, uca, tipo, None, c)
    modulos.append(
        '      <section class="indice-modulo">\n'
        "        <h2>Cierre de la UCA</h2>\n"
        '        <ul class="indice-lista">\n'
        + fila(c)
        + "\n        </ul>\n      </section>"
    )

    extras = otros(carpeta, usados)
    if extras:
        modulos.append(
            '      <section class="indice-modulo">\n'
            "        <h2>Otros trabajos de la UCA</h2>\n"
            '        <ul class="indice-lista">\n'
            + "\n".join(fila(e) for e in extras)
            + "\n        </ul>\n      </section>"
        )

    nn = f"{uca['n']:02d}"
    nombre = html.escape(uca["nombre"])
    resumen = (
        f"{publicadas} de {total} actividades publicadas"
        if publicadas
        else "Sin entregas publicadas todavía"
    )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{nombre} · UCA {nn} · LRIN</title>
<meta name="description" content="Índice de actividades publicadas de la UCA {nn}, {nombre}. Isaac Moctezuma Calderón, LRIN, Universidad Rosario Castellanos.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,300;0,600;1,400&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/UNRC/assets/css/portafolio.css">
</head>
<body>

<main class="doc">

  <header class="doc-cabecera">
    <span class="folio">{nn}</span>
    <p class="doc-uca">Semestre {semestre['n']} · {semestre['estado']}</p>
    <h1 class="doc-titulo">{nombre}</h1>
    <p class="doc-meta">
      <span>{resumen}</span>
      <span>Isaac Moctezuma Calderón</span>
    </p>
  </header>

  <div class="indice">
{chr(10).join(modulos)}
  </div>

  <p class="nota-fuentes">Solo se enlaza el trabajo efectivamente entregado. Las
  casillas sin publicar corresponden a actividades que aún no se migran al
  portafolio.</p>

</main>

<script src="/UNRC/assets/js/data.js"></script>
<script src="/UNRC/assets/js/nav.js"></script>
</body>
</html>
"""


def contar(carpeta):
    """Cuántas casillas de una UCA tienen trabajo enlazable."""
    total = publicadas = 0
    for m in range(1, 5):
        for tipo, etiqueta, sigla in TIPOS:
            total += 1
            publicadas += bool(casilla(carpeta, tipo, etiqueta, sigla, m)["archivo"])
    tipo, etiqueta, sigla = INTEGRADORA
    total += 1
    publicadas += bool(casilla(carpeta, tipo, etiqueta, sigla, None)["archivo"])
    return publicadas, total


def construir_semestre(semestre):
    """Índice de un semestre: sus seis UCA, con cuántas entregas tiene cada una."""
    filas = []
    for uca in semestre["ucas"]:
        carpeta = RAIZ / f"semestre_{semestre['n']}" / uca["slug"]
        nn = f"{uca['n']:02d}"
        nombre = html.escape(uca["nombre"])
        if carpeta.is_dir():
            publicadas, total = contar(carpeta)
            enlace = f'<a href="{html.escape(uca["slug"])}/index.html">{nombre}</a>'
            marca = "publicada" if publicadas else ""
            estado = f"{publicadas} de {total}" if publicadas else "Sin publicar"
        else:
            enlace = f'<span class="indice-vacia">{nombre}</span>'
            marca, estado = "", "Sin carpeta"
        filas.append(
            "        <li>\n"
            f'          <span class="indice-sigla">{nn}</span>\n'
            f"          {enlace}\n"
            f'          <span class="indice-estado {marca}">{estado}</span>\n'
            "        </li>"
        )
    n = semestre["n"]
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Semestre {n} · LRIN</title>
<meta name="description" content="Índice del semestre {n} del portafolio de Isaac Moctezuma Calderón, LRIN, Universidad Rosario Castellanos.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,300;0,600;1,400&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/UNRC/assets/css/portafolio.css">
</head>
<body>

<main class="doc">

  <header class="doc-cabecera">
    <span class="folio">S{n}</span>
    <p class="doc-uca">Semestre {n} · {semestre['estado']}</p>
    <h1 class="doc-titulo">Semestre {n}</h1>
    <p class="doc-meta">
      <span>{len(semestre['ucas'])} unidades de aprendizaje</span>
      <span>Isaac Moctezuma Calderón</span>
    </p>
  </header>

  <div class="indice">
      <section class="indice-modulo">
        <h2>Unidades de aprendizaje</h2>
        <ul class="indice-lista">
{chr(10).join(filas)}
        </ul>
      </section>
  </div>

  <p class="nota-fuentes">El número de la derecha cuenta las actividades con
  trabajo entregado y enlazado, de las trece de cada UCA
  (cuatro módulos con foro, tarea y tarea auténtica, más la integradora).</p>

</main>

<script src="/UNRC/assets/js/data.js"></script>
<script src="/UNRC/assets/js/nav.js"></script>
</body>
</html>
"""


HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,300;0,600;1,400&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/UNRC/assets/css/portafolio.css">
</head>
<body>
"""


PROYECTOS = [
    {
        "ruta": "proyectos/ruptura_tribunal/index.html",
        "nombre": "Ruptura & Tribunal",
        "tipo": "Simulador",
        "descripcion": "Simulador con dados que une Derecho Internacional Público, Historia Contemporánea y Pensamiento Político y Social.",
    },
    {
        "ruta": "proyectos/ruptura_tribunal/corpus_juridico.html",
        "nombre": "Arsenal jurídico del simulador",
        "tipo": "Fichas",
        "descripcion": "Fichas de tratados, principios, jurisprudencia y mecanismos que usa el simulador.",
    },
]


def construir_portada(semestres):
    filas = []
    for semestre in semestres:
        n = semestre["n"]
        publicadas = total = 0
        for uca in semestre["ucas"]:
            carpeta = RAIZ / f"semestre_{n}" / uca["slug"]
            if carpeta.is_dir():
                p, t = contar(carpeta)
                publicadas, total = publicadas + p, total + t
        filas.append(
            "        <li>\n"
            f'          <span class="indice-sigla">S{n}</span>\n'
            f'          <a href="semestre_{n}/index.html">Semestre {n} · UCA {semestre["ucas"][0]["n"]:02d}–{semestre["ucas"][-1]["n"]:02d}</a>\n'
            f'          <span class="indice-estado {"publicada" if publicadas else ""}">{semestre["estado"]} · {publicadas} de {total}</span>\n'
            "        </li>"
        )
    proyectos = "\n".join(
        "        <li>\n"
        '          <span class="indice-sigla">P</span>\n'
        f'          <a href="{html.escape(p["ruta"])}" title="{html.escape(p["descripcion"])}">{html.escape(p["nombre"])}</a>\n'
        f'          <span class="indice-estado publicada">{html.escape(p["tipo"])}</span>\n'
        "        </li>"
        for p in PROYECTOS
        if (RAIZ / p["ruta"]).exists()
    )
    return HEAD.format(
        titulo="Portafolio de evidencias · Isaac Moctezuma Calderón · LRIN UNRC",
        descripcion="Portafolio académico de Isaac Moctezuma Calderón, Licenciatura en Relaciones Internacionales, Universidad Rosario Castellanos. Trabajos entregados, tal como se entregaron.",
    ) + f"""
<main class="doc">

  <header class="doc-cabecera">
    <span class="folio">LRIN</span>
    <p class="doc-uca">Universidad Rosario Castellanos · Plan 2023 · Modalidad no escolarizada</p>
    <h1 class="doc-titulo">Portafolio de evidencias</h1>
    <p class="doc-meta">
      <span>Isaac Moctezuma Calderón</span>
      <span>Licenciatura en Relaciones Internacionales</span>
    </p>
  </header>

  <div class="indice">
      <section class="indice-modulo">
        <h2>Semestres</h2>
        <ul class="indice-lista">
{chr(10).join(filas)}
        </ul>
      </section>
      <section class="indice-modulo">
        <h2>Proyectos</h2>
        <ul class="indice-lista">
{proyectos}
        </ul>
      </section>
  </div>

  <p class="nota-fuentes">Cada trabajo se publica tal como se entregó: sin
  correcciones posteriores. Las lecturas y materiales de los cursos pertenecen a
  sus autores y no se reproducen aquí.</p>

</main>

<script src="/UNRC/assets/js/data.js"></script>
<script src="/UNRC/assets/js/nav.js"></script>
</body>
</html>
"""


def escribir_publicadas():
    import json
    destino = RAIZ / "assets" / "js" / "publicadas.js"
    cuerpo = json.dumps(dict(sorted(PUBLICADAS.items())), ensure_ascii=False, indent=1)
    destino.write_text(
        "/* publicadas.js — GENERADO por herramientas/generar_indices.py. No editar.\n"
        "   Clave: semestre|uca|tipo|módulo → archivo enlazado. nav.js lo usa para que\n"
        "   «anterior / siguiente» solo apunte a trabajo publicado. */\n"
        f"const PUBLICADAS = {cuerpo};\n",
        encoding="utf-8",
    )
    print(f"  [ok] {destino.relative_to(RAIZ)} ({len(PUBLICADAS)} actividades)")


def main():
    escritos = 0
    for semestre in leer_plan():
        for uca in semestre["ucas"]:
            carpeta = RAIZ / f"semestre_{semestre['n']}" / uca["slug"]
            if not carpeta.is_dir():
                print(f"  [!] sin carpeta: {carpeta.relative_to(RAIZ)}")
                continue
            destino = carpeta / "index.html"
            destino.write_text(construir(semestre, uca, carpeta), encoding="utf-8")
            escritos += 1
            print(f"  [ok] {destino.relative_to(RAIZ)}")
        carpeta_sem = RAIZ / f"semestre_{semestre['n']}"
        if carpeta_sem.is_dir():
            destino = carpeta_sem / "index.html"
            destino.write_text(construir_semestre(semestre), encoding="utf-8")
            escritos += 1
            print(f"  [ok] {destino.relative_to(RAIZ)}")
    semestres = leer_plan()
    (RAIZ / "index.html").write_text(construir_portada(semestres), encoding="utf-8")
    print("  [ok] index.html")
    escribir_publicadas()
    print(f"\n{escritos + 1} índices generados.")


if __name__ == "__main__":
    main()
