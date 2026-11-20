from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from .models import Aspirante, MensajeContacto, ConfiguracionSitio

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

    def test_limite_5_personas_envia_correo_y_bloquea_inscripciones(self):
        """
        Verifica que al registrar a la 5ta persona:
        1. Se envíe un correo de notificación a gamezur27@gmail.com
        2. El apartado de inscripciones se bloquee para personas adicionales
        3. Intentos posteriores de inscripción sean rechazados
        """
        config = ConfiguracionSitio.get_solo()
        config.limite_inscripciones = 5
        config.email_notificaciones = 'gamezur27@gmail.com'
        config.inscripciones_activas = True
        config.limite_notificado = False
        config.save()

        # Ya hay 1 en setUp (Carlos Mendoza). Creamos 3 más para tener 4
        for i in range(2, 5):
            Aspirante.objects.create(
                nombre=f'Aspirante {i}',
                email=f'aspirante{i}@ejemplo.com',
                telefono=f'834111222{i}',
                carrera='Medicina',
                promedio=9.0
            )

        self.assertEqual(Aspirante.objects.count(), 4)
        mail.outbox = []

        # El 5to aspirante se registra por la página pública
        response = self.client.post(reverse('inscripcion'), {
            'nombre': 'Quinto Aspirante',
            'email': 'quinto@ejemplo.com',
            'telefono': '8345559999',
            'carrera': 'Derecho',
            'promedio': '9.5',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Aspirante.objects.count(), 5)

        # 1. Verificar que se envió el correo a gamezur27@gmail.com
        self.assertEqual(len(mail.outbox), 1)
        email_enviado = mail.outbox[0]
        self.assertIn('gamezur27@gmail.com', email_enviado.to)
        self.assertIn('Límite de Inscripciones Alcanzado', email_enviado.subject)
        self.assertIn('5/5', email_enviado.subject)
        self.assertIn('Quinto Aspirante', email_enviado.body)

        # 2. Verificar que el flag de límite notificado está activo
        config.refresh_from_db()
        self.assertTrue(config.limite_notificado)

        # 3. Verificar que la página de inscripciones pública ahora muestra el bloqueo
        response_get = self.client.get(reverse('inscripcion'))
        self.assertEqual(response_get.status_code, 200)
        self.assertContains(response_get, 'Apartado de Inscripciones Bloqueado')
        self.assertContains(response_get, 'Inscripciones Cerradas')

        # 4. Verificar que un 6to aspirante es RECHAZADO y bloqueado
        response_sexto = self.client.post(reverse('inscripcion'), {
            'nombre': 'Sexto Aspirante',
            'email': 'sexto@ejemplo.com',
            'telefono': '8349991111',
            'carrera': 'Arquitectura',
            'promedio': '8.8',
        }, follow=True)

        self.assertEqual(response_sexto.status_code, 200)
        self.assertContains(response_sexto, 'El período de inscripciones se encuentra cerrado')
        self.assertEqual(Aspirante.objects.count(), 5)  # No aumentó a 6

    def test_admin_controla_limite_desde_panel(self):
        """
        Verifica que desde el panel de admin se pueda cambiar el límite de cupos,
        lo cual reabre las inscripciones y permite nuevos registros.
        """
        self.client.login(username=self.username, password=self.password)
        config = ConfiguracionSitio.get_solo()
        config.limite_inscripciones = 5
        config.save()

        # Llenar a 5 registros
        for i in range(2, 6):
            Aspirante.objects.create(
                nombre=f'Aspirante {i}',
                email=f'aspirante{i}@ejemplo.com',
                telefono=f'834111222{i}',
                carrera='Medicina',
                promedio=9.0
            )
        self.assertEqual(Aspirante.objects.count(), 5)

        # Modificar límite desde el admin a 8
        response_cfg = self.client.post(reverse('configuracion_actualizar'), {
            'limite_inscripciones': 8,
            'email_notificaciones': 'gamezur27@gmail.com',
            'inscripciones_activas': True,
        }, follow=True)

        self.assertEqual(response_cfg.status_code, 200)
        config.refresh_from_db()
        self.assertEqual(config.limite_inscripciones, 8)
        self.assertFalse(config.limite_notificado)

        # Ahora el 6to aspirante ya PUEDE registrarse porque el límite subió a 8
        self.client.logout()
        response_nuevo = self.client.post(reverse('inscripcion'), {
            'nombre': 'Sexto Aspirante',
            'email': 'sexto@ejemplo.com',
            'telefono': '8349991111',
            'carrera': 'Arquitectura',
            'promedio': '8.8',
        }, follow=True)

        self.assertEqual(response_nuevo.status_code, 200)
        self.assertEqual(Aspirante.objects.count(), 6)
        self.assertTrue(Aspirante.objects.filter(email='sexto@ejemplo.com').exists())

    def test_eliminar_aspirante_restablece_cupo(self):
        """
        Verifica que al eliminar un aspirante cuando se había alcanzado el límite,
        el cupo se libera y se pueden volver a recibir inscripciones.
        """
        config = ConfiguracionSitio.get_solo()
        config.limite_inscripciones = 2
        config.limite_notificado = True
        config.save()

        segundo = Aspirante.objects.create(
            nombre='Segundo Aspirante',
            email='segundo@ejemplo.com',
            telefono='8347778888',
            carrera='Derecho',
            promedio=8.5
        )
        self.assertEqual(Aspirante.objects.count(), 2)

        # El admin elimina al segundo aspirante
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse('aspirante_eliminar', kwargs={'id': segundo.id}))

        config.refresh_from_db()
        self.assertEqual(Aspirante.objects.count(), 1)
        self.assertFalse(config.limite_notificado)

        # Ahora se puede registrar uno nuevo
        self.client.logout()
        response = self.client.post(reverse('inscripcion'), {
            'nombre': 'Nuevo Reemplazo',
            'email': 'reemplazo@ejemplo.com',
            'telefono': '8346665555',
            'carrera': 'Medicina',
            'promedio': '9.1',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Aspirante.objects.count(), 2)

