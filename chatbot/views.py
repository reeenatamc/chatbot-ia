from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .evento_queries import (
    interpretar_consulta_usuario,
    ejecutar_consulta_eventos,
    formatear_respuesta_eventos,
    generar_respuesta_fallback
)

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
            
            # Paso 1: Gemini interpreta el mensaje y extrae parámetros
            parametros = interpretar_consulta_usuario(user_message)
            
            # Verificar si la pregunta es sobre eventos
            es_sobre_eventos = parametros.get('es_sobre_eventos', True)
            
            if not es_sobre_eventos:
                # Usar fallback para preguntas fuera de tema
                respuesta = generar_respuesta_fallback(user_message)
            else:
                # Paso 2: Ejecutar consulta SQL predefinida con los parámetros
                eventos = ejecutar_consulta_eventos(parametros)
                
                # Paso 3: Formatear respuesta usando Gemini
                respuesta = formatear_respuesta_eventos(eventos, parametros)
            
            return JsonResponse({
                'response': respuesta
            })
            
        except Exception as e:
            return JsonResponse({
                'error': f'Error al procesar la solicitud: {str(e)}'
            }, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
