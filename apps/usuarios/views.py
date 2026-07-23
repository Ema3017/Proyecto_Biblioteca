from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm
from .decorators import requiere_rol

# Vista de Registro Público (Para Estudiantes/Docentes)
class RegistroUsuarioView(CreateView):
    """Vista pública para registrar un nuevo usuario en la biblioteca."""
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('libros:catalogo')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Loguear automáticamente al usuario recién registrado
        login(self.request, self.object)
        return response

# Mixin para verificar que es bibliotecario
class BibliotecarioRequiredMixin(UserPassesTestMixin):
    """Seguridad base para restringir módulos a bibliotecarios y admins."""
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.rol == 'bibliotecario'

class UsuarioListView(LoginRequiredMixin, BibliotecarioRequiredMixin, ListView):
    """Vista administrativa para listar y gestionar a todos los usuarios registrados."""
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'

class UsuarioCreateView(LoginRequiredMixin, BibliotecarioRequiredMixin, CreateView):
    """Vista administrativa para crear un nuevo usuario directamente desde el panel."""
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:lista')

class UsuarioUpdateView(LoginRequiredMixin, BibliotecarioRequiredMixin, UpdateView):
    """Vista para editar el perfil o rol de un usuario existente."""
    model = Usuario
    form_class = UsuarioChangeForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuarios:lista')

class UsuarioDeleteView(LoginRequiredMixin, BibliotecarioRequiredMixin, DeleteView):
    """Vista para confirmar y procesar la eliminación de un usuario del sistema."""
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuarios:lista')

@login_required
@requiere_rol('bibliotecario')
def suspender_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    # Evitar suspenderse a sí mismo
    if usuario != request.user:
        usuario.is_active = not usuario.is_active # Toggle: si está activo se suspende y viceversa
        usuario.save()
    return redirect('usuarios:lista')
