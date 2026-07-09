from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Definimos los roles según el informe técnico
    ROLES = (
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
        ('bibliotecario', 'Bibliotecario'),
    )
    
    # Definimos los niveles escolares para los filtros del catálogo
    GRADOS = (
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
        ('ninguno', 'Ninguno / Personal'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    grado_escolar = models.CharField(max_length=20, choices=GRADOS, default='ninguno')

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"