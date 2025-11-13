"""
Comando de Django para poblar la base de datos con eventos de prueba.
Uso: python manage.py poblar_eventos
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from chatbot.models import Evento
from decimal import Decimal


class Command(BaseCommand):
    help = 'Pobla la base de datos con eventos de prueba para la ciudad de Loja'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando eventos de prueba...'))
        
        hoy = timezone.now()
        
        eventos_data = [
            # Eventos de hoy
            {
                'titulo': 'Festival de Música Andina',
                'descripcion': 'Gran festival de música andina con artistas locales e internacionales. Ven a disfrutar de los mejores sonidos de los Andes.',
                'categoria': 'musica',
                'fecha_inicio': hoy.replace(hour=18, minute=0, second=0, microsecond=0),
                'fecha_fin': hoy.replace(hour=23, minute=0, second=0, microsecond=0),
                'ubicacion': 'Parque Central de Loja',
                'direccion': 'Parque Central, Centro Histórico, Loja',
                'precio': Decimal('15.00'),
                'contacto': '0987654321',
            },
            {
                'titulo': 'Clase de Yoga Gratuita',
                'descripcion': 'Clase de yoga al aire libre para todos los niveles. Trae tu mat y disfruta de una sesión relajante.',
                'categoria': 'deporte',
                'fecha_inicio': hoy.replace(hour=7, minute=0, second=0, microsecond=0),
                'fecha_fin': hoy.replace(hour=8, minute=30, second=0, microsecond=0),
                'ubicacion': 'Parque Jipiro',
                'direccion': 'Parque Jipiro, Loja',
                'precio': Decimal('0.00'),
                'contacto': 'yoga.loja@email.com',
            },
            
            # Eventos de mañana
            {
                'titulo': 'Feria Artesanal del Valle',
                'descripcion': 'Feria con productos artesanales, comida típica y música en vivo. Apoya a los artesanos locales.',
                'categoria': 'feria',
                'fecha_inicio': (hoy + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=1)).replace(hour=20, minute=0, second=0, microsecond=0),
                'ubicacion': 'Plaza de San Sebastián',
                'direccion': 'Plaza de San Sebastián, Centro Histórico, Loja',
                'precio': Decimal('0.00'),
                'contacto': 'feria.artesanal@loja.gob.ec',
            },
            {
                'titulo': 'Concierto de Rock Nacional',
                'descripcion': 'Los mejores grupos de rock nacional se presentan en Loja. No te pierdas esta noche llena de energía.',
                'categoria': 'musica',
                'fecha_inicio': (hoy + timedelta(days=1)).replace(hour=20, minute=0, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0),
                'ubicacion': 'Coliseo Ciudad de Loja',
                'direccion': 'Av. Universitaria, Loja',
                'precio': Decimal('25.00'),
                'contacto': 'ventas@coliseoloja.com',
            },
            
            # Eventos de esta semana
            {
                'titulo': 'Obra de Teatro: "El Quijote"',
                'descripcion': 'Adaptación moderna de la obra clásica de Cervantes. Presentación del grupo teatral local.',
                'categoria': 'teatro',
                'fecha_inicio': (hoy + timedelta(days=2)).replace(hour=19, minute=30, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=2)).replace(hour=21, minute=30, second=0, microsecond=0),
                'ubicacion': 'Teatro Bolívar',
                'direccion': 'Calle Bolívar, Centro Histórico, Loja',
                'precio': Decimal('10.00'),
                'contacto': 'teatro.bolivar@loja.gob.ec',
            },
            {
                'titulo': 'Taller de Cocina Ecuatoriana',
                'descripcion': 'Aprende a preparar los platos típicos de Loja. Incluye degustación de todos los platos preparados.',
                'categoria': 'gastronomia',
                'fecha_inicio': (hoy + timedelta(days=3)).replace(hour=15, minute=0, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=3)).replace(hour=18, minute=0, second=0, microsecond=0),
                'ubicacion': 'Centro Culinario Loja',
                'direccion': 'Av. 24 de Mayo, Loja',
                'precio': Decimal('30.00'),
                'contacto': 'cocina.loja@email.com',
            },
            {
                'titulo': 'Maratón de Loja 2024',
                'descripcion': 'Maratón anual de la ciudad. Categorías: 5K, 10K y 21K. Inscripciones abiertas.',
                'categoria': 'deporte',
                'fecha_inicio': (hoy + timedelta(days=4)).replace(hour=6, minute=0, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=4)).replace(hour=12, minute=0, second=0, microsecond=0),
                'ubicacion': 'Parque Lineal',
                'direccion': 'Parque Lineal, Loja',
                'precio': Decimal('20.00'),
                'contacto': 'maraton.loja@deportes.gob.ec',
            },
            
            # Eventos culturales
            {
                'titulo': 'Exposición de Arte Contemporáneo',
                'descripcion': 'Exposición de artistas locales e internacionales. Obras de pintura, escultura y fotografía.',
                'categoria': 'cultural',
                'fecha_inicio': (hoy + timedelta(days=5)).replace(hour=10, minute=0, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=12)).replace(hour=18, minute=0, second=0, microsecond=0),
                'ubicacion': 'Museo de Arte de Loja',
                'direccion': 'Calle Bernardo Valdivieso, Loja',
                'precio': Decimal('5.00'),
                'contacto': 'museo.arte@loja.gob.ec',
            },
            {
                'titulo': 'Festival de Danza Folclórica',
                'descripcion': 'Grupos de danza de toda la región se reúnen para celebrar la cultura lojana.',
                'categoria': 'danza',
                'fecha_inicio': (hoy + timedelta(days=6)).replace(hour=17, minute=0, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=6)).replace(hour=22, minute=0, second=0, microsecond=0),
                'ubicacion': 'Plaza de la Independencia',
                'direccion': 'Plaza de la Independencia, Centro Histórico, Loja',
                'precio': Decimal('0.00'),
                'contacto': 'danza.loja@cultura.gob.ec',
            },
            
            # Eventos educativos
            {
                'titulo': 'Conferencia: Inteligencia Artificial',
                'descripcion': 'Conferencia sobre el futuro de la IA y su impacto en la sociedad. Incluye demostraciones prácticas.',
                'categoria': 'educativo',
                'fecha_inicio': (hoy + timedelta(days=7)).replace(hour=15, minute=0, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=7)).replace(hour=17, minute=30, second=0, microsecond=0),
                'ubicacion': 'Universidad Nacional de Loja',
                'direccion': 'Campus Universitario, Loja',
                'precio': Decimal('0.00'),
                'contacto': 'conferencias@unl.edu.ec',
            },
            
            # Eventos religiosos
            {
                'titulo': 'Procesión de la Virgen del Cisne',
                'descripcion': 'Procesión tradicional en honor a la Virgen del Cisne, patrona de Loja.',
                'categoria': 'religioso',
                'fecha_inicio': (hoy + timedelta(days=8)).replace(hour=8, minute=0, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=8)).replace(hour=12, minute=0, second=0, microsecond=0),
                'ubicacion': 'Basilica de Loja',
                'direccion': 'Calle 10 de Agosto, Centro Histórico, Loja',
                'precio': Decimal('0.00'),
                'contacto': 'basilica.loja@iglesia.ec',
            },
            
            # Más eventos variados
            {
                'titulo': 'Noche de Jazz en Loja',
                'descripcion': 'Presentación de jazz en vivo con músicos locales. Ambiente íntimo y acogedor.',
                'categoria': 'musica',
                'fecha_inicio': (hoy + timedelta(days=9)).replace(hour=20, minute=0, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=9)).replace(hour=23, minute=0, second=0, microsecond=0),
                'ubicacion': 'Café Cultural Loja',
                'direccion': 'Calle Lourdes, Loja',
                'precio': Decimal('12.00'),
                'contacto': 'jazz.loja@email.com',
            },
            {
                'titulo': 'Feria de Emprendedores',
                'descripcion': 'Feria donde emprendedores locales muestran sus productos y servicios. Apoya el comercio local.',
                'categoria': 'feria',
                'fecha_inicio': (hoy + timedelta(days=10)).replace(hour=9, minute=0, second=0, microsecond=0),
                'fecha_fin': (hoy + timedelta(days=10)).replace(hour=18, minute=0, second=0, microsecond=0),
                'ubicacion': 'Centro Comercial Loja',
                'direccion': 'Av. 8 de Diciembre, Loja',
                'precio': Decimal('0.00'),
                'contacto': 'emprendedores@loja.gob.ec',
            },
            
            # Evento específico para probar fecha exacta (3 de noviembre)
            {
                'titulo': 'Festival de la Cerveza Artesanal',
                'descripcion': 'Festival con las mejores cervezas artesanales de la región. Música en vivo y comida.',
                'categoria': 'gastronomia',
                'fecha_inicio': datetime(2024, 11, 3, 16, 0, 0),
                'fecha_fin': datetime(2024, 11, 3, 23, 0, 0),
                'ubicacion': 'Parque Recreacional Jipiro',
                'direccion': 'Parque Jipiro, Loja',
                'precio': Decimal('18.00'),
                'contacto': 'cerveza.artesanal@loja.com',
            },
            {
                'titulo': 'Concierto de Música Clásica',
                'descripcion': 'Orquesta sinfónica de Loja presenta un repertorio de música clásica internacional.',
                'categoria': 'musica',
                'fecha_inicio': datetime(2024, 11, 3, 19, 30, 0),
                'fecha_fin': datetime(2024, 11, 3, 21, 30, 0),
                'ubicacion': 'Teatro Bolívar',
                'direccion': 'Calle Bolívar, Centro Histórico, Loja',
                'precio': Decimal('20.00'),
                'contacto': 'orquesta.loja@cultura.gob.ec',
            },
            
            # Eventos entre 15 y 20 de noviembre para probar rangos de fechas
            {
                'titulo': 'Festival de Cine Independiente',
                'descripcion': 'Proyección de películas independientes de directores ecuatorianos. Entrada gratuita.',
                'categoria': 'cultural',
                'fecha_inicio': datetime(2024, 11, 15, 18, 0, 0),
                'fecha_fin': datetime(2024, 11, 15, 22, 0, 0),
                'ubicacion': 'Centro Cultural Loja',
                'direccion': 'Av. 24 de Mayo, Loja',
                'precio': Decimal('0.00'),
                'contacto': 'cine.loja@cultura.gob.ec',
            },
            {
                'titulo': 'Conferencia de Tecnología',
                'descripcion': 'Conferencia sobre las últimas tendencias en tecnología e innovación. Incluye networking.',
                'categoria': 'educativo',
                'fecha_inicio': datetime(2024, 11, 16, 14, 0, 0),
                'fecha_fin': datetime(2024, 11, 16, 18, 0, 0),
                'ubicacion': 'Universidad Técnica Particular de Loja',
                'direccion': 'Campus UTPL, Loja',
                'precio': Decimal('15.00'),
                'contacto': 'tecnologia@utpl.edu.ec',
            },
            {
                'titulo': 'Festival de Comida Típica',
                'descripcion': 'Festival gastronómico con los mejores platos típicos de Loja. Música folclórica en vivo.',
                'categoria': 'gastronomia',
                'fecha_inicio': datetime(2024, 11, 17, 10, 0, 0),
                'fecha_fin': datetime(2024, 11, 17, 20, 0, 0),
                'ubicacion': 'Plaza de San Francisco',
                'direccion': 'Plaza de San Francisco, Centro Histórico, Loja',
                'precio': Decimal('0.00'),
                'contacto': 'gastronomia.loja@turismo.gob.ec',
            },
            {
                'titulo': 'Torneo de Fútbol Local',
                'descripcion': 'Final del torneo de fútbol local. Ven a apoyar a los equipos de Loja.',
                'categoria': 'deporte',
                'fecha_inicio': datetime(2024, 11, 18, 15, 0, 0),
                'fecha_fin': datetime(2024, 11, 18, 18, 0, 0),
                'ubicacion': 'Estadio Reina del Cisne',
                'direccion': 'Av. Universitaria, Loja',
                'precio': Decimal('8.00'),
                'contacto': 'deportes.loja@municipio.gob.ec',
            },
            {
                'titulo': 'Noche de Poesía',
                'descripcion': 'Lectura de poesía con poetas locales e invitados especiales. Ambiente íntimo y acogedor.',
                'categoria': 'cultural',
                'fecha_inicio': datetime(2024, 11, 19, 19, 0, 0),
                'fecha_fin': datetime(2024, 11, 19, 21, 0, 0),
                'ubicacion': 'Café Literario Loja',
                'direccion': 'Calle Lourdes, Loja',
                'precio': Decimal('5.00'),
                'contacto': 'poesia.loja@cultura.gob.ec',
            },
            {
                'titulo': 'Feria de Artesanías',
                'descripcion': 'Feria con productos artesanales de toda la provincia. Ideal para comprar regalos únicos.',
                'categoria': 'feria',
                'fecha_inicio': datetime(2024, 11, 20, 9, 0, 0),
                'fecha_fin': datetime(2024, 11, 20, 19, 0, 0),
                'ubicacion': 'Parque Central de Loja',
                'direccion': 'Parque Central, Centro Histórico, Loja',
                'precio': Decimal('0.00'),
                'contacto': 'artesanias.loja@turismo.gob.ec',
            },
        ]
        
        # Convertir fechas a timezone-aware si no lo son
        for evento_data in eventos_data:
            if not timezone.is_aware(evento_data['fecha_inicio']):
                evento_data['fecha_inicio'] = timezone.make_aware(evento_data['fecha_inicio'])
            if evento_data.get('fecha_fin') and not timezone.is_aware(evento_data['fecha_fin']):
                evento_data['fecha_fin'] = timezone.make_aware(evento_data['fecha_fin'])
        
        # Crear eventos
        eventos_creados = 0
        for evento_data in eventos_data:
            evento, created = Evento.objects.get_or_create(
                titulo=evento_data['titulo'],
                fecha_inicio=evento_data['fecha_inicio'],
                defaults=evento_data
            )
            if created:
                eventos_creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {evento.titulo}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⊘ Ya existe: {evento.titulo}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n¡Listo! Se crearon {eventos_creados} eventos nuevos. '
                f'Total de eventos en la base de datos: {Evento.objects.count()}'
            )
        )

