from django.contrib import admin
from .models import Alumno, Aspirante, MensajeContacto, ConfiguracionSitio

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'edad', 'grado')
    search_fields = ('nombre', 'grado')

@admin.register(Aspirante)
class AspiranteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'telefono', 'carrera', 'promedio', 'fecha_registro')
    list_filter = ('carrera', 'fecha_registro')
    search_fields = ('nombre', 'email', 'telefono', 'carrera')
    ordering = ('-fecha_registro',)

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'asunto', 'fecha')
    list_filter = ('asunto', 'fecha')
    search_fields = ('nombre', 'email', 'asunto', 'mensaje')
    ordering = ('-fecha',)

@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    list_display = ('id', 'limite_inscripciones', 'email_notificaciones', 'inscripciones_activas', 'limite_notificado')
    fieldsets = (
        ('Control de Cupos y Límite de Personas', {
            'fields': ('limite_inscripciones', 'inscripciones_activas'),
            'description': 'Define el límite de personas que pueden registrarse. Al alcanzarse, el apartado de inscripciones se bloqueará automáticamente.'
        }),
        ('Notificación de Alerta por Correo', {
            'fields': ('email_notificaciones', 'limite_notificado'),
            'description': 'Dirección de correo a la que se enviará la notificación cuando se alcance el límite.'
        }),
    )

    def has_add_permission(self, request):
        # Solo permitir 1 instancia global de configuración
        return not ConfiguracionSitio.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Evitar eliminar la configuración global
        return False

