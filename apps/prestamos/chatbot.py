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

        # Regla 4: Respuesta a solicitud de libro
        mensaje_limpio = mensaje.replace('ó','o').replace('á','a').replace('é','e').replace('í','i').replace('ú','u')
        if any(palabra in mensaje_limpio for palabra in ['si', 'quiero', 'solicitar', 'me interesa', 'el de']):
            libros = Libro.objects.all()
            for libro in libros:
                titulo_limpio = libro.titulo.lower().replace('ó','o').replace('á','a').replace('é','e').replace('í','i').replace('ú','u')
                if titulo_limpio in mensaje_limpio:
                    return f"¡Excelente elección! Para pedir '{libro.titulo}', por favor búscalo en el Catálogo y haz clic en el botón 'Solicitar Préstamo Directo'."
            
            # Si dice que sí pero no menciona el libro exacto
            if 'si' in mensaje_limpio.split() or 'quiero' in mensaje_limpio.split():
                 return "¡Genial! Por favor ve a la pestaña de 'Catálogo', busca el libro que te interesa y haz clic en 'Solicitar Préstamo Directo'."

        # Respuesta por defecto
        return "Lo siento, no entendí bien tu consulta. Puedes preguntarme por libros disponibles o tus préstamos."

    def _consultar_libros(self):
        libros = Libro.objects.filter(ejemplares_disponibles__gt=0)[:3]
        if libros.exists():
            nombres = ", ".join([f"'{l.titulo}' de {l.autor}" for l in libros])
            return f"¡Sí! Tenemos estos libros disponibles: {nombres}. ¿Deseas solicitar alguno?"
        return "Ahora mismo no hay libros disponibles en el catálogo."

    def _consultar_prestamos(self):
        if not self.usuario or not self.usuario.is_authenticated:
            return "Debes iniciar sesión para que pueda revisar tus préstamos personales."
        
        prestamos_activos = Prestamo.objects.filter(usuario=self.usuario, estado='activo')
        if prestamos_activos.exists():
            return f"Tienes {prestamos_activos.count()} préstamo(s) activo(s) en curso."
        return "No tienes préstamos activos en este momento."