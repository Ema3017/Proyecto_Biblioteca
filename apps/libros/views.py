from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Libro
from .forms import LibroForm

class BibliotecarioRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.rol == 'bibliotecario'

class CatalogoView(LoginRequiredMixin, ListView):
    model = Libro
    template_name = 'libros/catalogo.html'
    context_object_name = 'libros'

    def get_queryset(self):
        usuario = self.request.user
        queryset = Libro.objects.all()

        # Filtro de seguridad por grado escolar (Estudiantes)
        if usuario.rol == 'estudiante':
            queryset = queryset.filter(Q(grado_objetivo=usuario.grado_escolar) | Q(grado_objetivo='general'))
        
        # Filtro por docente (Materia/Categoria). Si el docente tuviese un campo materia, lo cruzaríamos aquí.
        # Por ahora lo dejamos libre o filtrando por su grado asignado.
        elif usuario.rol == 'docente' and usuario.grado_escolar != 'ninguno':
            queryset = queryset.filter(Q(grado_objetivo=usuario.grado_escolar) | Q(grado_objetivo='general'))

        # Búsqueda dinámica (RF07)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(titulo__icontains=q) | 
                Q(autor__icontains=q) | 
                Q(categoria__icontains=q)
            )

        return queryset

class LibroDetailView(LoginRequiredMixin, DetailView):
    model = Libro
    template_name = 'libros/libro_detalle.html'
    context_object_name = 'libro'

    def get_queryset(self):
        # Re-aplicamos la misma lógica para que no puedan acceder a libros prohibidos por URL
        usuario = self.request.user
        queryset = Libro.objects.all()
        if usuario.rol == 'estudiante':
            queryset = queryset.filter(Q(grado_objetivo=usuario.grado_escolar) | Q(grado_objetivo='general'))
        return queryset

class LibroCreateView(LoginRequiredMixin, BibliotecarioRequiredMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/libro_form.html'
    success_url = reverse_lazy('libros:catalogo')

class LibroUpdateView(LoginRequiredMixin, BibliotecarioRequiredMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/libro_form.html'
    success_url = reverse_lazy('libros:catalogo')

class LibroDeleteView(LoginRequiredMixin, BibliotecarioRequiredMixin, DeleteView):
    model = Libro
    template_name = 'libros/libro_confirm_delete.html'
    success_url = reverse_lazy('libros:catalogo')
