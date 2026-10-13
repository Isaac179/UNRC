# LRIN - Universidad Rosario Castellanos

Portafolio academico publico de la **Licenciatura en Relaciones Internacionales**, plan 2023, modalidad no escolarizada.

**Isaac Moctezuma Calderon** - Generacion 2025

**[Ver el sitio](https://isaac179.github.io/UNRC/)**

---

## Organizacion

El plan de estudios numera las UCA de forma corrida a lo largo de toda la carrera. Cada semestre agrupa seis.

| Semestre | UCA | Estado |
|---|---|---|
| [Primero](semestre_1/) | 01 - 06 | Concluido |
| [Segundo](semestre_2/) | 07 - 12 | Concluido |
| [Tercero](semestre_3/) | 13 - 18 | En curso |
| Cuarto a octavo | 19 - 51 | Pendiente |

### Tercer semestre

| UCA | Nombre |
|---|---|
| 13 | Derecho Internacional Publico |
| 14 | Historia Contemporanea de las Relaciones Internacionales |
| 15 | Pensamiento Politico y Social |
| 16 | Pensamiento Complejo para la Argumentacion |
| 17 | Teoria Economica |
| 18 | America del Norte |

### Estructura de carpetas

    index.html                   portada (generada)
    semestre_N/
      index.html                 indice del semestre (generado)
      NN_nombre_de_la_uca/
        index.html               indice de la UCA (generado)
        foroN.html / foroN_moodle.html
        tareaN.html  taN.html    tarea y tarea autentica
        integradora.html         actividad integradora
        *_Moctezuma_*.pdf        entregas en PDF, con el nombre que pidio el docente
    proyectos/
      ruptura_tribunal/          simulador de DIP, Historia y Pensamiento Politico
    assets/                      estilos y navegacion (data.js es la fuente unica del plan)
    herramientas/                generador de indices y verificador

Los semestres cuarto a octavo se agregan a `assets/js/data.js` cuando empiezan; no se crean carpetas vacias.

---

## Que encontraras aqui

Trabajos entregados y calificados: tareas, tareas autenticas, participaciones en foro y actividades integradoras, publicados en HTML para consulta abierta.

Este repositorio contiene **unicamente material terminado y de autoria propia**. Las lecturas, fuentes bibliograficas, apuntes de trabajo y borradores se mantienen fuera del repositorio.

---

## Como llega un trabajo aqui

1. El trabajo se prepara y se entrega fuera de este repositorio.
2. Solo entra aqui cuando ya fue entregado, y entra tal como se entrego: sin correcciones ni mejoras posteriores. Si algo quedo incompleto, se marca, no se rellena.
3. Las notas de margen (que abrio, con que conecta, que revisar) las escribe el autor al releer; no se generan.
4. Despues de agregar o migrar un trabajo se regeneran los indices y se verifica:

        python herramientas/generar_indices.py
        python herramientas/verificar_restaurante.py

El verificador rechaza material de terceros, PDF ajenos, paginas de relleno y enlaces rotos. GitHub Actions lo corre en cada push (`.github/workflows/verificar.yml`), junto con la comprobacion de que los indices estan al dia.

Las lecturas, contenidos de los cursos y materiales de terceros no se publican aqui, aunque se citen en los trabajos.

---

## Convenciones

- Nombres de archivo en minusculas, sin acentos ni espacios
- Un directorio por UCA, con la numeracion del plan de estudios
- Si un archivo no se va a publicar, no entra al repositorio

---

## Licencia

Los trabajos de autoria propia se publican bajo los terminos del archivo [LICENSE](LICENSE). El material de terceros citado en ellos pertenece a sus respectivos autores.
