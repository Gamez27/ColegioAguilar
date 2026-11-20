from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    grado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Aspirante(models.Model):
    nombre   = models.CharField(max_length=100)
    email    = models.EmailField()
    telefono = models.CharField(max_length=20)
    carrera  = models.CharField(max_length=100)
    promedio = models.DecimalField(max_digits=4, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = 'Aspirante'
        verbose_name_plural = 'Aspirantes'

    def __str__(self):
        return f"{self.nombre} ({self.carrera})"

class MensajeContacto(models.Model):
    nombre  = models.CharField(max_length=100)
    email   = models.EmailField()
    asunto  = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"

class ConfiguracionSitio(models.Model):
    limite_inscripciones = models.PositiveIntegerField(
        default=5,
        verbose_name="Límite máximo de inscripciones"
    )
    email_notificaciones = models.EmailField(
        default="gamezur27@gmail.com",
        verbose_name="Correo para recibir alertas"
    )
    inscripciones_activas = models.BooleanField(
        default=True,
        verbose_name="Inscripciones activas"
    )
    limite_notificado = models.BooleanField(
        default=False,
        verbose_name="¿Notificación de límite enviada?"
    )

    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"

    def __str__(self):
        return f"Configuración: Límite {self.limite_inscripciones} cupos ({self.email_notificaciones})"

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj
