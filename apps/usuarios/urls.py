from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html', next_page='libros:catalogo'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='usuarios:login'), name='logout'),
    path('registro/', views.RegistroUsuarioView.as_view(), name='registro'),
    
    # CRUD Usuarios
    path('lista/', views.UsuarioListView.as_view(), name='lista'),
    path('crear/', views.UsuarioCreateView.as_view(), name='crear'),
    path('editar/<int:pk>/', views.UsuarioUpdateView.as_view(), name='editar'),
    path('eliminar/<int:pk>/', views.UsuarioDeleteView.as_view(), name='eliminar'),
    path('suspender/<int:pk>/', views.suspender_usuario, name='suspender'),
]
