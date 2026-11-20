from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Aspirante, MensajeContacto

class AdministracionCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'admin_test'
        self.password = 'SuperSecret123!'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='admin@test.com'
        )

        # Crear registros de prueba
        self.aspirante = Aspirante.objects.create(
            nombre='Carlos Mendoza',
            email='carlos@ejemplo.com',
            telefono='8349876543',
            carrera='Ingenieria en Sistemas',
            promedio=9.2
        )

        self.mensaje = MensajeContacto.objects.create(
            nombre='Maria Fernandez',
            email='maria@ejemplo.com',
            asunto='admisiones',
            mensaje='Hola, me gustaría saber las fechas de examen de admisión.'
        )

    def test_acceso_anonimo_redirige_a_login(self):
        """Verifica que un usuario no autenticado no pueda entrar al panel."""
        response = self.client.get(reverse('panel_admin'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('admin_login'), response.url)

    def test_login_exitoso(self):
        """Verifica que el login autentica y redirige al panel."""
        response = self.client.post(reverse('admin_login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('panel_admin'))

    def test_login_fallido(self):
        """Verifica que credenciales inválidas no den acceso."""
        response = self.client.post(reverse('admin_login'), {
            'username': self.username,
            'password': 'password_incorrecto',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña incorrectos')

    def test_panel_autenticado_muestra_datos(self):
        """Verifica que el panel cargue y muestre la información de la base de datos."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('panel_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carlos Mendoza')
        self.assertContains(response, 'Ingenieria en Sistemas')

    def test_crear_aspirante_se_refleja_en_bd(self):
        """CRUD Crear: Verifica creación de aspirante desde el panel administrativo."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('aspirante_crear'), {
            'nombre': 'Valeria Ramos',
            'email': 'valeria@ejemplo.com',
            'telefono': '8315551234',
            'carrera': 'Medicina',
            'promedio': '9.8',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Aspirante.objects.filter(email='valeria@ejemplo.com').exists())
        creado = Aspirante.objects.get(email='valeria@ejemplo.com')
        self.assertEqual(creado.nombre, 'Valeria Ramos')
        self.assertEqual(float(creado.promedio), 9.8)

    def test_editar_aspirante_se_refleja_en_bd(self):
        """CRUD Editar: Modifica un aspirante y verifica la actualización en la BD."""
        self.client.login(username=self.username, password=self.password)
        url_edit = reverse('aspirante_editar', kwargs={'id': self.aspirante.id})
        response = self.client.post(url_edit, {
            'nombre': 'Carlos Mendoza Actualizado',
            'email': 'carlos_nuevo@ejemplo.com',
            'telefono': '8341112233',
            'carrera': 'Derecho',
            'promedio': '9.5',
        })
        self.assertEqual(response.status_code, 302)
        self.aspirante.refresh_from_db()
        self.assertEqual(self.aspirante.nombre, 'Carlos Mendoza Actualizado')
        self.assertEqual(self.aspirante.email, 'carlos_nuevo@ejemplo.com')
        self.assertEqual(self.aspirante.carrera, 'Derecho')
        self.assertEqual(float(self.aspirante.promedio), 9.5)

    def test_eliminar_aspirante_se_refleja_en_bd(self):
        """CRUD Eliminar: Elimina un aspirante y verifica que se borre de la BD."""
        self.client.login(username=self.username, password=self.password)
        id_aspirante = self.aspirante.id
        url_del = reverse('aspirante_eliminar', kwargs={'id': id_aspirante})
        response = self.client.post(url_del)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Aspirante.objects.filter(id=id_aspirante).exists())

    def test_editar_comentario_se_refleja_en_bd(self):
        """CRUD Editar Mensaje: Modifica un comentario y verifica que se guarde en la BD."""
        self.client.login(username=self.username, password=self.password)
        url_edit = reverse('comentario_editar', kwargs={'id': self.mensaje.id})
        response = self.client.post(url_edit, {
            'nombre': 'Maria Fernandez Editada',
            'email': 'maria_edit@ejemplo.com',
            'asunto': 'becas',
            'mensaje': 'Mensaje editado sobre solicitud de beca.',
        })
        self.assertEqual(response.status_code, 302)
        self.mensaje.refresh_from_db()
        self.assertEqual(self.mensaje.nombre, 'Maria Fernandez Editada')
        self.assertEqual(self.mensaje.asunto, 'becas')

    def test_eliminar_comentario_se_refleja_en_bd(self):
        """CRUD Eliminar Mensaje: Elimina un comentario y verifica que se borre de la BD."""
        self.client.login(username=self.username, password=self.password)
        id_mensaje = self.mensaje.id
        url_del = reverse('comentario_eliminar', kwargs={'id': id_mensaje})
        response = self.client.post(url_del)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MensajeContacto.objects.filter(id=id_mensaje).exists())

    def test_exportar_csv(self):
        """Verifica que la exportación a CSV funcione y devuelva el archivo."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('aspirantes_exportar_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('Carlos Mendoza', response.content.decode('utf-8'))

    def test_logout(self):
        """Verifica el cierre de sesión."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('admin_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_login'))
