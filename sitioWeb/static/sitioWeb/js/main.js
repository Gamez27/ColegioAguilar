// ============================================================
//  MENÚ HAMBURGUESA (aplica en todas las páginas)
// ============================================================
(function () {
    var btn = document.getElementById('navHamburguesa');
    var menu = document.getElementById('botonesNav');

    if (!btn || !menu) return;

    btn.addEventListener('click', function () {
        var abierto = menu.classList.toggle('abierto');
        btn.classList.toggle('abierto', abierto);
        btn.setAttribute('aria-expanded', abierto ? 'true' : 'false');
    });

    // Cerrar al hacer clic en cualquier enlace del menú
    var enlaces = menu.querySelectorAll('a');
    for (var i = 0; i < enlaces.length; i++) {
        enlaces[i].addEventListener('click', function () {
            menu.classList.remove('abierto');
            btn.classList.remove('abierto');
            btn.setAttribute('aria-expanded', 'false');
        });
    }

    // Cerrar al hacer clic fuera
    document.addEventListener('click', function (e) {
        if (!btn.contains(e.target) && !menu.contains(e.target)) {
            menu.classList.remove('abierto');
            btn.classList.remove('abierto');
            btn.setAttribute('aria-expanded', 'false');
        }
    });
})();

//  INSCRIPCION (Manejado por Django directamente)
// El procesamiento y guardado de datos en SQLite ahora lo maneja Django en el backend.


//  NOSOTROS 
var contadorAlumnos = document.getElementById('contadorAlumnos');

if (contadorAlumnos) {
    function animarContador(elementoId, valorFinal, duracion) {
        var elemento = document.getElementById(elementoId);
        var incremento = Math.ceil(valorFinal / (duracion / 30));
        var actual = 0;

        var intervalo = setInterval(function () {
            actual = actual + incremento;
            if (actual >= valorFinal) {
                actual = valorFinal;
                clearInterval(intervalo);
            }
            elemento.textContent = actual.toLocaleString();
        }, 30);
    }

    var contadoresIniciados = false;

    function verificarContadores() {
        var seccion = document.querySelector('.contador-seccion');
        var posicion = seccion.getBoundingClientRect();

        if (posicion.top < window.innerHeight && !contadoresIniciados) {
            contadoresIniciados = true;
            animarContador('contadorAlumnos', 5200, 2000);
            animarContador('contadorDocentes', 180, 2000);
            animarContador('contadorCarreras', 25, 2000);
            animarContador('contadorAnios', 30, 2000);
        }
    }

    window.addEventListener('scroll', verificarContadores);
    window.addEventListener('load', verificarContadores);

    var cards = document.querySelectorAll('.mv-card');
    for (var i = 0; i < cards.length; i++) {
        cards[i].addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-8px)';
        });
        cards[i].addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    }
}


//  ADMISIONES 
var carrerasGrid = document.getElementById('carrerasGrid');

if (carrerasGrid) {
    var carreras = [
        { nombre: 'Ingenieria en Sistemas', categoria: 'ingenieria', duracion: '9 semestres', descripcion: 'Desarrolla soluciones tecnologicas innovadoras para empresas y organizaciones.', enlace: '/sistemas/' },
        { nombre: 'Ingenieria Civil', categoria: 'ingenieria', duracion: '10 semestres', descripcion: 'Diseña y construye infraestructura que transforma ciudades y comunidades.' },
        { nombre: 'Ingenieria Industrial', categoria: 'ingenieria', duracion: '9 semestres', descripcion: 'Optimiza procesos productivos para mejorar la eficiencia empresarial.' },
        { nombre: 'Medicina General', categoria: 'ciencias', duracion: '12 semestres', descripcion: 'Forma profesionales de la salud comprometidos con el bienestar de la sociedad.' },
        { nombre: 'Enfermeria', categoria: 'ciencias', duracion: '8 semestres', descripcion: 'Brinda cuidados de salud de calidad con vocacion de servicio.' },
        { nombre: 'Biologia', categoria: 'ciencias', duracion: '8 semestres', descripcion: 'Estudia los seres vivos y su interaccion con el medio ambiente.' },
        { nombre: 'Derecho', categoria: 'humanidades', duracion: '10 semestres', descripcion: 'Forma abogados eticos comprometidos con la justicia y el estado de derecho.' },
        { nombre: 'Administracion de Empresas', categoria: 'humanidades', duracion: '8 semestres', descripcion: 'Lidera organizaciones con vision estrategica y habilidades gerenciales.' },
        { nombre: 'Arquitectura', categoria: 'ingenieria', duracion: '10 semestres', descripcion: 'Crea espacios funcionales y esteticos que mejoran la calidad de vida.' }
    ];

    var filtroActual = 'todas';

    function mostrarCarreras(listaCarreras) {
        var grid = document.getElementById('carrerasGrid');
        grid.innerHTML = '';

        if (listaCarreras.length === 0) {
            grid.innerHTML = '<p class="sin-resultados">No se encontraron carreras con ese criterio.</p>';
            return;
        }

        for (var i = 0; i < listaCarreras.length; i++) {
            var card = document.createElement('div');
            card.className = 'carrera-card';
            var enlaceHtml = listaCarreras[i].enlace ? '<a href="' + listaCarreras[i].enlace + '" class="btn-enviar" style="margin-top:10px; display:inline-block; padding:8px 20px; font-size: 0.85rem;">Ver Detalles</a>' : '';

            card.innerHTML =
                '<div class="carrera-categoria">' + listaCarreras[i].categoria.toUpperCase() + '</div>' +
                '<h3>' + listaCarreras[i].nombre + '</h3>' +
                '<p>' + listaCarreras[i].descripcion + '</p>' +
                '<div class="carrera-duracion">Duracion: ' + listaCarreras[i].duracion + '</div>' +
                enlaceHtml;
            grid.appendChild(card);
        }
    }

    function filtrarCarreras(categoria) {
        filtroActual = categoria;
        document.getElementById('buscadorCarreras').value = '';

        var botones = document.querySelectorAll('.filtro-btn');
        for (var i = 0; i < botones.length; i++) {
            botones[i].classList.remove('activo');
        }
        event.target.classList.add('activo');

        if (categoria === 'todas') {
            mostrarCarreras(carreras);
        } else {
            var filtradas = [];
            for (var i = 0; i < carreras.length; i++) {
                if (carreras[i].categoria === categoria) {
                    filtradas.push(carreras[i]);
                }
            }
            mostrarCarreras(filtradas);
        }
    }
    window.filtrarCarreras = filtrarCarreras;

    function buscarCarrera() {
        var texto = document.getElementById('buscadorCarreras').value.toLowerCase();
        var resultados = [];

        for (var i = 0; i < carreras.length; i++) {
            if (carreras[i].nombre.toLowerCase().indexOf(texto) !== -1) {
                resultados.push(carreras[i]);
            }
        }
        mostrarCarreras(resultados);
    }
    window.buscarCarrera = buscarCarrera;

    mostrarCarreras(carreras);
}


//  CAMPUS 
var galeriaGrid = document.getElementById('galeriaGrid');

if (galeriaGrid) {
    var instalaciones = [
        { nombre: 'Biblioteca Central', categoria: 'academico', descripcion: 'Mas de 50,000 volumenes y salas de estudio.' },
        { nombre: 'Laboratorio de Computo', categoria: 'academico', descripcion: 'Equipos de ultima generacion para practicas.' },
        { nombre: 'Auditorio Principal', categoria: 'academico', descripcion: 'Capacidad para 500 personas con equipo audiovisual.' },
        { nombre: 'Cancha de Futbol', categoria: 'deportivo', descripcion: 'Cancha profesional con pasto sintetico.' },
        { nombre: 'Gimnasio', categoria: 'deportivo', descripcion: 'Equipamiento completo para entrenamiento.' },
        { nombre: 'Alberca Olimpica', categoria: 'deportivo', descripcion: 'Alberca techada con carriles reglamentarios.' },
        { nombre: 'Cafeteria', categoria: 'servicios', descripcion: 'Alimentacion variada y saludable para la comunidad.' },
        { nombre: 'Centro Medico', categoria: 'servicios', descripcion: 'Atencion medica y de emergencia para estudiantes.' },
        { nombre: 'Estacionamiento', categoria: 'servicios', descripcion: 'Espacio amplio y vigilado las 24 horas.' }
    ];

    var horarios = [
        { servicio: 'Biblioteca', lv: '7:00 - 21:00', sab: '8:00 - 14:00', abierto: true },
        { servicio: 'Cafeteria', lv: '7:00 - 20:00', sab: '8:00 - 13:00', abierto: true },
        { servicio: 'Gimnasio', lv: '6:00 - 22:00', sab: '7:00 - 15:00', abierto: true },
        { servicio: 'Centro Medico', lv: '8:00 - 18:00', sab: '9:00 - 13:00', abierto: true },
        { servicio: 'Administracion', lv: '8:00 - 16:00', sab: 'Cerrado', abierto: false },
        { servicio: 'Laboratorios', lv: '7:00 - 20:00', sab: '8:00 - 14:00', abierto: true }
    ];

    var eventos = [
        { titulo: 'Feria de Ciencias', fecha: '15 Mayo 2026', descripcion: 'Presentacion de proyectos de investigacion estudiantil.' },
        { titulo: 'Torneo Deportivo', fecha: '22 Mayo 2026', descripcion: 'Competencias inter-facultades de futbol y basquetbol.' },
        { titulo: 'Conferencia de Tecnologia', fecha: '1 Junio 2026', descripcion: 'Ponentes internacionales sobre inteligencia artificial.' },
        { titulo: 'Semana Cultural', fecha: '10 Junio 2026', descripcion: 'Actividades artisticas, musica y exposiciones.' }
    ];

    function mostrarInstalaciones(lista) {
        var grid = document.getElementById('galeriaGrid');
        grid.innerHTML = '';

        for (var i = 0; i < lista.length; i++) {
            var card = document.createElement('div');
            card.className = 'instalacion-card';
            card.innerHTML =
                '<div class="instalacion-tipo">' + lista[i].categoria.toUpperCase() + '</div>' +
                '<h3>' + lista[i].nombre + '</h3>' +
                '<p>' + lista[i].descripcion + '</p>';
            grid.appendChild(card);
        }
    }

    function cambiarTab(categoria) {
        var botones = document.querySelectorAll('.tab-btn');
        for (var i = 0; i < botones.length; i++) {
            botones[i].classList.remove('activo');
        }
        event.target.classList.add('activo');

        if (categoria === 'todos') {
            mostrarInstalaciones(instalaciones);
        } else {
            var filtradas = [];
            for (var i = 0; i < instalaciones.length; i++) {
                if (instalaciones[i].categoria === categoria) {
                    filtradas.push(instalaciones[i]);
                }
            }
            mostrarInstalaciones(filtradas);
        }
    }
    window.cambiarTab = cambiarTab;

    function mostrarHorarios() {
        var tabla = document.getElementById('horarioTabla');
        tabla.innerHTML = '';

        for (var i = 0; i < horarios.length; i++) {
            var fila = document.createElement('tr');
            var estado = horarios[i].abierto ? '<span class="estado-abierto">Abierto</span>' : '<span class="estado-cerrado">Cerrado</span>';
            fila.innerHTML =
                '<td>' + horarios[i].servicio + '</td>' +
                '<td>' + horarios[i].lv + '</td>' +
                '<td>' + horarios[i].sab + '</td>' +
                '<td>' + estado + '</td>';
            tabla.appendChild(fila);
        }
    }

    function mostrarEventos() {
        var grid = document.getElementById('eventosGrid');
        grid.innerHTML = '';

        for (var i = 0; i < eventos.length; i++) {
            var card = document.createElement('div');
            card.className = 'evento-card';
            card.innerHTML =
                '<div class="evento-fecha">' + eventos[i].fecha + '</div>' +
                '<h3>' + eventos[i].titulo + '</h3>' +
                '<p>' + eventos[i].descripcion + '</p>';
            grid.appendChild(card);
        }
    }

    mostrarInstalaciones(instalaciones);
    mostrarHorarios();
    mostrarEventos();
}


//  CONTACTO 
var formContacto = document.getElementById('formContacto');

if (formContacto) {
    var mensajes = [];

    var preguntas = [
        { pregunta: '¿Cual es el costo de la inscripcion?', respuesta: 'El costo de inscripcion varia segun la carrera. Para mas informacion consulta la pagina de admisiones o contacta directamente a la oficina.', abierta: false },
        { pregunta: '¿Ofrecen becas?', respuesta: 'Si, contamos con programas de becas academicas, deportivas y de apoyo economico. Los requisitos incluyen mantener un promedio minimo de 8.5.', abierta: false },
        { pregunta: '¿Tienen modalidad en linea?', respuesta: 'Actualmente ofrecemos modalidad presencial y algunas materias en formato hibrido. Estamos trabajando para ampliar nuestra oferta en linea.', abierta: false },
        { pregunta: '¿Como puedo agendar una visita al campus?', respuesta: 'Puedes agendar una visita llamando al telefono (834) 123-4567 o enviando un correo a admisiones@colegioaguilas.edu.mx. Las visitas guiadas son de lunes a viernes.', abierta: false },
        { pregunta: '¿Cuales son las fechas de inscripcion?', respuesta: 'Las inscripciones para el semestre 2026-II estan abiertas desde mayo hasta julio. Te recomendamos iniciar tu proceso lo antes posible ya que los cupos son limitados.', abierta: false }
    ];

    function mostrarPreguntas() {
        var lista = document.getElementById('faqLista');
        lista.innerHTML = '';

        for (var i = 0; i < preguntas.length; i++) {
            var item = document.createElement('div');
            item.className = 'faq-item';
            if (preguntas[i].abierta) {
                item.classList.add('faq-abierta');
            }

            var preguntaDiv = document.createElement('div');
            preguntaDiv.className = 'faq-pregunta';
            preguntaDiv.setAttribute('data-indice', i);
            preguntaDiv.innerHTML = '<span>' + preguntas[i].pregunta + '</span><span class="faq-flecha">' + (preguntas[i].abierta ? '▲' : '▼') + '</span>';

            preguntaDiv.addEventListener('click', function () {
                var indice = parseInt(this.getAttribute('data-indice'));
                preguntas[indice].abierta = !preguntas[indice].abierta;
                mostrarPreguntas();
            });

            var respuestaDiv = document.createElement('div');
            respuestaDiv.className = 'faq-respuesta';
            respuestaDiv.style.display = preguntas[i].abierta ? 'block' : 'none';
            respuestaDiv.innerHTML = '<p>' + preguntas[i].respuesta + '</p>';

            item.appendChild(preguntaDiv);
            item.appendChild(respuestaDiv);
            lista.appendChild(item);
        }
    }

    // El envío del formulario de contacto ahora lo gestiona Django directamente hacia SQLite.

    mostrarPreguntas();
}


//  SISTEMAS COMPUTACIONALES 
var tabSistemas = document.getElementById('tabsSistemas');

if (tabSistemas) {
    var tabBotones = tabSistemas.querySelectorAll('.tab-btn');
    var paneles = document.querySelectorAll('.tab-panel');

    function cambiarTabSistemas(tabId) {
        // Ocultar todos los paneles
        for (var i = 0; i < paneles.length; i++) {
            paneles[i].style.display = 'none';
        }
        // Quitar clase activo de todos los botones
        for (var i = 0; i < tabBotones.length; i++) {
            tabBotones[i].classList.remove('activo');
        }
        // Mostrar panel seleccionado
        document.getElementById(tabId).style.display = 'block';
        event.target.classList.add('activo');
    }
    window.cambiarTabSistemas = cambiarTabSistemas;
}
