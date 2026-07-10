from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from .models import Prestamo
from apps.libros.models import Libro
from .prolog.engine import engine

class BibliotecarioRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.rol == 'bibliotecario'

@login_required
def solicitar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    usuario = request.user
    
    if libro.ejemplares_disponibles <= 0:
        messages.error(request, "No hay ejemplares disponibles de este libro.")
        return redirect('libros:detalle', pk=libro_id)

    # 1. Recopilar datos actuales del usuario para enviarlos a Prolog
    libros_activos = Prestamo.objects.filter(usuario=usuario, estado='activo').count()
    sanciones = Prestamo.objects.filter(usuario=usuario, estado='atrasado').count()
    
    # 2. Consultar al Motor Prolog (El Cerebro)
    if engine.puede_prestar(usuario.rol, libros_activos, sanciones):
        # Prolog Aprueba
        fecha_esperada = timezone.now().date() + timedelta(days=7) # 1 semana prestado
        
        # Crear Préstamo
        Prestamo.objects.create(
            usuario=usuario,
            libro=libro,
            fecha_devolucion_esperada=fecha_esperada
        )
        
        # Restar disponibilidad
        libro.ejemplares_disponibles -= 1
        libro.save()
        
        messages.success(request, f"¡Préstamo aprobado por el motor! Tienes hasta el {fecha_esperada} para devolverlo.")
    else:
        # Prolog Rechaza
        if sanciones > 0:
            messages.error(request, "Préstamo denegado por Inteligencia Artificial: Tienes libros con atraso o sanción.")
        else:
            messages.error(request, "Préstamo denegado por Inteligencia Artificial: Has alcanzado tu límite máximo de libros para tu rol.")

    return redirect('libros:detalle', pk=libro_id)

class MisPrestamosView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'prestamos/mis_prestamos.html'
    context_object_name = 'prestamos'
    
    def get_queryset(self):
        return Prestamo.objects.filter(usuario=self.request.user).order_by('-fecha_prestamo')

class GestionPrestamosView(LoginRequiredMixin, BibliotecarioRequiredMixin, ListView):
    model = Prestamo
    template_name = 'prestamos/gestion.html'
    context_object_name = 'prestamos'
    
    def get_queryset(self):
        return Prestamo.objects.all().order_by('-fecha_prestamo')

@login_required
def devolver_prestamo(request, prestamo_id):
    if not (request.user.rol == 'bibliotecario' or request.user.is_superuser):
        return redirect('prestamos:mis_prestamos')
        
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if prestamo.estado != 'devuelto':
        prestamo.estado = 'devuelto'
        prestamo.fecha_devolucion_real = timezone.now().date()
        prestamo.save()
        
        # Devolver ejemplar al catálogo
        prestamo.libro.ejemplares_disponibles += 1
        prestamo.libro.save()
        
        # Enviar correo de confirmación de devolución
        if prestamo.usuario.email:
            send_mail(
                subject='Devolución Exitosa - Biblioteca UTP',
                message=f'Hola {prestamo.usuario.username},\n\nHemos recibido correctamente tu devolución del libro "{prestamo.libro.titulo}".\n\n¡Gracias por cuidar el material!',
                from_email='biblioteca@utp.edu.pe',
                recipient_list=[prestamo.usuario.email],
                fail_silently=True,
            )
            
        messages.success(request, f"Libro {prestamo.libro.titulo} devuelto correctamente y notificación enviada.")
        
    return redirect('prestamos:gestion')

@login_required
def marcar_atraso(request, prestamo_id):
    if not (request.user.rol == 'bibliotecario' or request.user.is_superuser):
        return redirect('prestamos:mis_prestamos')
        
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if prestamo.estado == 'activo':
        prestamo.estado = 'atrasado'
        prestamo.save()
        
        # Enviar correo de sanción/advertencia
        if prestamo.usuario.email:
            send_mail(
                subject='[URGENTE] Préstamo Vencido y Sanción - Biblioteca UTP',
                message=f'Hola {prestamo.usuario.username},\n\nEl sistema registra que no has devuelto el libro "{prestamo.libro.titulo}" en la fecha límite.\n\nPor este motivo, tu cuenta ha sido SANCIONADA automáticamente. No podrás solicitar nuevos libros hasta que regularices tu situación.\n\nAcércate a la biblioteca lo antes posible.',
                from_email='biblioteca@utp.edu.pe',
                recipient_list=[prestamo.usuario.email],
                fail_silently=True,
            )
            
        messages.error(request, f"El préstamo de {prestamo.usuario.username} fue marcado como Atrasado. Sanción aplicada y notificada.")
        
    return redirect('prestamos:gestion')
