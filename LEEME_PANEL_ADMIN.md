# 🦅 Colegio Águilar - Portal de Administración y CRUD

Este proyecto cuenta con un sistema completo y profesional de **Administración, Autenticación (Login/Logout) y CRUD** para la gestión de inscripciones (aspirantes) y mensajes/comentarios de contacto, integrado directamente con la base de datos SQLite y preparado para subirse a Internet.

---

## 🚀 Rutas Principales

| Ruta | Descripción | Acceso |
| :--- | :--- | :--- |
| `/` | Página de Inicio del Colegio Águilar | Público |
| `/inscripcion/` | Formulario de inscripción para aspirantes | Público / Modo Admin |
| `/contacto/` | Formulario de contacto y preguntas frecuentes | Público |
| `/admin-panel/login/` | **Pantalla de Inicio de Sesión de Administración** | Público |
| `/admin-panel/` | **Panel de Control Administrativo (Dashboard y CRUD)** | Requiere Login (`@login_required`) |
| `/admin-panel/aspirantes/nuevo/` | Formulario para registrar un aspirante manualmente | Requiere Login |
| `/admin-panel/aspirantes/<id>/editar/` | Formulario para editar datos del aspirante | Requiere Login |
| `/admin-panel/aspirantes/<id>/eliminar/` | Eliminación segura de un aspirante en la BD | Requiere Login |
| `/admin-panel/aspirantes/exportar-csv/` | Descarga de reporte de aspirantes en Excel/CSV | Requiere Login |
| `/admin-panel/configuracion/` | Actualizar límite de cupos y correo de alerta | Requiere Login |
| `/admin-panel/configuracion/probar-correo/` | Enviar correo de prueba para verificar notificaciones | Requiere Login |
| `/admin-panel/mensajes/<id>/editar/` | Edición de mensaje/comentario de contacto | Requiere Login |
| `/admin-panel/mensajes/<id>/eliminar/` | Eliminación de mensaje/comentario en la BD | Requiere Login |
| `/admin-panel/logout/` | Cierre de sesión seguro | Requiere Login |
| `/admin/` | Panel nativo de Django Admin | Superusuario |

---

## 🔐 Gestión de Usuarios Administradores

El usuario actual registrado en la base de datos es:
- **Usuario:** `gamez`

### ¿Cómo crear un nuevo administrador o cambiar la contraseña?

1. **Crear un nuevo superusuario/administrador:**
   ```bash
   python3 manage.py createsuperuser
   ```
   Te pedirá nombre de usuario, correo y contraseña.

2. **Cambiar la contraseña del usuario `gamez` (en caso de haberla olvidado):**
   ```bash
   python3 manage.py changepassword gamez
   ```

---

## 🛠️ Características Implementadas

### 1. Autenticación y Seguridad
- **Protección contra accesos no autorizados:** Todas las vistas administrativas están protegidas mediante el decorador `@login_required(login_url='admin_login')`. Si un usuario anónimo intenta acceder a `/admin-panel/`, es redirigido automáticamente a la pantalla de login.
- **Protección CSRF:** Todos los formularios de login, creación, edición y eliminación cuentan con `{% csrf_token %}`.
- **Eliminación segura:** Las eliminaciones requieren confirmación y método `POST`, evitando borrados accidentales o vulnerabilidades por prefetching de navegadores.
- **Validación de datos (`forms.py`):** Validación estricta de nombres, formato de correo, promedio escolar (0.00 a 10.00) y longitud de teléfono.

### 2. Panel de Administración y Dashboard
- **Métricas en tiempo real (KPIs):**
  - Total de Inscripciones recibidas.
  - Total de Comentarios y mensajes de contacto.
  - Promedio general calculado automáticamente de todos los aspirantes.
  - Carrera con mayor demanda.
- **Gestión de Inscripciones (CRUD Aspirantes):**
  - Buscador predictivo por nombre, correo o teléfono.
  - Filtro por carrera.
  - Badges de colores según el promedio académico (verde, amarillo, rojo).
  - Botón de edición con formulario validado.
  - Modal interactivo de confirmación de eliminación.
  - **Exportación a CSV:** Permite descargar la lista de aspirantes con compatibilidad total para Microsoft Excel.
- **Gestión de Comentarios y Contacto (CRUD Mensajes):**
  - Buscador por remitente o contenido del mensaje.
  - Filtro por tipo de asunto (admisiones, académico, becas, otro).
  - Modal de lectura rápida para ver el mensaje completo y botón para responder por email directamente con un clic (`mailto:`).
  - Edición y eliminación de comentarios.
- **Control de Cupos, Bloqueo Automático y Alertas por Correo:**
  - **Límite configurable:** Desde la pestaña *Control de Cupos y Límite* en el panel administrativo, el administrador puede definir cuántas personas pueden inscribirse (por defecto 5 cupos).
  - **Bloqueo Automático:** Al registrarse el aspirante que alcanza el cupo límite (por ejemplo, el 5to aspirante), el sistema bloquea inmediatamente la página `/inscripcion/`, impidiendo nuevos registros y mostrando una pantalla explicativa de "Convocatoria Cerrada / Límite Alcanzado" con botón hacia el formulario de contacto.
  - **Notificación por Correo Electrónico:** En el momento exacto en que se alcanza el límite, se despacha un correo HTML y texto plano a la dirección configurada (`gamezur27@gmail.com`) alertando que los cupos se han llenado, mostrando los datos del último aspirante registrado y proporcionando un botón para acceder al panel.
  - **Aumento o Reajuste Dinámico de Cupos:** Si el administrador aumenta el límite desde el panel (por ejemplo a 10 o 20) o elimina una inscripción para liberar un lugar, el sistema desbloquea automáticamente el formulario web público y reactiva las notificaciones para cuando se llene el nuevo límite.
  - **Envío de Correo de Prueba:** Botón integrado en el panel para probar en cualquier momento el despacho de alertas.

### 3. Integración en el Sitio Web
- En la barra de navegación superior (Navbar) de todas las páginas:
  - Si el usuario **no ha iniciado sesión**, aparece el botón elegante **"🔒 ACCESO"**.
  - Si el usuario **ha iniciado sesión**, aparece **"⚙️ PANEL"** y **"SALIR"**.
- En la página `/inscripcion/`:
  - Si un administrador entra a la página pública de inscripción, la tabla de aspirantes le muestra accesos directos para **Editar** y **Eliminar** aspirantes directamente en sitio.

---

## 🌐 Recomendaciones para Subir a Internet (Producción)

En `ColegioAguilar/settings.py` ya se dejaron las configuraciones preparadas:
1. **Variables de entorno:**
   - Puedes definir la variable `SECRET_KEY` y `DEBUG=False` en el panel de tu hosting (por ejemplo Render, PythonAnywhere, Railway, etc.).
2. **Archivos Estáticos:**
   - Se configuró `STATIC_ROOT = BASE_DIR / 'staticfiles'`.
   - Antes de iniciar en tu servidor en la nube, ejecuta:
     ```bash
     python3 manage.py collectstatic --noinput
     ```
3. **Migraciones:**
   - Asegúrate de ejecutar en el servidor:
     ```bash
     python3 manage.py migrate
     ```
