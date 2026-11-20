from django.contrib import admin
from .models import Alumno, Aspirante, MensajeContacto

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
