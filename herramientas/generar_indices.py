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
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA_JS = RAIZ / "assets" / "js" / "data.js"

# Marcador del lote de cascarones generados automáticamente (may-jun 2026).
MARCA_CASCARON = "[Tema del módulo]"
# Marcador de las páginas ya migradas a la plantilla del portafolio.
MARCA_MIGRADA = "portafolio.css"

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

    contenido = ruta.read_text(encoding="utf-8", errors="replace")

    if MARCA_CASCARON in contenido:
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
    """
    if tipo == "integradora":
        return [carpeta / "integradora.html", carpeta / "integradora5.html"]
    return [carpeta / f"{tipo}{modulo}.html"]


def casilla(carpeta, tipo, etiqueta, sigla, modulo):
    for ruta in candidatos(carpeta, tipo, modulo):
        estado, titulo = clasificar(ruta)
        if estado in ("publicada", "anterior"):
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
        estado = "Publicada" if c["estado"] == "publicada" else "Formato anterior"
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


def construir(semestre, uca, carpeta):
    modulos, publicadas, total = [], 0, 0

    for m in range(1, 5):
        filas = []
        for tipo, etiqueta, sigla in TIPOS:
            c = casilla(carpeta, tipo, etiqueta, sigla, m)
            total += 1
            if c["archivo"]:
                publicadas += 1
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
    modulos.append(
        '      <section class="indice-modulo">\n'
        "        <h2>Cierre de la UCA</h2>\n"
        '        <ul class="indice-lista">\n'
        + fila(c)
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
    print(f"\n{escritos} índices generados.")


if __name__ == "__main__":
    main()
