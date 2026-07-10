import os
from django.conf import settings

# Intentar importar pyswip. Si falla, crearemos un "DummyEngine" para no romper Django en desarrollo
# si SWI-Prolog no está instalado en el sistema operativo del usuario.
try:
    from pyswip import Prolog
    PYSWIP_AVAILABLE = True
except Exception as e:
    print(f"Advertencia: PySwip no pudo cargarse ({e}). Usando motor simulado (Fallback).")
    PYSWIP_AVAILABLE = False

class PrologEngine:
    def __init__(self):
        self.prolog = None
        if PYSWIP_AVAILABLE:
            self.prolog = Prolog()
            # Cargar el archivo de reglas
            ruta_reglas = os.path.join(settings.BASE_DIR, 'apps', 'prestamos', 'prolog', 'reglas.pl')
            # En Windows a veces las barras causan problemas en Prolog, usamos forward slashes
            ruta_reglas = ruta_reglas.replace('\\', '/')
            try:
                self.prolog.consult(ruta_reglas)
            except Exception as e:
                print(f"Error consultando reglas.pl: {e}")
                self.prolog = None

    def puede_prestar(self, rol, libros_activos, sanciones):
        if self.prolog:
            # Query real a Prolog
            query = f"puede_prestar({rol}, {libros_activos}, {sanciones})"
            resultado = list(self.prolog.query(query))
            return len(resultado) > 0
        else:
            # Lógica de respaldo si pyswip no funciona en la PC
            maximos = {'estudiante': 3, 'docente': 5, 'bibliotecario': 10}
            return sanciones == 0 and libros_activos < maximos.get(rol, 0)

# Instancia global (Singleton) para evitar recargar el motor en cada petición
engine = PrologEngine()
