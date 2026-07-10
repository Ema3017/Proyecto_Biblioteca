from django.urls import path
from . import views

app_name = 'libros'

urlpatterns = [
    path('catalogo/', views.CatalogoView.as_view(), name='catalogo'),
    path('detalle/<int:pk>/', views.LibroDetailView.as_view(), name='detalle'),
    
    # CRUD de libros para bibliotecario
    path('crear/', views.LibroCreateView.as_view(), name='crear'),
    path('editar/<int:pk>/', views.LibroUpdateView.as_view(), name='editar'),
    path('eliminar/<int:pk>/', views.LibroDeleteView.as_view(), name='eliminar'),
]
