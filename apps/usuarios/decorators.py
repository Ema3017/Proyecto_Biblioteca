from django.core.exceptions import PermissionDenied
from functools import wraps

def requiere_rol(rol_requerido):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.rol == rol_requerido:
                return view_func(request, *args, **kwargs)
            elif request.user.is_superuser: # Superusers can do anything
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorador
