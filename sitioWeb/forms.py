import os
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Aspirante, MensajeContacto, Alumno, ConfiguracionSitio

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingresa tu usuario',
            'autocomplete': 'username',
            'autofocus': True,
        }),
        label='Usuario'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password',
        }),
        label='Contraseña'
    )


class ConsultaLoginForm(forms.Form):
    matricula = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej: 2243520111',
            'autocomplete': 'off',
            'autofocus': True,
        }),
        label='Matrícula de Aspirante'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingresa tu contraseña de consulta',
            'autocomplete': 'current-password',
        }),
        label='Contraseña'
    )


class AspiranteForm(forms.ModelForm):
    CARRERAS_CHOICES = [
        ('', 'Selecciona una carrera'),
        ('Ingenieria en Sistemas', 'Ingeniería en Sistemas'),
        ('Administracion', 'Administración de Empresas'),
        ('Derecho', 'Derecho'),
        ('Medicina', 'Medicina'),
        ('Arquitectura', 'Arquitectura'),
        ('Ingenieria Civil', 'Ingeniería Civil'),
        ('Ingenieria Industrial', 'Ingeniería Industrial'),
        ('Enfermeria', 'Enfermería'),
        ('Biologia', 'Biología'),
    ]

    MODALIDAD_CHOICES = [
        ('Presencial', 'Presencial (Escolarizada)'),
        ('Sabatina', 'Ejecutiva (Sabatina)'),
        ('En linea', 'En Línea'),
    ]

    TURNO_CHOICES = [
        ('Matutino', 'Turno Matutino'),
        ('Vespertino', 'Turno Vespertino'),
    ]

    GENERO_CHOICES = [
        ('', 'Selecciona tu género'),
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro'),
        ('Prefiero no decir', 'Prefiero no especificar'),
    ]

    PARENTESCO_CHOICES = [
        ('', 'Selecciona el parentesco'),
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Tutor Legal', 'Tutor(a) Legal'),
        ('Abuelo/a', 'Abuelo / Abuela'),
        ('Tio/a', 'Tío / Tía'),
        ('Hermano/a', 'Hermano(a) Mayor'),
        ('Otro', 'Otro familiar o tutor'),
    ]

    carrera = forms.ChoiceField(
        choices=CARRERAS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input', 'required': True})
    )
    modalidad = forms.ChoiceField(
        choices=MODALIDAD_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    turno = forms.ChoiceField(
        choices=TURNO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    genero = forms.ChoiceField(
        choices=GENERO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    tutor_parentesco = forms.ChoiceField(
        choices=PARENTESCO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Aspirante
        fields = [
            'nombre', 'curp', 'fecha_nacimiento', 'genero', 'email', 'telefono',
            'direccion', 'colonia', 'ciudad', 'estado', 'codigo_postal',
            'carrera', 'modalidad', 'turno', 'escuela_procedencia', 'promedio',
            'tutor_nombre', 'tutor_parentesco', 'tutor_telefono', 'tutor_email',
            'documento'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: Juan Pérez García',
                'required': True
            }),
            'curp': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: ABCD010203HDFRRN09',
                'maxlength': '18',
                'style': 'text-transform: uppercase;',
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: juan@ejemplo.com',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: 8341234567',
                'required': True
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Calle y número exterior / interior'
            }),
            'colonia': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Colonia o Fraccionamiento'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ciudad o Municipio'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Estado'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: 87000',
                'maxlength': '10'
            }),
            'escuela_procedencia': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: Preparatoria Federal / CBTIS 24'
            }),
            'promedio': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: 9.5',
                'step': '0.01',
                'min': '0',
                'max': '10',
                'required': True
            }),
            'tutor_nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nombre completo del padre, madre o tutor'
            }),
            'tutor_telefono': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: 8349876543'
            }),
            'tutor_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'tutor@ejemplo.com'
            }),
            'documento': forms.FileInput(attrs={
                'class': 'form-input file-input',
                'accept': '.pdf,.txt,.doc,.docx'
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        return nombre

    def clean_curp(self):
        curp = self.cleaned_data.get('curp', '')
        if curp:
            curp = curp.strip().upper()
            if len(curp) != 18:
                raise forms.ValidationError('La CURP debe tener exactamente 18 caracteres.')
        return curp

    def clean_promedio(self):
        promedio = self.cleaned_data.get('promedio')
        if promedio is not None:
            if promedio < 0 or promedio > 10:
                raise forms.ValidationError('El promedio debe estar en una escala de 0.00 a 10.00.')
        return promedio

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        digits = ''.join(c for c in telefono if c.isdigit())
        if len(digits) < 7:
            raise forms.ValidationError('Ingresa un teléfono válido (al menos 7 dígitos).')
        return telefono

    def clean_documento(self):
        doc = self.cleaned_data.get('documento')
        if doc:
            if doc.size > 15 * 1024 * 1024:
                raise forms.ValidationError('El archivo no debe exceder 15 MB.')
            ext = os.path.splitext(doc.name)[1].lower()
            if ext not in ['.pdf', '.txt', '.doc', '.docx']:
                raise forms.ValidationError('Por favor sube un archivo en formato PDF o TXT (.pdf, .txt).')
        return doc



class MensajeContactoForm(forms.ModelForm):
    ASUNTOS_CHOICES = [
        ('', 'Selecciona un asunto'),
        ('admisiones', 'Información de admisiones'),
        ('academico', 'Consulta académica'),
        ('becas', 'Becas y financiamiento'),
        ('otro', 'Otro'),
    ]

    asunto = forms.ChoiceField(
        choices=ASUNTOS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input', 'required': True})
    )

    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tu nombre completo',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'tu-correo@ejemplo.com',
                'required': True
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Escribe aquí tu consulta o comentario...',
                'required': True
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 2:
            raise forms.ValidationError('Por favor ingresa un nombre válido.')
        return nombre


class ConfiguracionSitioForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionSitio
        fields = ['limite_inscripciones', 'email_notificaciones', 'inscripciones_activas']
        widgets = {
            'limite_inscripciones': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '1',
                'max': '1000',
                'required': True,
            }),
            'email_notificaciones': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'correo@ejemplo.com',
                'required': True,
            }),
            'inscripciones_activas': forms.CheckboxInput(attrs={
                'style': 'width: 20px; height: 20px; cursor: pointer; accent-color: #220d2a;',
            }),
        }

    def clean_limite_inscripciones(self):
        limite = self.cleaned_data.get('limite_inscripciones')
        if limite is None or limite < 1:
            raise forms.ValidationError('El límite debe ser al menos de 1 persona.')
        return limite
