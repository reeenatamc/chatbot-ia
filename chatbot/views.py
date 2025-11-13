from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .evento_queries import (
    interpretar_consulta_usuario,
    ejecutar_consulta_eventos,
    formatear_respuesta_eventos,
    generar_respuesta_fallback
)
from .models import Evento

# Create your views here.

def index(request):
    """Vista principal del chatbot"""
    return render(request, 'chatbot/index.html')

@csrf_exempt
def chat(request):
    """
    Endpoint para recibir mensajes y responder con Gemini.
    Gemini interpreta la consulta, extrae parámetros y ejecuta consultas SQL predefinidas.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'Mensaje vacío'}, status=400)
            
            lower_message = user_message.strip().lower()
            
            # Respuestas quemadas para preguntas frecuentes
            faq_responses = {
                'eventos de hoy': 'eventos de hoy',
                'eventos de esta semana': 'eventos de esta semana',
                'eventos de este mes': 'eventos de este mes',
                'eventos gratis': 'eventos gratis',
                'eventos de música': 'eventos de música',
                'eventos de teatro': 'eventos de teatro'
            }
            
            # Verificar si es una pregunta frecuente
            is_faq = False
            for faq_key in faq_responses.keys():
                if faq_key in lower_message:
                    is_faq = True
                    # Normalizar la consulta para que funcione con el sistema existente
                    user_message = faq_responses[faq_key]
                    break
            detalle_prefix = "dame más información sobre "
            eventos_info = []

            if lower_message.startswith(detalle_prefix):
                titulo_evento = user_message.strip()[len(detalle_prefix):].strip()

                if not titulo_evento:
                    return JsonResponse({
                        'response': 'Necesito que me digas el nombre del evento del que quieres más información.'
                    })

                evento = Evento.objects.filter(titulo__iexact=titulo_evento).first()

                if not evento:
                    return JsonResponse({
                        'response': f"No encontré un evento con el nombre '{titulo_evento}'. ¿Quieres intentar con otro nombre?"
                    })

                fecha_inicio = timezone.localtime(evento.fecha_inicio)
                fecha_fin = timezone.localtime(evento.fecha_fin) if evento.fecha_fin else None

                fecha_texto = fecha_inicio.strftime('%d/%m/%Y a las %H:%M')
                if fecha_fin and fecha_fin.date() != fecha_inicio.date():
                    fecha_texto += f" hasta el {fecha_fin.strftime('%d/%m/%Y a las %H:%M')}"
                elif fecha_fin and fecha_fin != fecha_inicio:
                    fecha_texto += f" hasta las {fecha_fin.strftime('%H:%M')}"

                precio_texto = "Gratis" if evento.es_gratuito else f"${evento.precio}"
                ubicacion_texto = evento.ubicacion or "Ubicación por confirmar"
                direccion_texto = f" ({evento.direccion})" if evento.direccion else ""
                descripcion = (evento.descripcion or "").strip()

                lineas_respuesta = [
                    f"A ver, mijo, te cuento del {evento.titulo}:",
                    f"[calendar] **Fecha y horario:** {fecha_texto}",
                    f"[location] **Lugar:** {ubicacion_texto}{direccion_texto}",
                ]

                if descripcion:
                    lineas_respuesta.append(f"[detail] **¿Qué habrá?:** {descripcion}")

                lineas_respuesta.append(f"[price] **Costo:** {precio_texto}")
                lineas_respuesta.append(f"[category] **Categoría:** {evento.get_categoria_display()}")

                if evento.contacto:
                    lineas_respuesta.append(f"[contact] **Contacto:** {evento.contacto}")
                if evento.enlace:
                    lineas_respuesta.append(f"[link] **Más info:** {evento.enlace}")

                lineas_respuesta.append("Apoya lo local.")

                respuesta_detalle = "\n".join(lineas_respuesta)

                eventos_info.append({
                    'titulo': evento.titulo,
                    'descripcion': evento.descripcion or '',
                    'fecha': fecha_inicio.strftime('%d/%m/%Y %H:%M'),
                    'ubicacion': ubicacion_texto,
                    'precio': precio_texto,
                    'categoria': evento.get_categoria_display()
                })

                return JsonResponse({
                    'response': respuesta_detalle,
                    'events': eventos_info
                })

            # Paso 1: Gemini interpreta el mensaje y extrae parámetros
            parametros = interpretar_consulta_usuario(user_message)
            
            # Verificar si la pregunta es sobre eventos
            es_sobre_eventos = parametros.get('es_sobre_eventos', True)
            es_recomendacion = parametros.get('es_recomendacion', False)
            tipo_consulta = parametros.get('tipo_consulta', '')
            
            # Solo tratar como recomendación si es explícitamente una recomendación SIN parámetros específicos
            # Si hay parámetros como fecha, categoría, etc., NO es una recomendación simple
            tiene_parametros_especificos = any([
                parametros.get('fecha'),
                parametros.get('fecha_inicio'),
                parametros.get('fecha_fin'),
                parametros.get('categoria'),
                parametros.get('ubicacion'),
                parametros.get('solo_gratuitos'),
                parametros.get('dias_proximos'),
                tipo_consulta in ['por_fecha', 'por_rango_fechas', 'por_categoria', 'por_ubicacion', 'gratuitos', 'proximos']
            ])
            
            # Solo es recomendación si Gemini lo detectó Y no hay parámetros específicos
            es_recomendacion_simple = es_recomendacion and not tiene_parametros_especificos
            
            if not es_sobre_eventos:
                # Usar fallback para preguntas fuera de tema
                respuesta = generar_respuesta_fallback(user_message)
                eventos_info = []
            elif es_recomendacion_simple:
                # Obtener un evento aleatorio activo
                import random
                eventos_activos = list(Evento.objects.filter(activo=True))
                
                if eventos_activos:
                    evento_aleatorio = random.choice(eventos_activos)
                    fecha_inicio = timezone.localtime(evento_aleatorio.fecha_inicio)
                    
                    precio_texto = "Gratis" if evento_aleatorio.es_gratuito else f"${evento_aleatorio.precio}"
                    ubicacion_texto = evento_aleatorio.ubicacion or "Ubicación por confirmar"
                    
                    # Usar Gemini para generar una respuesta personalizada basada en el contexto del mensaje
                    from .evento_queries import generar_respuesta_recomendacion
                    respuesta = generar_respuesta_recomendacion(evento_aleatorio, user_message)
                    
                    eventos_info = [{
                        'titulo': evento_aleatorio.titulo,
                        'descripcion': evento_aleatorio.descripcion or '',
                        'fecha': fecha_inicio.strftime('%d/%m/%Y %H:%M'),
                        'ubicacion': ubicacion_texto,
                        'precio': precio_texto,
                        'categoria': evento_aleatorio.get_categoria_display()
                    }]
                else:
                    respuesta = 'Lo siento, no hay eventos disponibles en este momento. Pronto habrá más eventos chéveres en Loja.'
                    eventos_info = []
            else:
                # Paso 2: Ejecutar consulta SQL predefinida con los parámetros
                eventos = ejecutar_consulta_eventos(parametros)
                
                # Paso 3: Formatear respuesta usando Gemini
                respuesta, eventos_info = formatear_respuesta_eventos(eventos, parametros)
            
            return JsonResponse({
                'response': respuesta,
                'events': eventos_info
            })
            
        except Exception as e:
            return JsonResponse({
                'error': f'Error al procesar la solicitud: {str(e)}'
            }, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
