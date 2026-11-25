import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from django.urls import reverse

from .models import Aspirante, MensajeContacto, Alumno, ConfiguracionSitio
from .forms import AdminLoginForm, AspiranteForm, MensajeContactoForm, ConfiguracionSitioForm, ConsultaLoginForm
from .notifications import enviar_notificacion_limite

PASSWORD_CONSULTA_ASPIRANTE = 'cnsulta123'


# ============================================================
#  VISTAS PÚBLICAS
# ============================================================

def inicio(request):
    return render(request, 'sitioWeb/index.html')

def nosotros(request):
    return render(request, 'sitioWeb/nosotros.html')

def admisiones(request):
    return render(request, 'sitioWeb/admisiones.html')

def campus(request):
    return render(request, 'sitioWeb/campus.html')

def sistemas(request):
    return render(request, 'sitioWeb/sistemas.html')

def contacto(request):
    if request.method == 'POST':
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu mensaje fue enviado con éxito! Nos comunicaremos contigo a la brevedad.')
            return redirect('contacto')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    return render(request, 'sitioWeb/contacto.html')

def inscripcion(request):
    config = ConfiguracionSitio.get_solo()
    total_aspirantes = Aspirante.objects.count()
    limite = config.limite_inscripciones
    inscripciones_bloqueadas = (not config.inscripciones_activas) or (total_aspirantes >= limite)
    cupos_disponibles = max(0, limite - total_aspirantes)
    porcentaje_ocupado = min(100, int((total_aspirantes / limite) * 100)) if limite > 0 else 100

    if request.method == 'POST':
        if inscripciones_bloqueadas:
            messages.error(
                request,
                f'El período de inscripciones se encuentra cerrado. Se ha alcanzado el límite máximo de {limite} personas permitidas.'
            )
            return redirect('inscripcion')

        form = AspiranteForm(request.POST, request.FILES)
        if form.is_valid():
            aspirante = form.save()
            nuevo_total = Aspirante.objects.count()

            # Notificar al correo si se alcanzó el límite
            if nuevo_total >= config.limite_inscripciones and not config.limite_notificado:
                enviar_notificacion_limite(config, nuevo_total, aspirante)
                config.limite_notificado = True
                config.save(update_fields=['limite_notificado'])

            # Guardar matrícula generada en la sesión para la confirmación
            request.session['registro_exitoso_matricula'] = aspirante.matricula
            messages.success(request, f'¡Tu registro universitario fue exitoso! Tu matrícula asignada es {aspirante.matricula}.')
            return redirect('inscripcion_exito')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = AspiranteForm()

    return render(request, 'sitioWeb/inscripcion.html', {
        'form': form,
        'config': config,
        'total_aspirantes': total_aspirantes,
        'limite': limite,
        'inscripciones_bloqueadas': inscripciones_bloqueadas,
        'cupos_disponibles': cupos_disponibles,
        'porcentaje_ocupado': porcentaje_ocupado,
    })


def inscripcion_exito(request):
    """
    Pantalla de confirmación tras finalizar el registro de un nuevo aspirante.
    Muestra la matrícula generada y las instrucciones para acceder a su expediente.
    """
    matricula = request.session.get('registro_exitoso_matricula')
    aspirante = None
    if matricula:
        aspirante = Aspirante.objects.filter(matricula=matricula).first()

    if not aspirante:
        # Si no hay matrícula reciente en sesión, redirigir al formulario
        return redirect('inscripcion')

    return render(request, 'sitioWeb/inscripcion_exito.html', {
        'aspirante': aspirante,
        'matricula': aspirante.matricula,
        'password_consulta': PASSWORD_CONSULTA_ASPIRANTE,
    })


# ============================================================
#  PORTAL DE CONSULTA PARA ALUMNOS / ASPIRANTES
# ============================================================

def consulta_login(request):
    """
    Permite al alumno acceder a su información utilizando su matrícula
    y la contraseña fija 'cnsulta123' (o 'consulta123').
    """
    # Si ya tiene sesión activa de consulta, enviarlo directo a su expediente
    if request.session.get('aspirante_matricula'):
        return redirect('consulta_expediente')

    if request.method == 'POST':
        form = ConsultaLoginForm(request.POST)
        if form.is_valid():
            matricula_ingresada = form.cleaned_data['matricula'].strip()
            password_ingresado = form.cleaned_data['password'].strip()

            # Verificar contraseña solicitada
            if password_ingresado in [PASSWORD_CONSULTA_ASPIRANTE, 'consulta123']:
                aspirante = Aspirante.objects.filter(matricula=matricula_ingresada).first()
                if aspirante:
                    request.session['aspirante_matricula'] = aspirante.matricula
                    messages.success(request, f'Bienvenido, {aspirante.nombre}. Consulta tu información académica.')
                    return redirect('consulta_expediente')
                else:
                    messages.error(request, 'No se encontró ningún alumno con la matrícula proporcionada. Verifica tu número de matrícula.')
            else:
                messages.error(request, 'Contraseña incorrecta. Recuerda que la contraseña para consulta es cnsulta123.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = ConsultaLoginForm()

    return render(request, 'sitioWeb/consulta_login.html', {
        'form': form,
    })


def consulta_expediente(request):
    """
    Muestra el expediente completo del alumno consultante (datos personales,
    curp, tutor, datos académicos, matrícula y archivo adjunto).
    """
    matricula = request.session.get('aspirante_matricula')
    if not matricula:
        messages.warning(request, 'Debes iniciar sesión con tu matrícula y contraseña para consultar tu información.')
        return redirect('consulta_login')

    aspirante = get_object_or_404(Aspirante, matricula=matricula)

    return render(request, 'sitioWeb/consulta_expediente.html', {
        'aspirante': aspirante,
    })


def consulta_logout(request):
    """
    Cierra la sesión de consulta del alumno.
    """
    request.session.pop('aspirante_matricula', None)
    messages.info(request, 'Has cerrado la sesión de consulta correctamente.')
    return redirect('consulta_login')



# ============================================================
#  AUTENTICACIÓN ADMINISTRACIÓN (LOGIN / LOGOUT)
# ============================================================

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('panel_admin')

    next_url = request.GET.get('next') or request.POST.get('next') or 'panel_admin'

    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.first_name or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Verifica tus credenciales.')
    else:
        form = AdminLoginForm()

    return render(request, 'sitioWeb/admin/login.html', {
        'form': form,
        'next': next_url,
    })

def admin_logout(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('admin_login')


# ============================================================
#  PANEL DE ADMINISTRACIÓN (DASHBOARD & TABLAS CRUD)
# ============================================================

@login_required(login_url='admin_login')
def panel_admin(request):
    # Pestaña activa: 'aspirantes' o 'mensajes'
    tab = request.GET.get('tab', 'aspirantes')

    # Filtros y búsqueda para Aspirantes
    q_asp = request.GET.get('q_asp', '').strip()
    carrera_filtro = request.GET.get('carrera', '').strip()

    aspirantes_qs = Aspirante.objects.all()
    if q_asp:
        aspirantes_qs = aspirantes_qs.filter(
            Q(nombre__icontains=q_asp) |
            Q(matricula__icontains=q_asp) |
            Q(curp__icontains=q_asp) |
            Q(email__icontains=q_asp) |
            Q(telefono__icontains=q_asp) |
            Q(carrera__icontains=q_asp)
        )
    if carrera_filtro:
        aspirantes_qs = aspirantes_qs.filter(carrera=carrera_filtro)

    # Filtros y búsqueda para Mensajes/Comentarios
    q_msg = request.GET.get('q_msg', '').strip()
    asunto_filtro = request.GET.get('asunto', '').strip()

    mensajes_qs = MensajeContacto.objects.all()
    if q_msg:
        mensajes_qs = mensajes_qs.filter(
            Q(nombre__icontains=q_msg) |
            Q(email__icontains=q_msg) |
            Q(asunto__icontains=q_msg) |
            Q(mensaje__icontains=q_msg)
        )
    if asunto_filtro:
        mensajes_qs = mensajes_qs.filter(asunto=asunto_filtro)

    # Estadísticas para el resumen
    total_aspirantes = Aspirante.objects.count()
    total_mensajes = MensajeContacto.objects.count()
    promedio_dict = Aspirante.objects.aggregate(avg=Avg('promedio'))
    promedio_general = round(promedio_dict['avg'], 2) if promedio_dict['avg'] else 0.0

    carrera_top = (
        Aspirante.objects.values('carrera')
        .annotate(total=Count('carrera'))
        .order_by('-total')
        .first()
    )

    # Lista de carreras únicas para el selector de filtro
    carreras_disponibles = (
        Aspirante.objects.values_list('carrera', flat=True).distinct()
    )

    # Configuración de límites y cupos del sistema
    config = ConfiguracionSitio.get_solo()
    config_form = ConfiguracionSitioForm(instance=config)
    limite = config.limite_inscripciones
    inscripciones_bloqueadas = (not config.inscripciones_activas) or (total_aspirantes >= limite)
    cupos_disponibles = max(0, limite - total_aspirantes)
    porcentaje_ocupado = min(100, int((total_aspirantes / limite) * 100)) if limite > 0 else 100

    context = {
        'tab': tab,
        'aspirantes': aspirantes_qs,
        'mensajes': mensajes_qs,
        'q_asp': q_asp,
        'carrera_filtro': carrera_filtro,
        'q_msg': q_msg,
        'asunto_filtro': asunto_filtro,
        'total_aspirantes': total_aspirantes,
        'total_mensajes': total_mensajes,
        'promedio_general': promedio_general,
        'carrera_top': carrera_top['carrera'] if carrera_top else 'Ninguna',
        'carreras_disponibles': carreras_disponibles,
        'config': config,
        'config_form': config_form,
        'limite': limite,
        'inscripciones_bloqueadas': inscripciones_bloqueadas,
        'cupos_disponibles': cupos_disponibles,
        'porcentaje_ocupado': porcentaje_ocupado,
    }
    return render(request, 'sitioWeb/admin/panel.html', context)


# ============================================================
#  CRUD: ASPIRANTES (INSCRIPCIONES)
# ============================================================

@login_required(login_url='admin_login')
def aspirante_crear(request):
    config = ConfiguracionSitio.get_solo()
    if request.method == 'POST':
        form = AspiranteForm(request.POST, request.FILES)
        if form.is_valid():
            aspirante = form.save()
            nuevo_total = Aspirante.objects.count()
            if nuevo_total >= config.limite_inscripciones and not config.limite_notificado:
                enviar_notificacion_limite(config, nuevo_total, aspirante)
                config.limite_notificado = True
                config.save(update_fields=['limite_notificado'])

            messages.success(request, f'Aspirante "{aspirante.nombre}" con matrícula {aspirante.matricula} registrado exitosamente.')
            return redirect('panel_admin')
    else:
        form = AspiranteForm()

    return render(request, 'sitioWeb/admin/aspirante_form.html', {
        'form': form,
        'titulo': 'Nuevo Aspirante / Inscripción',
        'accion': 'Crear Aspirante',
    })

@login_required(login_url='admin_login')
def aspirante_editar(request, id):
    aspirante = get_object_or_404(Aspirante, id=id)
    if request.method == 'POST':
        form = AspiranteForm(request.POST, request.FILES, instance=aspirante)
        if form.is_valid():
            form.save()
            messages.success(request, f'Los datos de "{aspirante.nombre}" se actualizaron correctamente en la base de datos.')
            return redirect('panel_admin')
    else:
        form = AspiranteForm(instance=aspirante)

    return render(request, 'sitioWeb/admin/aspirante_form.html', {
        'form': form,
        'aspirante': aspirante,
        'titulo': f'Editar Inscripción: {aspirante.nombre}',
        'accion': 'Guardar Cambios',
    })

@login_required(login_url='admin_login')
def aspirante_eliminar(request, id):
    aspirante = get_object_or_404(Aspirante, id=id)
    if request.method == 'POST':
        nombre = aspirante.nombre
        aspirante.delete()

        # Si tras borrar queda por debajo del límite, restablecer límite_notificado para futuras alertas
        config = ConfiguracionSitio.get_solo()
        nuevo_total = Aspirante.objects.count()
        if nuevo_total < config.limite_inscripciones and config.limite_notificado:
            config.limite_notificado = False
            config.save(update_fields=['limite_notificado'])

        messages.success(request, f'La inscripción de "{nombre}" fue eliminada de la base de datos.')
        return redirect('panel_admin')

    return render(request, 'sitioWeb/admin/confirmar_eliminar.html', {
        'tipo': 'Inscripción de Aspirante',
        'elemento': f'{aspirante.nombre} ({aspirante.carrera})',
        'cancelar_url': reverse('panel_admin'),
    })

@login_required(login_url='admin_login')
def aspirantes_exportar_csv(request):
    """Permite exportar todos los aspirantes registrados a un archivo CSV completo."""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="aspirantes_colegio_aguilas.csv"'
    
    # Agregar BOM para que Excel en español/Windows lo abra con los acentos perfectos
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Matrícula', 'Nombre Completo', 'CURP', 'Fecha Nacimiento', 'Género',
        'Correo', 'Teléfono', 'Domicilio', 'Colonia', 'Ciudad', 'Estado', 'C.P.',
        'Carrera', 'Modalidad', 'Turno', 'Preparatoria Procedencia', 'Promedio',
        'Nombre Padre/Tutor', 'Parentesco', 'Teléfono Tutor', 'Correo Tutor',
        'Documento Adjunto', 'Estatus', 'Fecha de Registro'
    ])

    for asp in Aspirante.objects.all().order_by('-fecha_registro'):
        writer.writerow([
            asp.id,
            asp.matricula or '',
            asp.nombre,
            asp.curp or '',
            asp.fecha_nacimiento.strftime('%Y-%m-%d') if asp.fecha_nacimiento else '',
            asp.genero or '',
            asp.email,
            asp.telefono,
            asp.direccion or '',
            asp.colonia or '',
            asp.ciudad or '',
            asp.estado or '',
            asp.codigo_postal or '',
            asp.carrera,
            asp.modalidad or '',
            asp.turno or '',
            asp.escuela_procedencia or '',
            asp.promedio,
            asp.tutor_nombre or '',
            asp.tutor_parentesco or '',
            asp.tutor_telefono or '',
            asp.tutor_email or '',
            asp.documento.url if asp.documento else 'Sin archivo',
            asp.estatus or 'Registrado',
            asp.fecha_registro.strftime('%Y-%m-%d %H:%M') if asp.fecha_registro else '',
        ])

    return response



# ============================================================
#  CRUD: MENSAJES DE CONTACTO (COMENTARIOS)
# ============================================================

@login_required(login_url='admin_login')
def comentario_editar(request, id):
    mensaje = get_object_or_404(MensajeContacto, id=id)
    if request.method == 'POST':
        form = MensajeContactoForm(request.POST, instance=mensaje)
        if form.is_valid():
            form.save()
            messages.success(request, f'Mensaje de "{mensaje.nombre}" actualizado correctamente.')
            return redirect(f"{reverse('panel_admin')}?tab=mensajes")
    else:
        form = MensajeContactoForm(instance=mensaje)

    return render(request, 'sitioWeb/admin/comentario_form.html', {
        'form': form,
        'mensaje_obj': mensaje,
        'titulo': f'Editar Comentario / Mensaje #{mensaje.id}',
        'accion': 'Guardar Cambios',
    })

@login_required(login_url='admin_login')
def comentario_eliminar(request, id):
    mensaje = get_object_or_404(MensajeContacto, id=id)
    if request.method == 'POST':
        asunto = mensaje.asunto
        nombre = mensaje.nombre
        mensaje.delete()
        messages.success(request, f'El mensaje "{asunto}" de {nombre} fue eliminado de la base de datos.')
        return redirect(f"{reverse('panel_admin')}?tab=mensajes")

    return render(request, 'sitioWeb/admin/confirmar_eliminar.html', {
        'tipo': 'Mensaje de Contacto',
        'elemento': f'"{mensaje.asunto}" enviado por {mensaje.nombre}',
        'cancelar_url': f"{reverse('panel_admin')}?tab=mensajes",
    })


# ============================================================
#  CONFIGURACIÓN DE LÍMITES Y NOTIFICACIONES
# ============================================================

@login_required(login_url='admin_login')
def configuracion_actualizar(request):
    config = ConfiguracionSitio.get_solo()
    if request.method == 'POST':
        form = ConfiguracionSitioForm(request.POST, instance=config)
        if form.is_valid():
            nueva_cfg = form.save(commit=False)
            total_actual = Aspirante.objects.count()

            # Si el nuevo límite es superior al total de aspirantes registrados,
            # reactivamos el envío de notificación para cuando se alcance la nueva meta
            if nueva_cfg.limite_inscripciones > total_actual:
                nueva_cfg.limite_notificado = False

            nueva_cfg.save()
            messages.success(
                request,
                f'Configuración actualizada exitosamente. Límite: {nueva_cfg.limite_inscripciones} personas. Notificaciones enviadas a: {nueva_cfg.email_notificaciones}.'
            )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    return redirect(f"{reverse('panel_admin')}?tab=configuracion")


@login_required(login_url='admin_login')
def configuracion_probar_correo(request):
    if request.method == 'POST':
        config = ConfiguracionSitio.get_solo()
        total_aspirantes = Aspirante.objects.count()
        ultimo = Aspirante.objects.order_by('-fecha_registro').first()
        enviado = enviar_notificacion_limite(config, total_aspirantes, ultimo)
        if enviado:
            messages.success(
                request,
                f'¡Correo de prueba enviado con éxito a {config.email_notificaciones}! Revisa tu bandeja de entrada.'
            )
        else:
            messages.warning(
                request,
                f'El correo de prueba fue generado. Si tu servidor no tiene SMTP activo, se imprimió en la consola del servidor.'
            )
    return redirect(f"{reverse('panel_admin')}?tab=configuracion")
