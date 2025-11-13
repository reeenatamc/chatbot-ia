from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class Evento(models.Model):
    """Modelo para almacenar eventos de la ciudad de Loja"""
    
    CATEGORIA_CHOICES = [
        ('musica', 'Música'),
        ('deporte', 'Deporte'),
        ('cultural', 'Cultural'),
        ('gastronomia', 'Gastronomía'),
        ('educativo', 'Educativo'),
        ('religioso', 'Religioso'),
        ('feria', 'Feria'),
        ('teatro', 'Teatro'),
        ('danza', 'Danza'),
        ('otro', 'Otro'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción')
    categoria = models.CharField(
        max_length=20, 
        choices=CATEGORIA_CHOICES, 
        default='otro',
        verbose_name='Categoría'
    )
    fecha_inicio = models.DateTimeField(verbose_name='Fecha y hora de inicio')
    fecha_fin = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Fecha y hora de fin (opcional)'
    )
    ubicacion = models.CharField(max_length=200, verbose_name='Ubicación')
    direccion = models.TextField(
        blank=True, 
        verbose_name='Dirección completa (opcional)'
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Precio',
        help_text='0.00 para eventos gratuitos'
    )
    imagen = models.ImageField(
        upload_to='eventos/', 
        null=True, 
        blank=True,
        verbose_name='Imagen del evento'
    )
    contacto = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='Contacto (teléfono, email, etc.)'
    )
    enlace = models.URLField(
        blank=True,
        verbose_name='Enlace adicional (opcional)'
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Desmarcar para ocultar el evento'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['fecha_inicio']
        indexes = [
            models.Index(fields=['fecha_inicio']),
            models.Index(fields=['categoria']),
            models.Index(fields=['activo']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha_inicio.strftime('%d/%m/%Y')}"
    
    @property
    def es_gratuito(self):
        """Retorna True si el evento es gratuito"""
        return self.precio == Decimal('0.00')
