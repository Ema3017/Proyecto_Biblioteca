from django.db import models

class Libro(models.Model):
    # Filtros que coinciden con los grados de los usuarios
    GRADOS_DESTINO = (
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
        ('general', 'General (Todos)'),
    )

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    archivo_pdf = models.FileField(upload_to='libros_pdfs/') # Para subir el archivo digital
    portada = models.ImageField(upload_to='portadas/', blank=True, null=True)
    grado_objetivo = models.CharField(max_length=20, choices=GRADOS_DESTINO, default='general')
    ejemplares_disponibles = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.get_grado_objetivo_display()})"