from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Aspirante, MensajeContacto, Alumno

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

    carrera = forms.ChoiceField(
        choices=CARRERAS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input', 'required': True})
    )

    class Meta:
        model = Aspirante
        fields = ['nombre', 'email', 'telefono', 'carrera', 'promedio']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: Juan Pérez García',
                'required': True
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
            'promedio': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: 9.5',
                'step': '0.01',
                'min': '0',
                'max': '10',
                'required': True
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        return nombre

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
