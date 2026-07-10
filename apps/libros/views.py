from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Libro
from .forms import LibroForm
from apps.prestamos.prolog.engine import engine

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
        usuario = self.request.user
        queryset = Libro.objects.all()
        if usuario.rol == 'estudiante':
            queryset = queryset.filter(Q(grado_objetivo=usuario.grado_escolar) | Q(grado_objetivo='general'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro_actual = self.object
        usuario = self.request.user
        
        # Obtener recomendaciones cruzando con Prolog de forma simulada/directa
        # Prolog dice que es_recomendable si la categoría coincide y el grado también
        todos_los_libros = Libro.objects.exclude(id=libro_actual.id)
        recomendados = []
        for l in todos_los_libros:
            # Lógica extraída de la regla de inferencia:
            if l.categoria == libro_actual.categoria and (l.grado_objetivo == usuario.grado_escolar or l.grado_objetivo == 'general'):
                recomendados.append(l)
                if len(recomendados) >= 3:
                    break
        context['recomendados'] = recomendados
        return context

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
