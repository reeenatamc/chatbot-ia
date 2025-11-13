"""
Módulo para manejar consultas de eventos usando Gemini para interpretar
el lenguaje natural y extraer parámetros para las consultas SQL.
"""
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from .models import Evento
from google import genai
from django.conf import settings
import json
import re


def interpretar_consulta_usuario(mensaje_usuario):
    """
    Usa Gemini para interpretar el mensaje del usuario y extraer parámetros
    estructurados para las consultas SQL.
    
    Retorna un diccionario con los parámetros extraídos.
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    # Obtener fecha y hora actual
    ahora = timezone.now()
    fecha_actual = ahora.strftime('%Y-%m-%d')
    hora_actual = ahora.strftime('%H:%M:%S')
    dia_semana = ahora.strftime('%A')  # Lunes, Martes, etc.
    dia_mes = ahora.day
    mes_actual = ahora.month
    año_actual = ahora.year
    
    prompt = f"""Eres un asistente que interpreta consultas sobre eventos en la ciudad de Loja.
Tu tarea es extraer parámetros estructurados del siguiente mensaje del usuario.

FECHA Y HORA ACTUAL (usa esta información como referencia):
- Fecha actual: {fecha_actual}
- Hora actual: {hora_actual}
- Día de la semana: {dia_semana}
- Día del mes: {dia_mes}
- Mes actual: {mes_actual}
- Año actual: {año_actual}

Mensaje del usuario: "{mensaje_usuario}"

Debes extraer y retornar SOLO un JSON válido con los siguientes campos posibles:
- es_sobre_eventos: true si la pregunta es sobre eventos en Loja, false si es sobre otro tema
- tipo_consulta: "por_fecha", "por_rango_fechas", "por_categoria", "por_ubicacion", "gratuitos", "proximos", "busqueda", "todos" (solo si es_sobre_eventos es true)
- fecha: fecha específica en formato YYYY-MM-DD (si menciona una fecha como "3 de noviembre", "mañana", "hoy", etc.)
- fecha_inicio: fecha de inicio del rango en formato YYYY-MM-DD (si pregunta "entre X y Y" o "del X al Y")
- fecha_fin: fecha de fin del rango en formato YYYY-MM-DD (si pregunta "entre X y Y" o "del X al Y")
- categoria: una de estas opciones: musica, deporte, cultural, gastronomia, educativo, religioso, feria, teatro, danza, otro
- ubicacion: nombre de ubicación mencionada
- texto_busqueda: palabras clave para buscar en título/descripción
- solo_gratuitos: true si pregunta por eventos gratuitos
- dias_proximos: número de días (si pregunta "próximos eventos" o "esta semana")

IMPORTANTE - USAR FECHA Y HORA ACTUAL COMO REFERENCIA:
- Si menciona "hoy", usa la fecha actual: {fecha_actual}
- Si menciona "mañana", calcula la fecha del día siguiente a {fecha_actual}
- Si menciona días de la semana (lunes, martes, etc.), calcula la fecha correspondiente basándote en que hoy es {dia_semana}
- Si menciona "3 de noviembre" o "3 de nov", asume año {año_actual} si no se especifica otro año
- Si menciona fechas relativas como "esta semana", "próxima semana", calcula basándote en la fecha actual
- Si menciona un RANGO de fechas como "entre el 15 y el 20 de noviembre" o "del 15 al 20 de nov", usa tipo_consulta: "por_rango_fechas" y proporciona fecha_inicio y fecha_fin
- Retorna SOLO el JSON, sin texto adicional, sin markdown, sin explicaciones

Ejemplos de respuesta:
- Fecha específica: {{"tipo_consulta": "por_fecha", "fecha": "{fecha_actual}"}}
- Rango de fechas: {{"tipo_consulta": "por_rango_fechas", "fecha_inicio": "2024-11-15", "fecha_fin": "2024-11-20"}}
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        # Extraer JSON de la respuesta
        texto_respuesta = response.text.strip()
        
        # Limpiar si viene con markdown
        texto_respuesta = re.sub(r'```json\s*', '', texto_respuesta)
        texto_respuesta = re.sub(r'```\s*', '', texto_respuesta)
        texto_respuesta = texto_respuesta.strip()
        
        # Parsear JSON
        parametros = json.loads(texto_respuesta)
        return parametros
        
    except Exception as e:
        # Si falla, intentar búsqueda genérica
        return {
            "tipo_consulta": "busqueda",
            "texto_busqueda": mensaje_usuario
        }


def formatear_fecha(fecha_str):
    """
    Convierte una fecha en string a objeto datetime.
    Maneja fechas relativas como "hoy", "mañana", etc.
    """
    if not fecha_str:
        return None
    
    fecha_str = fecha_str.strip()
    hoy = timezone.now().date()
    
    # Fechas relativas
    if fecha_str.lower() == "hoy":
        return timezone.make_aware(datetime.combine(hoy, datetime.min.time()))
    elif fecha_str.lower() == "mañana":
        manana = hoy + timedelta(days=1)
        return timezone.make_aware(datetime.combine(manana, datetime.min.time()))
    
    # Intentar parsear fecha en formato YYYY-MM-DD
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        return timezone.make_aware(datetime.combine(fecha_obj, datetime.min.time()))
    except:
        pass
    
    # Intentar otros formatos comunes
    try:
        # Formato DD/MM/YYYY
        fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y').date()
        return timezone.make_aware(datetime.combine(fecha_obj, datetime.min.time()))
    except:
        pass
    
    return None


def ejecutar_consulta_eventos(parametros):
    """
    Ejecuta la consulta de eventos basada en los parámetros extraídos.
    Usa el ORM de Django para seguridad.
    """
    # Base query: solo eventos activos
    query = Evento.objects.filter(activo=True)
    
    tipo_consulta = parametros.get('tipo_consulta', 'todos')
    
    if tipo_consulta == 'por_fecha':
        fecha = formatear_fecha(parametros.get('fecha'))
        if fecha:
            # Eventos que empiezan en esa fecha
            fecha_fin = fecha + timedelta(days=1)
            query = query.filter(fecha_inicio__gte=fecha, fecha_inicio__lt=fecha_fin)
        else:
            # Si no se pudo parsear la fecha, retornar vacío
            return Evento.objects.none()
    
    elif tipo_consulta == 'por_rango_fechas':
        fecha_inicio = formatear_fecha(parametros.get('fecha_inicio'))
        fecha_fin = formatear_fecha(parametros.get('fecha_fin'))
        
        if fecha_inicio and fecha_fin:
            # Eventos que empiezan dentro del rango (incluyendo ambas fechas)
            # Incluir eventos que empiezan desde fecha_inicio hasta el final del día de fecha_fin
            fecha_fin_dia = fecha_fin + timedelta(days=1)
            query = query.filter(
                fecha_inicio__gte=fecha_inicio,
                fecha_inicio__lt=fecha_fin_dia
            )
        elif fecha_inicio:
            # Si solo hay fecha_inicio, buscar desde esa fecha
            query = query.filter(fecha_inicio__gte=fecha_inicio)
        elif fecha_fin:
            # Si solo hay fecha_fin, buscar hasta esa fecha
            fecha_fin_dia = fecha_fin + timedelta(days=1)
            query = query.filter(fecha_inicio__lt=fecha_fin_dia)
        else:
            # Si no se pudieron parsear las fechas, retornar vacío
            return Evento.objects.none()
    
    elif tipo_consulta == 'por_categoria':
        categoria = parametros.get('categoria')
        if categoria:
            query = query.filter(categoria=categoria)
    
    elif tipo_consulta == 'por_ubicacion':
        ubicacion = parametros.get('ubicacion', '')
        if ubicacion:
            query = query.filter(
                Q(ubicacion__icontains=ubicacion) | 
                Q(direccion__icontains=ubicacion)
            )
    
    elif tipo_consulta == 'gratuitos' or parametros.get('solo_gratuitos'):
        query = query.filter(precio=0)
    
    elif tipo_consulta == 'proximos':
        dias = parametros.get('dias_proximos', 7)
        fecha_limite = timezone.now() + timedelta(days=dias)
        query = query.filter(
            fecha_inicio__gte=timezone.now(),
            fecha_inicio__lte=fecha_limite
        )
    
    elif tipo_consulta == 'busqueda':
        texto = parametros.get('texto_busqueda', '')
        if texto:
            query = query.filter(
                Q(titulo__icontains=texto) |
                Q(descripcion__icontains=texto) |
                Q(ubicacion__icontains=texto)
            )
    
    # Ordenar por fecha de inicio
    query = query.order_by('fecha_inicio')
    
    return query


def formatear_respuesta_eventos(eventos, parametros):
    """
    Formatea los eventos encontrados en una respuesta amigable usando Gemini.
    """
    if not eventos.exists():
        return "No encontré eventos que coincidan con tu búsqueda. ¿Podrías intentar con otros criterios?"
    
    # Preparar información de eventos para Gemini
    eventos_info = []
    for evento in eventos:
        eventos_info.append({
            'titulo': evento.titulo,
            'descripcion': evento.descripcion[:200],  # Limitar descripción
            'fecha': evento.fecha_inicio.strftime('%d/%m/%Y %H:%M'),
            'ubicacion': evento.ubicacion,
            'precio': 'Gratis' if evento.es_gratuito else f'${evento.precio}',
            'categoria': evento.get_categoria_display()
        })
    
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    prompt = f"""Eres un asistente amigable que informa sobre eventos en la ciudad de Loja, Ecuador.
El usuario hizo la siguiente consulta y encontré {len(eventos_info)} evento(s).

Información de los eventos:
{json.dumps(eventos_info, ensure_ascii=False, indent=2)}

Genera una respuesta amigable y natural en español con jerga lojana sutil que:
1. Mencione cuántos eventos se encontraron
2. Liste los eventos de forma clara y organizada
3. Incluya la información relevante (fecha, hora, ubicación, precio, categoría)
4. Sea conversacional y útil

JERGA LOJANA SUTIL (usa algunas de estas expresiones de forma natural, sin exagerar):
- "Chevere" o "chévere" (genial, bueno) - ejemplo: "¡Qué chevere!"
- "Pues" al final de algunas frases - ejemplo: "Hay varios eventos, pues"
- "No más" al final de frases - ejemplo: "Te paso la info, no más"
- "Vaya" (expresión de asombro) - ejemplo: "Vaya, encontré varios eventos"
- "A ver" (déjame ver) - ejemplo: "A ver, déjame contarte"
- Forma de hablar más pausada y amigable, como lojanos
- Usa "mijo" o "mija" ocasionalmente de forma cariñosa si es apropiado

IMPORTANTE:
- Usa la jerga de forma natural y sutil, no en cada frase
- Mantén el tono amigable y profesional
- No exageres con las expresiones
- Responde SOLO con el texto, sin formato markdown, sin listas numeradas, solo texto natural
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        # Fallback: respuesta simple si Gemini falla
        respuesta = f"Encontré {len(eventos_info)} evento(s):\n\n"
        for evento in eventos_info:
            respuesta += f"• {evento['titulo']} - {evento['fecha']} en {evento['ubicacion']} ({evento['precio']})\n"
        return respuesta


def generar_respuesta_fallback(mensaje_usuario):
    """
    Genera una respuesta corta (máximo una línea) para preguntas fuera de tema,
    siempre redirigiendo a preguntar sobre eventos.
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    prompt = f"""Eres un asistente de eventos en la ciudad de Loja, Ecuador. El usuario hizo una pregunta que NO es sobre eventos.

Pregunta del usuario: "{mensaje_usuario}"

Tu tarea es:
1. Responder brevemente a la pregunta (máximo una línea, muy corto)
2. Siempre redirigir amigablemente a preguntar sobre eventos en Loja
3. Usa jerga lojana sutil (pues, no más, chevere, vaya) de forma natural

IMPORTANTE:
- Máximo una línea de respuesta
- Responde de forma amigable y natural con jerga lojana sutil
- Siempre termina redirigiendo a eventos
- No uses markdown, solo texto natural
- Usa expresiones como "pues", "no más", "chevere" de forma sutil

Ejemplos de respuestas:
- "No tengo esa información, pero puedo ayudarte a encontrar eventos en Loja, pues. ¿Qué tipo de eventos te interesan?"
- "Esa pregunta está fuera de mi alcance, pero puedo contarte sobre eventos en Loja, no más. ¿Qué eventos buscas?"
- "No puedo ayudarte con eso, pero sé mucho sobre eventos en Loja. ¿Qué eventos te gustaría conocer, mijo?"

Responde SOLO con el texto, sin explicaciones adicionales.
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        # Fallback si Gemini falla
        return "No puedo ayudarte con eso, pero puedo contarte sobre eventos en Loja. ¿Qué eventos te interesan?"

