/* =====================================================================
   data.js — Fuente única de verdad del plan de estudios LRIN
   Toda la navegación del sitio se genera desde este archivo.
   Para agregar una actividad: agrégala aquí. No edites ningún menú.
   ===================================================================== */

const PLAN = {
  carrera: "Licenciatura en Relaciones Internacionales",
  plan: "2023 · Modalidad no escolarizada",
  autor: "Isaac Moctezuma Calderón",

  /* Estructura de evaluación común a todas las UCA de los primeros
     semestres: 4 módulos, cada uno con foro, tarea auténtica y,
     al cierre, una actividad integradora. */
  modulo: ["foro", "tarea", "ta"],
  cierre: "integradora",

  semestres: [
    {
      n: 1, estado: "concluido",
      ucas: [
        { n: 1,  slug: "01_introduccion_a_la_investigacion_en_ciencias_sociales", nombre: "Introducción a la Investigación en Ciencias Sociales" },
        { n: 2,  slug: "02_escritura_argumentativa", nombre: "Escritura Argumentativa" },
        { n: 3,  slug: "03_introduccion_al_estudio_de_las_relaciones_internacionales", nombre: "Introducción al Estudio de las Relaciones Internacionales" },
        { n: 4,  slug: "04_perspectiva_de_genero_para_el_diseno_social", nombre: "Perspectiva de Género para el Diseño Social" },
        { n: 5,  slug: "05_historia_y_formacion_del_estado_mexicano_y_politica_exterior", nombre: "Historia y Formación del Estado Mexicano y Política Exterior" },
        { n: 6,  slug: "06_geografia_politica_y_economica", nombre: "Geografía Política y Económica" }
      ]
    },
    {
      n: 2, estado: "concluido",
      ucas: [
        { n: 7,  slug: "07_derecho_constitucional_mexicano", nombre: "Derecho Constitucional Mexicano" },
        { n: 8,  slug: "08_taller_de_expresion_escrita", nombre: "Taller de Expresión Escrita" },
        { n: 9,  slug: "09_historia_y_formacion_del_estado_moderno_mexicano_y_politica_exterior", nombre: "Historia y Formación del Estado Moderno Mexicano y Política Exterior" },
        { n: 10, slug: "10_desarrollo_sostenible_equidad_y_responsabilidad_social", nombre: "Desarrollo Sostenible, Equidad y Responsabilidad Social" },
        { n: 11, slug: "11_historia_de_las_relaciones_internacionales_1815-1945", nombre: "Historia de las Relaciones Internacionales 1815–1945" },
        { n: 12, slug: "12_america_latina_y_el_caribe", nombre: "América Latina y el Caribe" }
      ]
    },
    {
      n: 3, estado: "en curso",
      ucas: [
        { n: 13, slug: "13_derecho_internacional_publico", nombre: "Derecho Internacional Público" },
        { n: 14, slug: "14_por_definir", nombre: "Por definir" },
        { n: 15, slug: "15_pensamiento_politico_y_social", nombre: "Pensamiento Político y Social" },
        { n: 16, slug: "16_pensamiento_complejo_para_la_argumentacion", nombre: "Pensamiento Complejo para la Argumentación" },
        { n: 17, slug: "17_teoria_economica", nombre: "Teoría Económica" },
        { n: 18, slug: "18_america_del_norte", nombre: "América del Norte" }
      ]
    },
    { n: 4, estado: "pendiente", ucas: [] },
    { n: 5, estado: "pendiente", ucas: [] },
    { n: 6, estado: "pendiente", ucas: [] },
    { n: 7, estado: "pendiente", ucas: [] },
    { n: 8, estado: "pendiente", ucas: [] }
  ]
};

/* Etiquetas legibles de cada tipo de actividad */
const TIPOS = {
  foro:        { etiqueta: "Foro",                sigla: "F" },
  tarea:       { etiqueta: "Tarea",               sigla: "T" },
  ta:          { etiqueta: "Tarea auténtica",     sigla: "TA" },
  integradora: { etiqueta: "Actividad integradora", sigla: "AI" }
};

/* Ruta de una actividad. Convención:
   semestre_N/NN_slug_uca/tipoM.html   (ej. semestre_2/09_.../foro4.html) */
function rutaActividad(semestre, ucaSlug, tipo, modulo) {
  const archivo = tipo === "integradora" ? "integradora.html" : `${tipo}${modulo}.html`;
  return `semestre_${semestre}/${ucaSlug}/${archivo}`;
}

if (typeof module !== "undefined") module.exports = { PLAN, TIPOS, rutaActividad };
