from django.urls import path
from . import views

urlpatterns = [
    # Páginas Públicas
    path('', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('admisiones/', views.admisiones, name='admisiones'),
    path('campus/', views.campus, name='campus'),
    path('inscripcion/', views.inscripcion, name='inscripcion'),
    path('sistemas/', views.sistemas, name='sistemas'),

    # Autenticación de Administración
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),

    # Panel de Administración Principal
    path('admin-panel/', views.panel_admin, name='panel_admin'),

    # CRUD Inscripciones (Aspirantes)
    path('admin-panel/aspirantes/nuevo/', views.aspirante_crear, name='aspirante_crear'),
    path('admin-panel/aspirantes/<int:id>/editar/', views.aspirante_editar, name='aspirante_editar'),
    path('admin-panel/aspirantes/<int:id>/eliminar/', views.aspirante_eliminar, name='aspirante_eliminar'),
    path('admin-panel/aspirantes/exportar-csv/', views.aspirantes_exportar_csv, name='aspirantes_exportar_csv'),

    # CRUD Comentarios / Contacto (MensajeContacto)
    path('admin-panel/mensajes/<int:id>/editar/', views.comentario_editar, name='comentario_editar'),
    path('admin-panel/mensajes/<int:id>/eliminar/', views.comentario_eliminar, name='comentario_eliminar'),
]
