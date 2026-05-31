(function() {
    // Detectar si estamos en GitHub Pages o local
    var isGitHubPages = window.location.hostname === 'isaac179.github.io';
    var basePath = isGitHubPages ? '/UNRC/' : '/';
    
    // Si es local, usar rutas relativas normales
    if (!isGitHubPages && window.location.protocol === 'file:') {
        basePath = './';
    }
    
    const CONFIG = {
        semestres: [
            { numero: 1, nombre: "Semestre 1" },
            { numero: 2, nombre: "Semestre 2" },
            { numero: 3, nombre: "Semestre 3" },
            { numero: 4, nombre: "Semestre 4" },
            { numero: 5, nombre: "Semestre 5" },
            { numero: 6, nombre: "Semestre 6" },
            { numero: 7, nombre: "Semestre 7" },
            { numero: 8, nombre: "Semestre 8" }
        ]
    };

    function getRelativePath() {
        var path = window.location.pathname;
        // Si estamos en GitHub Pages, ajustar
        if (window.location.hostname === 'isaac179.github.io') {
            var cleanPath = path.replace('/UNRC/', '/');
            var depth = (cleanPath.match(/\//g) || []).length - 1;
            if (depth <= 1) return './';
            return '../'.repeat(depth - 1);
        }
        // Local
        var depth = (path.match(/\//g) || []).length - 1;
        if (depth <= 1) return './';
        return '../'.repeat(depth - 1);
    }

    function getFullUrl(semestre) {
        if (window.location.hostname === 'isaac179.github.io') {
            return '/UNRC/semestre_' + semestre + '/';
        }
        // Para archivo local
        var relPath = getRelativePath();
        return relPath + 'semestre_' + semestre + '/';
    }

    function getCurrentLocation() {
        var path = window.location.pathname;
        var cleanPath = path.replace('/UNRC/', '/');
        var matchSemestre = cleanPath.match(/semestre_(\d+)/);
        var matchMateria = cleanPath.match(/semestre_\d+\/(\d+_[^\/]+)/);
        return {
            semestre: matchSemestre ? matchSemestre[1] : null,
            materia: matchMateria ? matchMateria[1] : null,
            isRoot: cleanPath === '/' || cleanPath === '/index.html' || cleanPath === ''
        };
    }

    function generateBreadcrumb() {
        var location = getCurrentLocation();
        var relPath = getRelativePath();
        var baseUrl = (window.location.hostname === 'isaac179.github.io') ? '/UNRC/' : relPath;
        
        if (location.isRoot) return '';
        
        var html = '<div class="nav-breadcrumb"><a href="' + baseUrl + 'index.html">🏠 Inicio</a>';
        
        if (location.semestre) {
            html += '<span> / </span><a href="' + getFullUrl(location.semestre) + '">Semestre ' + location.semestre + '</a>';
        }
        
        if (location.materia) {
            var nombre = location.materia.replace(/^\d+_/, '').replace(/_/g, ' ');
            var materiaPath = (window.location.hostname === 'isaac179.github.io') 
                ? '/UNRC/semestre_' + location.semestre + '/' + location.materia + '/'
                : relPath + 'semestre_' + location.semestre + '/' + location.materia + '/';
            html += '<span> / </span><a href="' + materiaPath + '">' + nombre.charAt(0).toUpperCase() + nombre.slice(1) + '</a>';
        }
        
        html += '</div>';
        return html;
    }

    function generateNavHTML() {
        var relPath = getRelativePath();
        var location = getCurrentLocation();
        var baseUrl = (window.location.hostname === 'isaac179.github.io') ? '/UNRC/' : relPath;
        
        var semestresHtml = '';
        for (var i = 0; i < CONFIG.semestres.length; i++) {
            var sem = CONFIG.semestres[i];
            var activeClass = (location.semestre == sem.numero) ? 'active' : '';
            var semUrl = getFullUrl(sem.numero);
            semestresHtml += '<a href="' + semUrl + '" class="nav-link semestre ' + activeClass + '">📚 ' + sem.nombre + '</a>';
        }
        
        return '<div class="nav-persistente"><div class="nav-container"><div class="nav-bar"><button class="menu-toggle" id="navMenuToggle">☰</button><div class="nav-logo"><a href="' + baseUrl + 'index.html"><h2>🎓 Isaac Moctezuma</h2><p>Relaciones Internacionales · UNRC</p></a></div><div class="nav-links" id="navLinks">' + semestresHtml + '<a href="' + baseUrl + 'index.html#actividadesSection" class="nav-link">📝 Actividades</a><a href="' + baseUrl + 'index.html#perfilSection" class="nav-link">👤 Mi Perfil</a><a href="https://github.com/Isaac179/UNRC" target="_blank" class="nav-link">🐙 GitHub</a></div><div class="nav-user"><span>👨‍🎓</span><span>25228942-2</span></div></div></div>' + generateBreadcrumb() + '</div>';
    }

    function injectNavigation() {
        var existingNav = document.querySelector('.nav-persistente');
        if (existingNav) existingNav.remove();
        document.body.insertAdjacentHTML('afterbegin', generateNavHTML());
        
        var menuToggle = document.getElementById('navMenuToggle');
        var navLinks = document.getElementById('navLinks');
        if (menuToggle) {
            menuToggle.addEventListener('click', function() {
                navLinks.classList.toggle('show');
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectNavigation);
    } else {
        injectNavigation();
    }
})();
