from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.prestamos.models import Prestamo

class Command(BaseCommand):
    help = 'Bot diario que busca préstamos vencidos y actualiza su estado a Atrasado'

    def handle(self, *args, **options):
        hoy = timezone.now().date()
        
        # El bot busca préstamos activos que ya pasaron su fecha límite de devolución
        prestamos_vencidos = Prestamo.objects.filter(
            estado='activo',
            fecha_devolucion_esperada__lt=hoy
        )
        
        cantidad = prestamos_vencidos.count()
        
        if cantidad > 0:
            for prestamo in prestamos_vencidos:
                prestamo.estado = 'atrasado'
                prestamo.save()
            self.stdout.write(self.style.SUCCESS(f'[BOT] Éxito: Se detectaron y penalizaron {cantidad} préstamos vencidos.'))
        else:
            self.stdout.write(self.style.WARNING('[BOT] Control diario realizado: No hay préstamos vencidos el día de hoy.'))