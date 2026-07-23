from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Libro
from .forms import LibroForm
from apps.prestamos.prolog.engine import engine

class BibliotecarioRequiredMixin(UserPassesTestMixin):
    """Mixin para restringir el acceso a vistas únicamente a bibliotecarios o superusuarios."""
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.rol == 'bibliotecario'

class DocenteOrBibliotecarioRequiredMixin(UserPassesTestMixin):
    """Mixin para restringir el acceso a vistas a bibliotecarios, superusuarios o docentes."""
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.rol in ['bibliotecario', 'docente']

class CatalogoView(LoginRequiredMixin, ListView):
    """
    Vista principal del catálogo de libros.
    Filtra los resultados según el rol y grado del usuario, y provee un buscador general.
    """
    model = Libro
    template_name = 'libros/catalogo.html'
    context_object_name = 'libros'

    def get_queryset(self):
        usuario = self.request.user
        
        # Si es superusuario o bibliotecario, ve todos los libros sin restricciones de grado
        if usuario.is_superuser or getattr(usuario, 'rol', None) == 'bibliotecario':
            queryset = Libro.objects.all()
        else:
            queryset = Libro.objects.all()
            # Filtro de seguridad por grado escolar (Estudiantes)
            if usuario.rol == 'estudiante':
                queryset = queryset.filter(Q(grado_objetivo=usuario.grado_escolar) | Q(grado_objetivo='general'))

            # Filtro por docente
            elif usuario.rol == 'docente' and usuario.grado_escolar != 'ninguno':
                queryset = queryset.filter(Q(grado_objetivo=usuario.grado_escolar) | Q(grado_objetivo='general'))

        # Búsqueda dinámica (RF07) - Aplica para todos los roles
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(titulo__icontains=q) |
                Q(autor__icontains=q) |
                Q(categoria__icontains=q)
            )

        return queryset

class LibroDetailView(LoginRequiredMixin, DetailView):
    """
    Vista de detalles de un libro específico.
    Se comunica con Prolog (IA) para calcular recomendaciones basadas en la categoría.
    """
    model = Libro
    template_name = 'libros/libro_detalle.html'
    context_object_name = 'libro'

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser or getattr(usuario, 'rol', None) == 'bibliotecario':
            return Libro.objects.all()
            
        queryset = Libro.objects.all()
        if usuario.rol == 'estudiante':
            queryset = queryset.filter(Q(grado_objetivo=usuario.grado_escolar) | Q(grado_objetivo='general'))
        elif usuario.rol == 'docente' and usuario.grado_escolar != 'ninguno':
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
        
        # Verificar si el usuario tiene permiso para leer/descargar el libro
        # Bibliotecarios y superusuarios siempre pueden.
        tiene_prestamo = False
        if usuario.is_superuser or usuario.rol == 'bibliotecario':
            tiene_prestamo = True
        else:
            from apps.prestamos.models import Prestamo
            tiene_prestamo = Prestamo.objects.filter(usuario=usuario, libro=libro_actual, estado='activo').exists()
            
        context['tiene_prestamo'] = tiene_prestamo

        return context

class LibroCreateView(LoginRequiredMixin, DocenteOrBibliotecarioRequiredMixin, CreateView):
    """Formulario para registrar un nuevo libro en el catálogo."""
    model = Libro
    form_class = LibroForm
    template_name = 'libros/libro_form.html'
    success_url = reverse_lazy('libros:catalogo')

class LibroUpdateView(LoginRequiredMixin, BibliotecarioRequiredMixin, UpdateView):
    """Formulario para actualizar los datos o archivos de un libro existente."""
    model = Libro
    form_class = LibroForm
    template_name = 'libros/libro_form.html'
    success_url = reverse_lazy('libros:catalogo')

class LibroDeleteView(LoginRequiredMixin, BibliotecarioRequiredMixin, DeleteView):
    """Pantalla de confirmación para eliminar definitivamente un libro del sistema."""
    model = Libro
    template_name = 'libros/libro_confirm_delete.html'
    success_url = reverse_lazy('libros:catalogo')
