#!/usr/bin/env python3
"""Verifica que el repositorio cumpla la regla del restaurante antes de publicar.

    python herramientas/verificar_restaurante.py

Falla (código 1) si encuentra:
  1. Material de terceros o de trabajo: lecturas, contenidos de los cursos,
     audio y video, prompts, gemelo digital, briefs internos.
  2. PDF que no sean de autoría propia (sin el apellido del autor en el nombre).
  3. Cascarones: páginas de relleno sin trabajo real.
  4. Enlaces internos rotos (href/src a archivos del propio sitio).

Se corre en cada push con GitHub Actions (.github/workflows/verificar.yml).
"""

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "herramientas"))
from generar_indices import MARCAS_CASCARON, FIRMA_PDF  # noqa: E402

PROHIBIDOS = [
    (r"(^|/)LIT/", "lecturas (van a la despensa)"),
    (r"sre_fondo_sdocumentales_primarios", "fondos documentales de terceros"),
    (r"contenido[_ ]nuclear|NUCLEAR_FULL|_Contenido\b|Contenido Nuclear", "contenido de los cursos"),
    (r"\.(aup3|mp3|wav|mp4|zip|exe|epub|docx)$", "binario o archivo de trabajo"),
    (r"prompt|gemelo|digital_twin|alma_isaac", "material privado de cocina"),
    (r"(^|/)MIGRACION\.md$|(^|/)MIS DISE", "brief o fuente de trabajo"),
    (r"(^|/)CV_", "datos personales"),
    (r"_plantilla\.html$", "plantilla con huecos"),
]


# Huecos de imagen que el trabajo entregado ya traía: se dejan como evidencia.
MARCADORES_DE_IMAGEN = {"URL_DE_TU_IMAGEN", "ruta-o-url.jpg"}


def rastreados():
    salida = subprocess.run(
        ["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, check=True
    ).stdout.decode("utf-8")
    return [p for p in salida.split("\0") if p]


def enlaces(html_text):
    for m in re.finditer(r'(?:href|src)\s*=\s*"([^"]+)"', html_text):
        yield m.group(1)


def main():
    errores = []
    archivos = rastreados()
    existentes = set(archivos)

    for ruta in archivos:
        for patron, motivo in PROHIBIDOS:
            if re.search(patron, ruta, re.I):
                errores.append(f"[prohibido] {ruta} — {motivo}")
        if ruta.lower().endswith(".pdf") and FIRMA_PDF not in ruta.lower():
            errores.append(f"[pdf ajeno] {ruta} — el nombre no lleva «{FIRMA_PDF}»")

    for ruta in archivos:
        if not ruta.endswith(".html"):
            continue
        texto = (RAIZ / ruta).read_text(encoding="utf-8", errors="replace")
        if any(m in texto for m in MARCAS_CASCARON):
            errores.append(f"[cascarón] {ruta}")
        base = Path(ruta).parent
        for url in enlaces(texto):
            partes = urlsplit(url)
            if partes.scheme or url.startswith(("#", "mailto:", "data:", "javascript:")) or "${" in url:
                continue
            destino = unquote(partes.path)
            if not destino or destino in MARCADORES_DE_IMAGEN:
                continue
            if destino.startswith("/UNRC/"):
                objetivo = Path(destino[len("/UNRC/"):])
            elif destino.startswith("/"):
                continue
            else:
                objetivo = base / destino
            objetivo = Path(*[p for p in objetivo.as_posix().split("/") if p not in ("", ".")])
            normal = []
            for parte in objetivo.parts:
                if parte == "..":
                    if normal:
                        normal.pop()
                else:
                    normal.append(parte)
            clave = "/".join(normal)
            if clave.endswith("/") or (clave and "." not in normal[-1]):
                clave = (clave + "/index.html").lstrip("/")
            if clave and clave not in existentes:
                errores.append(f"[enlace roto] {ruta} → {url}")

    if errores:
        print(f"{len(errores)} problema(s):")
        for e in errores:
            print("  " + e)
        sys.exit(1)
    print(f"Restaurante en orden: {len(archivos)} archivos revisados.")


if __name__ == "__main__":
    main()
