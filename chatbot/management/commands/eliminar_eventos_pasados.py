"""
Comando de Django para eliminar eventos cuya fecha de inicio ya haya pasado.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from chatbot.models import Evento


class Command(BaseCommand):
    help = 'Elimina eventos cuya fecha de inicio ya haya pasado'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué eventos se eliminarían sin eliminarlos realmente',
        )
        parser.add_argument(
            '--dias',
            type=int,
            default=0,
            help='Eliminar eventos pasados hace más de X días (por defecto 0, elimina todos los pasados)',
        )

    def handle(self, *args, **options):
        ahora = timezone.now()
        dry_run = options['dry_run']
        dias = options['dias']
        
        # Calcular la fecha límite
        if dias > 0:
            fecha_limite = ahora - timezone.timedelta(days=dias)
            eventos_pasados = Evento.objects.filter(fecha_inicio__lt=fecha_limite)
            mensaje_fecha = f"hace más de {dias} días"
        else:
            eventos_pasados = Evento.objects.filter(fecha_inicio__lt=ahora)
            mensaje_fecha = "ya pasaron"
        
        cantidad = eventos_pasados.count()
        
        if cantidad == 0:
            self.stdout.write(
                self.style.SUCCESS('No hay eventos pasados para eliminar.')
            )
            return
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'[DRY RUN] Se eliminarían {cantidad} evento(s) que {mensaje_fecha}:'
                )
            )
            for evento in eventos_pasados:
                self.stdout.write(
                    f'  - {evento.titulo} ({evento.fecha_inicio.strftime("%d/%m/%Y %H:%M")})'
                )
            self.stdout.write(
                self.style.WARNING(
                    '\nEjecuta sin --dry-run para eliminar realmente estos eventos.'
                )
            )
        else:
            # Mostrar los eventos que se van a eliminar
            self.stdout.write(
                self.style.WARNING(
                    f'Eliminando {cantidad} evento(s) que {mensaje_fecha}:'
                )
            )
            for evento in eventos_pasados:
                self.stdout.write(
                    f'  - {evento.titulo} ({evento.fecha_inicio.strftime("%d/%m/%Y %H:%M")})'
                )
            
            # Eliminar los eventos
            eventos_pasados.delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Se eliminaron {cantidad} evento(s) exitosamente.'
                )
            )

