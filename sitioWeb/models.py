import random
from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    grado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


def generar_matricula_aspirante():
    """
    Genera una matrícula universitaria única de 10 dígitos (ej: 2243520111).
    Utiliza el prefijo 224 seguido de 7 dígitos aleatorios únicos.
    """
    while True:
        sufijo = ''.join(str(random.randint(0, 9)) for _ in range(7))
        matricula_candidata = f"224{sufijo}"
        if not Aspirante.objects.filter(matricula=matricula_candidata).exists():
            return matricula_candidata


class Aspirante(models.Model):
    # Matrícula generada automáticamente al finalizar el registro
    matricula = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Matrícula")

    # Datos personales del alumno / aspirante
    nombre = models.CharField(max_length=120, verbose_name="Nombre completo")
    curp = models.CharField(max_length=18, blank=True, null=True, verbose_name="CURP")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    genero = models.CharField(max_length=30, blank=True, null=True, verbose_name="Género")
    email = models.EmailField(verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")

    # Domicilio
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Calle y número")
    colonia = models.CharField(max_length=100, blank=True, null=True, verbose_name="Colonia")
    ciudad = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ciudad / Municipio")
    estado = models.CharField(max_length=100, blank=True, null=True, verbose_name="Estado")
    codigo_postal = models.CharField(max_length=10, blank=True, null=True, verbose_name="Código Postal")

    # Datos académicos
    carrera = models.CharField(max_length=100, verbose_name="Carrera")
    modalidad = models.CharField(max_length=50, blank=True, null=True, default="Presencial", verbose_name="Modalidad")
    turno = models.CharField(max_length=50, blank=True, null=True, default="Matutino", verbose_name="Turno")
    escuela_procedencia = models.CharField(max_length=150, blank=True, null=True, verbose_name="Preparatoria de procedencia")
    promedio = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Promedio")

    # Datos del Padre, Madre o Tutor Legal
    tutor_nombre = models.CharField(max_length=120, blank=True, null=True, verbose_name="Nombre del padre o tutor")
    tutor_parentesco = models.CharField(max_length=50, blank=True, null=True, verbose_name="Parentesco con el alumno")
    tutor_telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono del tutor")
    tutor_email = models.EmailField(blank=True, null=True, verbose_name="Correo del tutor")

    # Documento de prueba adjunto (PDF, TXT, etc.)
    documento = models.FileField(upload_to="documentos_aspirantes/", blank=True, null=True, verbose_name="Documento adjunto")

    # Estatus del aspirante
    estatus = models.CharField(max_length=30, default="Registrado", verbose_name="Estatus")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = 'Aspirante'
        verbose_name_plural = 'Aspirantes'

    def save(self, *args, **kwargs):
        if not self.matricula:
            self.matricula = generar_matricula_aspirante()
        super().save(*args, **kwargs)

    def __str__(self):
        mat = f"[{self.matricula}] " if self.matricula else ""
        return f"{mat}{self.nombre} ({self.carrera})"


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
