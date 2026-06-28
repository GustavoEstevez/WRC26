from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Estadio, Cancha, Equipo, Partido, Reserva, Perfil
from datetime import datetime, timedelta
from django.utils import timezone


# ─── TESTS DE MODELOS ─────────────────────────────────────
class EstadioModelTest(TestCase):
    def setUp(self):
        self.estadio = Estadio.objects.create(
            nombre='Estadio Azteca',
            ciudad='Ciudad de México',
            pais='México',
            capacidad=87000
        )

    def test_estadio_creado(self):
        self.assertEqual(self.estadio.nombre, 'Estadio Azteca')
        self.assertEqual(self.estadio.capacidad, 87000)

    def test_estadio_str(self):
        self.assertEqual(str(self.estadio), 'Estadio Azteca - Ciudad de México')


class CanchaModelTest(TestCase):
    def setUp(self):
        self.estadio = Estadio.objects.create(
            nombre='Estadio Azteca',
            ciudad='Ciudad de México',
            pais='México',
            capacidad=87000
        )
        self.cancha = Cancha.objects.create(
            estadio=self.estadio,
            numero=1,
            tipo='principal',
            superficie='cesped_natural',
            estado='disponible',
            largo=105,
            ancho=68
        )

    def test_cancha_creada(self):
        self.assertEqual(self.cancha.numero, 1)
        self.assertEqual(self.cancha.estado, 'disponible')

    def test_cancha_str(self):
        self.assertEqual(str(self.cancha), 'Cancha 1 - Estadio Azteca')


class EquipoModelTest(TestCase):
    def setUp(self):
        self.equipo = Equipo.objects.create(
            nombre='Argentina',
            pais='Argentina',
            codigo_fifa='ARG',
            grupo='Grupo B',
            entrenador='Lionel Scaloni'
        )

    def test_equipo_creado(self):
        self.assertEqual(self.equipo.nombre, 'Argentina')
        self.assertEqual(self.equipo.codigo_fifa, 'ARG')

    def test_equipo_str(self):
        self.assertEqual(str(self.equipo), 'Argentina (ARG)')


# ─── TESTS DE VALIDACIONES ────────────────────────────────
class ReservaValidacionTest(TestCase):
    def setUp(self):
        self.estadio = Estadio.objects.create(
            nombre='Estadio Azteca',
            ciudad='Ciudad de México',
            pais='México',
            capacidad=87000
        )
        self.cancha = Cancha.objects.create(
            estadio=self.estadio,
            numero=1,
            tipo='principal',
            superficie='cesped_natural',
            estado='disponible',
            largo=105,
            ancho=68
        )
        self.equipo = Equipo.objects.create(
            nombre='Argentina',
            pais='Argentina',
            codigo_fifa='ARG',
            grupo='Grupo B',
            entrenador='Lionel Scaloni'
        )

    def test_reserva_en_pasado(self):
        from django.core.exceptions import ValidationError
        reserva = Reserva(
            cancha=self.cancha,
            equipo=self.equipo,
            fecha_inicio=timezone.now() - timedelta(hours=5),
            duracion_horas=2,
            estado='confirmada'
        )
        with self.assertRaises(ValidationError):
            reserva.clean()

    def test_reserva_conflicto_horario(self):
        from django.core.exceptions import ValidationError
        fecha = timezone.now() + timedelta(days=1)

        Reserva.objects.create(
            cancha=self.cancha,
            equipo=self.equipo,
            fecha_inicio=fecha,
            duracion_horas=2,
            estado='confirmada'
        )

        reserva2 = Reserva(
            cancha=self.cancha,
            equipo=self.equipo,
            fecha_inicio=fecha + timedelta(hours=1),
            duracion_horas=2,
            estado='confirmada'
        )
        with self.assertRaises(ValidationError):
            reserva2.clean()


# ─── TESTS DE VISTAS ──────────────────────────────────────
class VistasTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Crear usuario admin
        self.admin = User.objects.create_user(
            username='admin_test',
            password='admin1234'
        )
        Perfil.objects.create(usuario=self.admin, rol='admin')

        # Crear usuario operador
        self.operador = User.objects.create_user(
            username='operador_test',
            password='oper1234'
        )
        Perfil.objects.create(usuario=self.operador, rol='operador')

        # Datos de prueba
        self.estadio = Estadio.objects.create(
            nombre='Estadio Test',
            ciudad='Ciudad Test',
            pais='País Test',
            capacidad=50000
        )

    def test_inicio_requiere_login(self):
        response = self.client.get(reverse('inicio'))
        self.assertRedirects(response, '/login/?next=/')

    def test_inicio_con_login(self):
        self.client.login(username='admin_test', password='admin1234')
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)

    def test_lista_estadios(self):
        self.client.login(username='admin_test', password='admin1234')
        response = self.client.get(reverse('lista_estadios'))
        self.assertEqual(response.status_code, 200)

    def test_crear_estadio_como_admin(self):
        self.client.login(username='admin_test', password='admin1234')
        response = self.client.post(reverse('crear_estadio'), {
            'nombre': 'Nuevo Estadio',
            'ciudad': 'Nueva Ciudad',
            'pais': 'Nuevo País',
            'capacidad': 60000
        })
        self.assertEqual(Estadio.objects.count(), 2)

    def test_crear_estadio_como_operador_denegado(self):
        self.client.login(username='operador_test', password='oper1234')
        response = self.client.get(reverse('crear_estadio'))
        self.assertEqual(response.status_code, 403)

    def test_lista_equipos(self):
        self.client.login(username='admin_test', password='admin1234')
        response = self.client.get(reverse('lista_equipos'))
        self.assertEqual(response.status_code, 200)

    def test_mapa_estadios(self):
        self.client.login(username='admin_test', password='admin1234')
        response = self.client.get(reverse('mapa_estadios'))
        self.assertEqual(response.status_code, 200)