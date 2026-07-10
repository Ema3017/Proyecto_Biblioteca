from django.urls import path
from . import views

app_name = 'prestamos'

urlpatterns = [
    path('solicitar/<int:libro_id>/', views.solicitar_prestamo, name='solicitar'),
    path('mis-prestamos/', views.MisPrestamosView.as_view(), name='mis_prestamos'),
    path('gestion/', views.GestionPrestamosView.as_view(), name='gestion'),
    path('devolver/<int:prestamo_id>/', views.devolver_prestamo, name='devolver'),
]
