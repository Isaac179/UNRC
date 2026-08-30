# Migración del portafolio LRIN — brief de trabajo

Documento de traspaso. Colocar en la raíz de `C:\Users\isaac\repos\UNRC`.
Última actualización: 29 ago 2026.

---

## Contexto en una línea

Portafolio académico público de Isaac Moctezuma Calderón, LRIN plan 2023 no
escolarizada, Universidad Rosario Castellanos. Publica en
`https://isaac179.github.io/UNRC/`. Sirve además como base para titulación por
**Portafolio de Evidencias**, una de las ocho modalidades de la UNRC.

## Tres zonas, no mezclar

| Zona | Ruta | Contiene |
|---|---|---|
| Despensa | `OneDrive\Desktop\IESCDMX-Rosario-Castellanos` | Materia prima: PDF, lecturas, audios |
| Cocina | Bóveda Obsidian `LRIN-Cerebro` | Notas de trabajo, borradores |
| **Restaurante** | **`repos\UNRC`** | **Solo trabajo terminado y de autoría propia** |

Regla única: **si no se va a publicar, no entra al repo.**

---

## Arquitectura ya montada

```
assets/js/data.js          fuente única de verdad del plan de estudios
assets/js/nav.js           genera menú, migas y anterior/siguiente
assets/css/portafolio.css  estilos
semestre_2/08_taller_de_expresion_escrita/integradora.html   ← referencia
```

**Ninguna página lleva navegación escrita a mano.** `nav.js` lee la URL, se ubica
en `data.js` e inyecta todo. Para agregar una UCA se edita `data.js` y nada más.

Las UCA se numeran de corrido en toda la carrera: semestre 1 = 01–06,
semestre 2 = 07–12, semestre 3 = 13–18.

### Convención de rutas

```
semestre_N/NN_slug_de_la_uca/
  index.html          ← pendiente de generar
  foro1.html  tarea1.html  ta1.html
  foro2.html  ...
  integradora.html
```

Minúsculas, sin acentos ni espacios. GitHub Pages distingue mayúsculas.

---

## Plantilla: estructura del documento

Ver `semestre_2/08_taller_de_expresion_escrita/integradora.html` como modelo.

```
.doc
  .doc-cabecera        folio, UCA, título, subtítulo, metadatos
  .doc-cuerpo
    .texto             ← el trabajo entregado, sin modificar
    .margen            ← las notas posteriores
  .fuentes
```

Clases disponibles: `.pregunta-guia` (la pregunta que organiza el trabajo),
`.doc-subtitulo`, `.marca-continua` (marca texto incompleto), `.nota-fuentes`.

### Reglas del cuerpo

**No editar el contenido entregado.** Ni corregir, ni mejorar, ni completar. Es
evidencia; su valor está en ser lo que efectivamente se entregó. Si falta texto,
marcarlo con `.marca-continua` en vez de rellenarlo.

### Reglas del margen

El margen NO se autogenera. Requiere que Isaac relea y decida. Al migrar, dejar
el andamio con los rótulos y sin contenido inventado:

- `Qué abrió esto` — la pregunta que quedó viva
- `Conecta con` — otra UCA, con enlace
- `Eje de investigación` — cómo alimenta soberanía territorial y digital
- `Revisar` — pendientes detectados
- `Trabajo paralelo` — solo si existe realmente

---

## Mapeo confirmado

Fuente: nota `MIS DISEÑOS PARA FOROS.md` (bóveda `obsidian-unrc`, 167 KB) y su
duplicado `Diseno_HTML_Foro_Vino.md`. Los bloques HTML vienen de corrido.

**Piezas "texto plano" (sin bloque HTML pre-diseñado):** no están en la nota de
diseños. Viven en el volcado crudo del foro de Moodle de cada UCA, guardado en
`J:\Mi unidad\obsidian-unrc\UNRC\<NOMBRE DE LA UCA>.md`. Ese archivo trae el
hilo completo de la clase — todas las participaciones de todos los
compañeros —, no solo las de Isaac. Para encontrar la pieza correcta: buscar
el nombre "ISAAC MOCTEZUMA" y localizar su publicación propia (encabezada por
su foto y "#### [ISAAC MOCTEZUMA](...) respondiendo a ..."), no las respuestas
de otros estudiantes que también mencionan el mismo tema. Así se resolvió la
pieza 1 (30 ago 2026).

| # | Pieza | Destino | Estado |
|---|---|---|---|
| 1 | La encomienda y la colonización | `semestre_1/05_historia_y_formacion_del_estado_mexicano_y_politica_exterior/foro2.html` | **Migrada** — reemplazó cascarón; margen en andamio, pendiente Isaac. Fuente: `HISTORIA Y FORMACIÓN DEL ESTADO MEXICANO Y POLÍTICA EXTERIOR.md` (bóveda `obsidian-unrc`, `J:\Mi unidad\obsidian-unrc\UNRC\`) líneas 1601–1611, publicación "Mi Aporte A Nuestro Foro: El Nuevo Mundo" de Isaac Moctezuma |
| 2 | Foro integrador: desarrollo, cooperación y educación | `semestre_1/01_introduccion_a_la_investigacion_en_ciencias_sociales/` | HTML listo |
| 3 | Orígenes históricos y filosóficos de las RRII | `semestre_1/03_introduccion_al_estudio_de_las_relaciones_internacionales/foro1.html` | HTML listo |
| 4 | Del humanismo a la soberanía | `semestre_1/03_.../foro2.html` | HTML listo |
| 5 | ¿Para qué sirve hacer teorías sobre las RRII? | `semestre_1/03_.../foro3.html` | HTML listo |
| 6 | Avance de México en la implementación de los ODS | `semestre_1/03_.../foro4.html` | Confirmar con Isaac: 03 o 10 |
| 7 | Desborde ecológico y desarrollo sostenible | `semestre_2/10_desarrollo_sostenible_equidad_y_responsabilidad_social/foro4.html` | HTML listo |
| 8 | Entre el papel y la tierra | `semestre_2/08_taller_de_expresion_escrita/integradora.html` | **Ya migrada** — texto truncado, falta completar |

### Excluidos por decisión de Isaac

- **"ESCRITURA ARGUMENTATIVA"** — etiqueta y contenido no coinciden. Prueba archivada.
- **MOOC Web3 de la Universidad de Nicosia** — material de otra institución. No
  pertenece al portafolio LRIN.
- **Blog: "Una aproximación novicia a las RRII", "Nepal y Albania"** — no son
  trabajos de la UNRC. Si se publican algún día, va en `/blog/`, nunca en
  `semestre_N/`.
- **Plantillas "Stellar Adaptado"** (3 variantes) — cascarones con texto de
  relleno. Sin contenido académico.

---

## Trabajo pendiente, en orden

1. **Migrar las piezas restantes** de la tabla (2, 3, 4, 5, 6 y 7 — falta
   confirmar/generar; 1 y 8 ya migradas), respetando la regla de no editar el
   cuerpo
2. **Generar `index.html` por UCA** — el menú ya apunta a ellos y hoy dan 404
3. **Generar `index.html` por semestre**
4. **Actualizar `data.js`** si aparecen UCA o nombres nuevos
5. **Completar el texto truncado** de la integradora del Taller (dato del Censo 2020)
6. Más adelante: tareas auténticas e integradoras restantes, que están en texto
   plano y requieren trabajo de redacción, no de script

## Pendiente de confirmar con Isaac

- Pieza 6: ¿UCA 03 o UCA 10?
- Nombre de la UCA 14 del tercer semestre, cuando salga la tira de materias

---

## Advertencias

**El `.gitignore` ya excluye** ejecutables, comprimidos, audio, video, archivos de
prompts, gemelo digital, PDF `_compressed`, carpetas `LIT/` y volcados de
estructura. No relajarlo.

**Las lecturas con derechos de autor no van al repo.** Se retiraron 246 MB de
material de terceros. Viven en la despensa.

**El repo está fuera de OneDrive y Google Drive** a propósito: un árbol `.git`
bajo doble sincronización se corrompe. No moverlo de vuelta.

**El CSS usa rutas absolutas** (`/UNRC/assets/...`). Para probar en local hace
falta servidor: `python -m http.server 8000`. Abrir con doble clic no funciona.
