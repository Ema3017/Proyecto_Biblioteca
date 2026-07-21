from django.urls import path
from . import views
from .views import procesar_mensaje_chat

app_name = 'prestamos'

urlpatterns = [
    path('solicitar/<int:libro_id>/', views.solicitar_prestamo, name='solicitar'),
    path('mis-prestamos/', views.MisPrestamosView.as_view(), name='mis_prestamos'),
    path('gestion/', views.GestionPrestamosView.as_view(), name='gestion_prestamos'),
    path('devolver/<int:prestamo_id>/', views.devolver_prestamo, name='devolver'),
    path('atraso/<int:prestamo_id>/', views.marcar_atraso, name='marcar_atraso'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('exportar/', views.exportar_excel_prestamos, name='exportar_excel'),
    path('api/chat/', procesar_mensaje_chat, name='procesar_mensaje_chat'),
]
