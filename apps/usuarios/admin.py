from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Biblioteca', {'fields': ('rol', 'grado_escolar')}),
    )
    list_display = ['username', 'email', 'rol', 'grado_escolar', 'is_staff']

admin.site.register(Usuario, CustomUserAdmin)