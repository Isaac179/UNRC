// ============================================
// SISTEMA DE NAVEGACIÓN PERSISTENTE
// ============================================

(function() {
    // Configuración
    const CONFIG = {
        // Datos de semestres y materias
        semestres: [
            { numero: 1, nombre: "Semestre 1", materias: [
                "01_introduccion_a_la_investigacion_en_ciencias_sociales",
                "02_escritura_argumentativa", 
                "03_introduccion_al_estudio_de_las_relaciones_internacionales",
                "04_perspectiva_de_genero_para_el_diseno_social",
                "05_historia_y_formacion_del_estado_mexicano_y_politica_exterior",
                "06_geografia_politica_y_economica"
            ]},
            { numero: 2, nombre: "Semestre 2", materias: [
                "07_derecho_constitucional_mexicano",
                "08_taller_de_expresion_escrita",
                "09_historia_y_formacion_del_estado_moderno_mexicano_y_politica_exterior",
                "10_desarrollo_sostenible_equidad_y_responsabilidad_social",
                "11_historia_de_las_relaciones_internacionales_1815-1945",
                "12_america_latina_y_el_caribe"
            ]},
            { numero: 3, nombre: "Semestre 3", materias: [
                "13_derecho_internacional_publico",
                "14_historia_contemporanea_de_las_relaciones_internacionales",
                "15_pensamiento_politico_y_social",
                "16_pensamiento_complejo_para_la_argumentacion",
                "17_teoria_economica",
                "18_america_del_norte"
            ]},
            { numero: 4, nombre: "Semestre 4", materias: [
                "19_derecho_internacional_privado",
                "20_organizacion_internacional",
                "21_teorias_de_las_relaciones_internacionales",
                "22_laboratorio_de_innovacion_social",
                "23_economia_politica_internacional",
                "24_europa"
            ]},
            { numero: 5, nombre: "Semestre 5", materias: [
                "25_negociaciones_internacionales",
                "26_diseno_y_evaluacion_de_politicas_publicas",
                "27_estudios_globales",
                "28_sistemas_politicos_comparados",
                "29_metodos_cuantitativos",
                "30_asia_y_el_pacifico"
            ]},
            { numero: 6, nombre: "Semestre 6", materias: [
                "31_derecho_internacional_de_los_derechos_humanos",
                "32_patrimonio_cultural",
                "33_introduccion_a_la_practica_profesional",
                "34_desarrollo_sustentable_y_medio_ambiente",
                "35_cooperacion_internacional",
                "36_comercio_internacional",
                "37_medio_oriente"
            ]},
            { numero: 7, nombre: "Semestre 7", materias: [
                "38_seminario_de_titulacion_i",
                "39_practica_profesional_i",
                "40_finanzas_internacionales",
                "41_gobernanza_global_ambiental",
                "42_africa",
                "48_procesos_de_conflicto_y_paz_en_el_siglo_xxi",
                "49_gobernanza_digital_en_las_ciencias_sociales"
            ]},
            { numero: 8, nombre: "Semestre 8", materias: [
                "43_seminario_de_titulacion_ii",
                "44_practica_profesional_ii",
                "45_migracion_internacional",
                "46_ciencia_tecnologia_e_innovacion_en_las_relaciones_internacionales",
                "47_retos_de_las_ciudades_globales",
                "50_dinamica_actual_de_la_politica_exterior_mexicana",
                "51_diplomacia_ambiental"
            ]}
        ],
        
        // Actividades base por módulo
        actividades: {
            modulo1: ["foro1.html"],
            modulo2: ["tarea2.html", "foro2.html"],
            modulo3: ["tarea3.html", "foro3.html"],
            modulo4: ["tarea4.html", "foro4.html"],
            modulo5: ["integradora5.html"]
        }
    };

    // Función para obtener la ruta relativa correcta
    function getRelativePath() {
        const path = window.location.pathname;
        const depth = (path.match(/\\//g) || []).length - 1;
        if (depth <= 1) return './';
        return '../'.repeat(depth - 1);
    }

    // Función para obtener el semestre y materia actual
    function getCurrentLocation() {
        const path = window.location.pathname;
        const matchSemestre = path.match(/semestre_(\\d+)/);
        const matchMateria = path.match(/semestre_\\d+\\/(\\d+_[^\\/]+)/);
        const matchActividad = path.match(/\\/(foro\\d|tarea\\d|integradora\\d)\\.html/);
        
        return {
            semestre: matchSemestre ? matchSemestre[1] : null,
            materia: matchMateria ? matchMateria[1] : null,
            actividad: matchActividad ? matchActividad[1] : null,
            isIndex: path.endsWith('index.html') || path.endsWith('/'),
            isRoot: path === '/' || path === '/index.html'
        };
    }

    // Generar breadcrumb
    function generateBreadcrumb() {
        const location = getCurrentLocation();
        const relPath = getRelativePath();
        
        if (location.isRoot) return '';
        
        let html = `<div class="nav-breadcrumb"><a href="${relPath}index.html">🏠 Inicio</a>`;
        
        if (location.semestre) {
            const semestreData = CONFIG.semestres.find(s => s.numero == location.semestre);
            html += `<span> / </span><a href="${relPath}semestre_${location.semestre}/">${semestreData?.nombre || 'Semestre ' + location.semestre}</a>`;
        }
        
        if (location.materia) {
            const materiaNombre = location.materia.replace(/^\\d+_/, '').replace(/_/g, ' ');
            html += `<span> / </span><a href="${relPath}semestre_${location.semestre}/${location.materia}/">${materiaNombre.charAt(0).toUpperCase() + materiaNombre.slice(1)}</a>`;
        }
        
        if (location.actividad) {
            let actividadNombre = '';
            if (location.actividad.includes('foro')) actividadNombre = `Foro ${location.actividad.match(/\\d+/)}`;
            else if (location.actividad.includes('tarea')) actividadNombre = `Tarea ${location.actividad.match(/\\d+/)}`;
            else if (location.actividad.includes('integradora')) actividadNombre = `Actividad Integradora`;
            html += `<span> / </span><span>📝 ${actividadNombre}</span>`;
        }
        
        html += `</div>`;
        return html;
    }

    // Generar el menú HTML
    function generateNavHTML() {
        const relPath = getRelativePath();
        const location = getCurrentLocation();
        
        let semestresHtml = '';
        CONFIG.semestres.forEach(sem => {
            const activeClass = location.semestre == sem.numero ? 'active' : '';
            semestresHtml += `<a href="${relPath}semestre_${sem.numero}/" class="nav-link semestre ${activeClass}" data-semestre="${sem.numero}">📚 ${sem.nombre}</a>`;
        });
        
        return `
            <div class="nav-persistente">
                <div class="nav-container">
                    <div class="nav-bar">
                        <button class="menu-toggle" id="navMenuToggle">☰</button>
                        <div class="nav-logo">
                            <a href="${relPath}index.html" style="text-decoration:none;">
                                <h2>🎓 Isaac Moctezuma</h2>
                                <p>Relaciones Internacionales · UNRC</p>
                            </a>
                        </div>
                        <div class="nav-links" id="navLinks">
                            ${semestresHtml}
                            <a href="${relPath}index.html#actividadesSection" class="nav-link">📝 Actividades</a>
                            <a href="${relPath}index.html#perfilSection" class="nav-link">👤 Mi Perfil</a>
                            <a href="https://github.com/Isaac179/UNRC" target="_blank" class="nav-link">🐙 GitHub</a>
                        </div>
                        <div class="nav-user">
                            <span>👨‍🎓</span>
                            <span>25228942-2</span>
                        </div>
                    </div>
                </div>
                ${generateBreadcrumb()}
            </div>
        `;
    }

    // Inyectar navegación
    function injectNavigation() {
        const navHTML = generateNavHTML();
        
        // Si ya existe, reemplazar
        const existingNav = document.querySelector('.nav-persistente');
        if (existingNav) {
            existingNav.remove();
        }
        
        // Insertar al inicio del body
        document.body.insertAdjacentHTML('afterbegin', navHTML);
        
        // Configurar menú responsive
        const menuToggle = document.getElementById('navMenuToggle');
        const navLinks = document.getElementById('navLinks');
        if (menuToggle) {
            menuToggle.addEventListener('click', () => {
                navLinks.classList.toggle('show');
            });
        }
        
        // Cerrar menú al hacer clic en un enlace (móvil)
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    navLinks.classList.remove('show');
                }
            });
        });
    }

    // Mostrar indicador de carga
    function showLoading() {
        let loader = document.querySelector('.nav-loading');
        if (!loader) {
            loader = document.createElement('div');
            loader.className = 'nav-loading';
            document.body.appendChild(loader);
        }
    }

    function hideLoading() {
        const loader = document.querySelector('.nav-loading');
        if (loader) loader.remove();
    }

    // Inicializar
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            showLoading();
            injectNavigation();
            hideLoading();
        });
    } else {
        showLoading();
        injectNavigation();
        hideLoading();
    }
})();
