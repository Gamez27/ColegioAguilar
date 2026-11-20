import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from django.urls import reverse

from .models import Aspirante, MensajeContacto, Alumno
from .forms import AdminLoginForm, AspiranteForm, MensajeContactoForm

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
    if request.method == 'POST':
        form = AspiranteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu inscripción fue registrada con éxito en el sistema!')
            return redirect('inscripcion')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    return render(request, 'sitioWeb/inscripcion.html')


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
    }
    return render(request, 'sitioWeb/admin/panel.html', context)


# ============================================================
#  CRUD: ASPIRANTES (INSCRIPCIONES)
# ============================================================

@login_required(login_url='admin_login')
def aspirante_crear(request):
    if request.method == 'POST':
        form = AspiranteForm(request.POST)
        if form.is_valid():
            aspirante = form.save()
            messages.success(request, f'Aspirante "{aspirante.nombre}" registrado exitosamente en la base de datos.')
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
        form = AspiranteForm(request.POST, instance=aspirante)
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
        messages.success(request, f'La inscripción de "{nombre}" fue eliminada de la base de datos.')
        return redirect('panel_admin')

    return render(request, 'sitioWeb/admin/confirmar_eliminar.html', {
        'tipo': 'Inscripción de Aspirante',
        'elemento': f'{aspirante.nombre} ({aspirante.carrera})',
        'cancelar_url': reverse('panel_admin'),
    })

@login_required(login_url='admin_login')
def aspirantes_exportar_csv(request):
    """Permite exportar todos los aspirantes registrados a un archivo CSV."""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="aspirantes_colegio_aguilas.csv"'
    
    # Agregar BOM para que Excel en español/Windows lo abra con los acentos perfectos
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Correo', 'Teléfono', 'Carrera', 'Promedio', 'Fecha de Registro'])

    for asp in Aspirante.objects.all().order_by('-fecha_registro'):
        writer.writerow([
            asp.id,
            asp.nombre,
            asp.email,
            asp.telefono,
            asp.carrera,
            asp.promedio,
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
