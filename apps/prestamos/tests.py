from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from apps.usuarios.models import Usuario
from apps.libros.models import Libro
from apps.prestamos.models import Prestamo

class PrestamoSeguridadTests(TestCase):
    def setUp(self):
        # Crear usuarios
        self.estudiante = Usuario.objects.create_user(
            username='estudiante1', 
            password='password123', 
            rol='estudiante', 
            email='estudiante@test.com'
        )
        self.bibliotecario = Usuario.objects.create_user(
            username='admin1', 
            password='password123', 
            rol='bibliotecario', 
            email='admin@test.com'
        )
        # Crear libro
        self.libro = Libro.objects.create(
            titulo='Test Libro',
            autor='Test Autor',
            categoria='Matematicas',
            grado_objetivo='secundaria',
            ejemplares_disponibles=2
        )
        # Crear préstamo
        self.prestamo = Prestamo.objects.create(
            usuario=self.estudiante,
            libro=self.libro,
            fecha_devolucion_esperada=timezone.now().date() + timedelta(days=7)
        )

    def test_estudiante_no_accede_dashboard(self):
        # Loguearse como estudiante
        self.client.login(username='estudiante1', password='password123')
        # Intentar acceder al dashboard
        response = self.client.get(reverse('prestamos:dashboard'))
        # Debería dar 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_estudiante_redirigido_en_exportar(self):
        self.client.login(username='estudiante1', password='password123')
        response = self.client.get(reverse('prestamos:exportar_excel'))
        # La vista exportar_excel_prestamos redirige a mis_prestamos si no es bibliotecario
        self.assertRedirects(response, reverse('prestamos:mis_prestamos'))

    def test_bibliotecario_accede_dashboard(self):
        self.client.login(username='admin1', password='password123')
        response = self.client.get(reverse('prestamos:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_bibliotecario_puede_exportar(self):
        self.client.login(username='admin1', password='password123')
        response = self.client.get(reverse('prestamos:exportar_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'], 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    def test_marcar_atraso_sancion(self):
        self.client.login(username='admin1', password='password123')
        response = self.client.post(reverse('prestamos:marcar_atraso', args=[self.prestamo.id]))
        # Refrescar de la DB
        self.prestamo.refresh_from_db()
        self.assertEqual(self.prestamo.estado, 'atrasado')
