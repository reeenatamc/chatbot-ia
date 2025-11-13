from django.contrib import admin
from unfold.decorators import display
from unfold.admin import ModelAdmin
from .models import Evento

# Register your models here.

@admin.register(Evento)
class EventoAdmin(ModelAdmin):
    list_display = [
        'titulo', 
        'categoria', 
        'fecha_inicio', 
        'ubicacion', 
        'precio_display',
        'activo_display'
    ]
    list_filter = ['categoria', 'activo', 'fecha_inicio', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'ubicacion']
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'descripcion', 'categoria', 'imagen')
        }),
        ('Fecha y hora', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Ubicación', {
            'fields': ('ubicacion', 'direccion')
        }),
        ('Información adicional', {
            'fields': ('precio', 'contacto', 'enlace', 'activo')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    @display(description='Precio')
    def precio_display(self, obj):
        if obj.es_gratuito:
            return 'Gratis'
        return f'${obj.precio}'
    
    @display(description='Activo', boolean=True)
    def activo_display(self, obj):
        return obj.activo
