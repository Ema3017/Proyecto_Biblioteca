from django.db import models
from django.conf import settings
from apps.libros.models import Libro

class Prestamo(models.Model):
    """
    Representa una transacción de préstamo de un libro.
    Vincula a un Usuario con un Libro, registrando fechas críticas y el estado actual 
    (activo, devuelto, atrasado) para aplicar la lógica del negocio.
    """
    # Estados lógicos para el control de la biblioteca
    ESTADOS = (
        ('activo', 'Activo / En Curso'),
        ('devuelto', 'Devuelto'),
        ('atrasado', 'Atrasado / Con Multa'),
    )

    # Relaciones: Unimos el préstamo con el usuario de la UTP y con el libro
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    
    # Fechas de control
    fecha_prestamo = models.DateField(auto_now_add=True)  # Se pone la fecha de hoy automáticamente
    fecha_devolucion_esperada = models.DateField()       # Fecha límite para devolverlo
    fecha_devolucion_real = models.DateField(blank=True, null=True) # Se llena cuando entreguen el libro
    
    # Estado del préstamo
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')

    def __str__(self):
        return f"Préstamo de {self.libro.titulo} a {self.usuario.username} ({self.get_estado_display()})"