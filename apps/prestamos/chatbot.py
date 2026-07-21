from .models import Libro, Prestamo

class BibliotecaChatbot:
    def __init__(self, usuario=None):
        self.usuario = usuario

    def responder(self, mensaje_texto):
        mensaje = mensaje_texto.lower()

        # Regla 1: Disponibilidad de libros
        if any(palabra in mensaje for palabra in ['libro', 'disponible', 'tienen', 'buscar']):
            return self._consultar_libros()

        # Regla 2: Préstamos del usuario
        elif any(palabra in mensaje for palabra in ['prestamo', 'mis libros', 'multa', 'sanción']):
            return self._consultar_prestamos()

        # Regla 3: Saludos
        elif any(palabra in mensaje for palabra in ['hola', 'buenos días', 'buenas tardes', 'hey']):
            return "¡Hola! Soy el asistente virtual de la biblioteca UTP. ¿En qué te puedo ayudar hoy?"

        # Respuesta por defecto
        return "Lo siento, no entendí bien tu consulta. Puedes preguntarme por libros disponibles o tus préstamos."

    def _consultar_libros(self):
        libros = Libro.objects.filter(estado__iexact='Disponible')[:3]
        if libros.exists():
            nombres = ", ".join([f"'{l.titulo}' de {l.autor}" for l in libros])
            return f"¡Sí! Tenemos estos libros disponibles: {nombres}. ¿Deseas solicitar alguno?"
        return "Ahora mismo no hay libros disponibles en el catálogo."

    def _consultar_prestamos(self):
        if not self.usuario or not self.usuario.is_authenticated:
            return "Debes iniciar sesión para que pueda revisar tus préstamos personales."
        
        prestamos_activos = Prestamo.objects.filter(usuario=self.usuario, estado='Activo')
        if prestamos_activos.exists():
            return f"Tienes {prestamos_activos.count()} préstamo(s) activo(s) en curso."
        return "No tienes préstamos activos en este momento."