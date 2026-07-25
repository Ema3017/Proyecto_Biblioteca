# =====================================================================
# Programación - forms.py
# Autoras: Coa Palo Jhadira Jazmín / Quispe Laura, Amarilis
# =====================================================================

from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'categoria', 'grado_objetivo', 'ejemplares_disponibles', 'archivo_pdf', 'portada']
