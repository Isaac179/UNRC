// Datos de materias generados automáticamente

// Actividades estándar con sus versiones Moodle
const actividadesEstandar = [
    { modulo: 1, tipo: "foro", archivo: "foro1.html", nombre: "Foro Integrador", moodle: "foro1_moodle.html", emoji: "💬" },
    { modulo: 2, tipo: "tarea", archivo: "tarea2.html", nombre: "Tarea Auténtica", moodle: null, emoji: "📝" },
    { modulo: 2, tipo: "foro", archivo: "foro2.html", nombre: "Foro Integrador", moodle: "foro2_moodle.html", emoji: "💬" },
    { modulo: 3, tipo: "tarea", archivo: "tarea3.html", nombre: "Tarea Auténtica", moodle: null, emoji: "📝" },
    { modulo: 3, tipo: "foro", archivo: "foro3.html", nombre: "Foro Integrador", moodle: "foro3_moodle.html", emoji: "💬" },
    { modulo: 4, tipo: "tarea", archivo: "tarea4.html", nombre: "Tarea Auténtica", moodle: null, emoji: "📝" },
    { modulo: 4, tipo: "foro", archivo: "foro4.html", nombre: "Foro Integrador", moodle: "foro4_moodle.html", emoji: "💬" },
    { modulo: 5, tipo: "integradora", archivo: "integradora5.html", nombre: "Actividad Integradora", moodle: null, emoji: "🎯" }
];

function generarMenu() {
    const container = document.getElementById('menuBotones');
    if (!container) return;
    
    let html = '';
    
    for (let s = 1; s <= 8; s++) {
        const materias = materiasData[s];
        if (!materias || materias.length === 0) continue;
        
        html += `<div class="dropdown">
            <button class="dropbtn">📚 Semestre ${s}</button>
            <div class="dropdown-content">`;
        
        for (const materia of materias) {
            const path = `${materia.path}/`;
            
            html += `<div class="submenu">
                <a href="${path}index.html">📖 ${materia.nombre} <span style="font-size:0.7rem;">▶</span></a>
                <div class="submenu-content">`;
            
            // Agrupar actividades por módulo
            for (const act of actividadesEstandar) {
                // Enlace a la actividad principal
                html += `<a href="${path}${act.archivo}">
                    ${act.emoji} <span class="modulo-badge">${act.modulo}</span> ${act.nombre} M${act.modulo}
                </a>`;
                
                // Si tiene versión Moodle, agregar enlace secundario
                if (act.moodle) {
                    html += `<a href="${path}${act.moodle}" style="background: rgba(0,0,0,0.15); padding-left: 35px; font-size: 0.7rem;">
                        📱 <span class="modulo-badge">${act.modulo}</span> Versión Moodle (CSS inline)
                    </a>`;
                }
            }
            
            html += `</div></div>`;
        }
        
        html += `</div></div>`;
    }
    
    container.innerHTML = html;
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', generarMenu);
} else {
    generarMenu();
}
