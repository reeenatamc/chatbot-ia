from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
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
    actions = ['eliminar_eventos_pasados']
    
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
    
    @admin.action(description='Eliminar eventos pasados')
    def eliminar_eventos_pasados(self, request, queryset):
        """
        Elimina eventos cuya fecha de inicio ya haya pasado.
        Si se seleccionaron eventos específicos, solo elimina los pasados de esa selección.
        Si no se seleccionó ninguno, elimina todos los eventos pasados.
        """
        ahora = timezone.now()
        
        if queryset.exists():
            # Si hay eventos seleccionados, solo eliminar los pasados de esa selección
            eventos_pasados = queryset.filter(fecha_inicio__lt=ahora)
            cantidad = eventos_pasados.count()
            
            if cantidad == 0:
                self.message_user(
                    request,
                    'No hay eventos pasados en la selección.',
                    messages.INFO
                )
                return
            
            eventos_pasados.delete()
            self.message_user(
                request,
                f'Se eliminaron {cantidad} evento(s) pasado(s) exitosamente.',
                messages.SUCCESS
            )
        else:
            # Si no hay selección, eliminar todos los eventos pasados
            eventos_pasados = Evento.objects.filter(fecha_inicio__lt=ahora)
            cantidad = eventos_pasados.count()
            
            if cantidad == 0:
                self.message_user(
                    request,
                    'No hay eventos pasados para eliminar.',
                    messages.INFO
                )
                return
            
            eventos_pasados.delete()
            self.message_user(
                request,
                f'Se eliminaron {cantidad} evento(s) pasado(s) exitosamente.',
                messages.SUCCESS
            )
