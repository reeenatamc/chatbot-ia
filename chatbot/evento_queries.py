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
- es_despedida: true si el usuario quiere terminar la conversación o despedirse. Ejemplos: "adiós", "chao", "hasta luego", "me voy", "nos vemos", "hasta pronto", "chao mijo", "nos vemos luego", "gracias, adiós", "listo, hasta luego", "ya me voy", etc. Si es_despedida es true, no necesitas procesar otros campos.
- es_sobre_eventos: true si la pregunta es sobre eventos en Loja, false si es sobre otro tema
- es_recomendacion: true SOLO si el usuario está pidiendo una recomendación genérica SIN especificar criterios (fecha, categoría, ubicación, etc.). Ejemplos: "que evento me recomiendas", "recomiéndame algo", "me recomiendas algo", "sugiere un evento", "dame una recomendación". IMPORTANTE: Si el usuario dice "recomiéndame eventos del 15 de noviembre" o "recomiéndame eventos de música", NO es una recomendación simple, es una consulta con parámetros específicos, así que es_recomendacion debe ser false. Solo es true cuando pide una recomendación sin criterios específicos.
- tipo_consulta: "por_fecha", "por_rango_fechas", "por_categoria", "por_ubicacion", "gratuitos", "proximos", "busqueda", "todos", "recomendacion" (solo si es_sobre_eventos es true). Si es_recomendacion es true, tipo_consulta debe ser "recomendacion"
- fecha: fecha específica en formato YYYY-MM-DD (si menciona una fecha como "3 de noviembre", "mañana", "hoy", etc.)
- fecha_inicio: fecha de inicio del rango en formato YYYY-MM-DD (si pregunta "entre X y Y" o "del X al Y")
- fecha_fin: fecha de fin del rango en formato YYYY-MM-DD (si pregunta "entre X y Y" o "del X al Y")
- hora: hora específica en formato HH:MM (24 horas) si menciona una hora. Ejemplos: "8 de la noche" -> "20:00", "8 pm" -> "20:00", "8:30 pm" -> "20:30", "20:00" -> "20:00", "8 de la mañana" -> "08:00", "8 am" -> "08:00"
- hora_inicio: hora de inicio del rango en formato HH:MM (24 horas) si menciona un rango de horas. Ejemplos: "entre las 7 y las 9" -> hora_inicio: "19:00", hora_fin: "21:00"
- hora_fin: hora de fin del rango en formato HH:MM (24 horas) si menciona un rango de horas
- periodo_dia: uno de estos períodos del día si menciona un período general: "madrugada", "mañana", "tarde", "noche". Ejemplos: "hay eventos en la mañana?" -> periodo_dia: "mañana", "eventos de la tarde" -> periodo_dia: "tarde", "eventos nocturnos" -> periodo_dia: "noche"
- categoria: una de estas opciones: musica, deporte, cultural, gastronomia, educativo, religioso, feria, teatro, danza, otro. Interpreta variaciones como "música", "musical", "concierto" -> "musica", "deportes" -> "deporte", "cultura" -> "cultural", "gastronómico" -> "gastronomia", etc.
- ubicacion: nombre de ubicación mencionada
- texto_busqueda: palabras clave para buscar en título/descripción
- solo_gratuitos: true si pregunta por eventos gratuitos
- precio_maximo: número máximo de precio en dólares (si pregunta "menos de X dólares", "menos de $X", "hasta X dólares", etc.). Los eventos gratuitos también cumplen este criterio
- dias_proximos: número de días (si pregunta "próximos eventos" o "esta semana")

IMPORTANTE - USAR FECHA Y HORA ACTUAL COMO REFERENCIA:
- Si menciona "hoy", usa la fecha actual: {fecha_actual}
- Si menciona "mañana", calcula la fecha del día siguiente a {fecha_actual}
- Si menciona días de la semana (lunes, martes, etc.), calcula la fecha correspondiente basándote en que hoy es {dia_semana}
- Si menciona "3 de noviembre" o "3 de nov", asume año {año_actual} si no se especifica otro año
- Si menciona fechas relativas como "esta semana", "próxima semana", calcula basándote en la fecha actual
- Si menciona un RANGO de fechas como "entre el 15 y el 20 de noviembre" o "del 15 al 20 de nov", usa tipo_consulta: "por_rango_fechas" y proporciona fecha_inicio y fecha_fin

IMPORTANTE - INTERPRETACIÓN DE HORAS:
- Interpreta horas en formato 24 horas (00:00 a 23:59)
- "8 de la noche", "8 pm", "8 p.m.", "8 de la tarde" -> "20:00"
- "8 de la mañana", "8 am", "8 a.m." -> "08:00"
- "mediodía", "12 del día" -> "12:00"
- "medianoche", "12 de la noche" -> "00:00"
- "8:30 pm", "8:30 de la noche" -> "20:30"
- Si menciona un rango de horas como "entre las 7 y las 9 de la noche" o "de 7 a 9 pm", proporciona hora_inicio: "19:00" y hora_fin: "21:00"
- Si menciona "a partir de las X" o "desde las X" o "después de las X", usa hora_inicio: "XX:00" (sin hora_fin). Ejemplos: "a partir de las 5pm" -> hora_inicio: "17:00", "desde las 8 de la noche" -> hora_inicio: "20:00", "después de las 3 de la tarde" -> hora_inicio: "15:00"
- Si menciona "hasta las X" o "antes de las X", usa hora_fin: "XX:00" (sin hora_inicio). Ejemplos: "hasta las 10pm" -> hora_fin: "22:00", "antes de las 6 de la tarde" -> hora_fin: "18:00"
- Puedes combinar fecha con hora: "eventos del 15 de noviembre a las 8 de la noche" -> fecha: "2024-11-15", hora: "20:00"
- Puedes combinar rango de fechas con rango de horas: "eventos del 15 al 20 de noviembre entre las 7 y las 9 pm" -> fecha_inicio: "2024-11-15", fecha_fin: "2024-11-20", hora_inicio: "19:00", hora_fin: "21:00"
- Puedes combinar fecha + hora_inicio + categoría + precio: "eventos de teatro el 7 de diciembre a partir de las 5pm que cuesten menos de 10 dólares" -> tipo_consulta: "por_fecha", fecha: "2024-12-07", hora_inicio: "17:00", categoria: "teatro", precio_maximo: 10

IMPORTANTE - INTERPRETACIÓN DE PERÍODOS DEL DÍA:
- Si menciona un período general del día (no una hora específica), usa periodo_dia en lugar de hora:
  - "mañana", "en la mañana", "durante la mañana", "por la mañana", "de mañana" -> periodo_dia: "mañana" (rango: 06:00 - 11:59)
  - "tarde", "en la tarde", "durante la tarde", "por la tarde", "de tarde" -> periodo_dia: "tarde" (rango: 12:00 - 18:59)
  - "noche", "en la noche", "durante la noche", "por la noche", "de noche", "nocturnos" -> periodo_dia: "noche" (rango: 19:00 - 23:59)
  - "madrugada", "en la madrugada", "durante la madrugada", "por la madrugada", "de madrugada" -> periodo_dia: "madrugada" (rango: 00:00 - 05:59)
- Ejemplos:
  - "hay eventos en la mañana?" -> periodo_dia: "mañana"
  - "eventos de la tarde" -> periodo_dia: "tarde"
  - "eventos nocturnos" -> periodo_dia: "noche"
  - "eventos de la madrugada" -> periodo_dia: "madrugada"
- Puedes combinar período del día con fecha: "eventos del 15 de noviembre en la mañana" -> fecha: "2024-11-15", periodo_dia: "mañana"
- Si menciona una hora específica (ej: "8 de la mañana"), usa hora: "08:00" en lugar de periodo_dia

IMPORTANTE - INTERPRETACIÓN DE CATEGORÍAS:
- Interpreta variaciones de categorías naturalmente:
  - "música", "musical", "concierto", "conciertos" -> "musica"
  - "deportes", "deportivo" -> "deporte"
  - "cultura", "cultural" -> "cultural"
  - "gastronomía", "gastronómico", "comida", "alimentario" -> "gastronomia"
  - "educación", "educativo", "educacional" -> "educativo"
  - "religión", "religioso" -> "religioso"
  - "feria", "ferias" -> "feria"
  - "teatro", "teatral" -> "teatro"
  - "danza", "danza", "baile" -> "danza"

IMPORTANTE - COMBINACIÓN DE PARÁMETROS:
- Puedes combinar múltiples parámetros: fecha + hora, fecha + categoría, fecha + hora + categoría + precio, fecha + periodo_dia, rango de fechas + rango de horas + categoría, etc.
- Cuando hay múltiples criterios, el tipo_consulta debe ser el del criterio más específico (fecha > categoría > búsqueda):
  - Si hay fecha específica o rango de fechas, usa tipo_consulta: "por_fecha" o "por_rango_fechas"
  - Si hay categoría pero NO fecha, usa tipo_consulta: "por_categoria"
  - Si hay solo texto de búsqueda o criterios generales sin fecha ni categoría específica, usa tipo_consulta: "busqueda"
- Ejemplo: "eventos de música el 15 de noviembre a las 8 de la noche" -> tipo_consulta: "por_fecha", fecha: "2024-11-15", hora: "20:00", categoria: "musica"
- Ejemplo: "eventos entre el 15 y el 20 de noviembre de las 7 a las 9 pm de gastronomía" -> tipo_consulta: "por_rango_fechas", fecha_inicio: "2024-11-15", fecha_fin: "2024-11-20", hora_inicio: "19:00", hora_fin: "21:00", categoria: "gastronomia"
- Ejemplo: "eventos del 15 de noviembre en la mañana de música" -> tipo_consulta: "por_fecha", fecha: "2024-11-15", periodo_dia: "mañana", categoria: "musica"
- Ejemplo: "eventos de teatro el 7 de diciembre a partir de las 5pm que cuesten menos de 10 dólares" -> tipo_consulta: "por_fecha", fecha: "2024-12-07", hora_inicio: "17:00", categoria: "teatro", precio_maximo: 10
- Ejemplo: "hay eventos en la mañana de deporte?" -> tipo_consulta: "busqueda", periodo_dia: "mañana", categoria: "deporte"

- Retorna SOLO el JSON, sin texto adicional, sin markdown, sin explicaciones

Ejemplos de respuesta:
- Despedida: {{"es_despedida": true}}
- "adiós": {{"es_despedida": true}}
- "chao, gracias": {{"es_despedida": true}}
- "hasta luego, mijo": {{"es_despedida": true}}
- Fecha específica: {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "por_fecha", "fecha": "{fecha_actual}"}}
- Rango de fechas: {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "por_rango_fechas", "fecha_inicio": "2024-11-15", "fecha_fin": "2024-11-20"}}
- Fecha con hora: {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "por_fecha", "fecha": "2024-11-15", "hora": "20:00"}}
- Rango de horas: {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "por_fecha", "fecha": "2024-11-15", "hora_inicio": "19:00", "hora_fin": "21:00"}}
- Fecha + hora + categoría: {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "por_fecha", "fecha": "2024-11-15", "hora": "20:00", "categoria": "musica"}}
- Recomendación: {{"es_sobre_eventos": true, "es_recomendacion": true, "tipo_consulta": "recomendacion"}}
- "que evento me recomiendas": {{"es_sobre_eventos": true, "es_recomendacion": true, "tipo_consulta": "recomendacion"}}
- "me recomiendas algo": {{"es_sobre_eventos": true, "es_recomendacion": true, "tipo_consulta": "recomendacion"}}
- "eventos de menos de 20 dólares": {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "busqueda", "precio_maximo": 20}}
- "eventos hasta $15": {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "busqueda", "precio_maximo": 15}}
- "eventos a las 8 de la noche": {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "busqueda", "hora": "20:00"}}
- "eventos entre las 7 y las 9 pm": {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "busqueda", "hora_inicio": "19:00", "hora_fin": "21:00"}}
- "eventos de música del 15 de noviembre a las 8 pm": {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "por_fecha", "fecha": "2024-11-15", "hora": "20:00", "categoria": "musica"}}
- "hay eventos en la mañana?": {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "busqueda", "periodo_dia": "mañana"}}
- "eventos de la tarde": {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "busqueda", "periodo_dia": "tarde"}}
- "eventos nocturnos": {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "busqueda", "periodo_dia": "noche"}}
- "eventos del 15 de noviembre en la mañana": {{"es_sobre_eventos": true, "es_recomendacion": false, "tipo_consulta": "por_fecha", "fecha": "2024-11-15", "periodo_dia": "mañana"}}
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


SPANISH_MONTHS = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'setiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12,
}


def detectar_fecha_en_texto(texto):
    """
    Intenta detectar una fecha a partir de un texto libre usando palabras clave o patrones comunes.
    Retorna una tupla (fecha_datetime, granularidad) o (None, None) si no se detecta.
    """
    if not texto:
        return (None, None)
    
    texto_normalizado = texto.lower()
    texto_normalizado = texto_normalizado.replace(',', ' ')
    
    # Palabras clave simples
    if "hoy" in texto_normalizado:
        return formatear_fecha("hoy")
    if "mañana" in texto_normalizado:
        return formatear_fecha("mañana")
    
    # Patrones como "15 de noviembre de 2025" o "15 de noviembre"
    patron_dia_mes = re.search(r'(\d{1,2})\s+de\s+([a-záéíóú]+)(?:\s+de)?\s*(\d{4})?', texto_normalizado)
    if patron_dia_mes:
        dia = patron_dia_mes.group(1)
        mes = patron_dia_mes.group(2)
        anio = patron_dia_mes.group(3) or ''
        fecha_str = f"{dia} de {mes} {anio}".strip()
        return formatear_fecha(fecha_str)
    
    # Patrones como "noviembre 2025"
    patron_mes_anio = re.search(r'([a-záéíóú]+)\s+(?:de\s+)?(\d{4})', texto_normalizado)
    if patron_mes_anio:
        mes = patron_mes_anio.group(1)
        anio = patron_mes_anio.group(2)
        return formatear_fecha(f"{mes} {anio}")
    
    # Solo el mes (ej. "noviembre")
    for mes_nombre in SPANISH_MONTHS:
        if mes_nombre in texto_normalizado:
            return formatear_fecha(mes_nombre)
    
    # Fechas numéricas comunes
    patron_iso = re.search(r'\b(\d{4})-(\d{2})(?:-(\d{2}))?\b', texto_normalizado)
    if patron_iso:
        anio, mes, dia = patron_iso.groups()
        if dia:
            return formatear_fecha(f"{anio}-{mes}-{dia}")
        return formatear_fecha(f"{anio}-{mes}")
    
    patron_dd_mm_yyyy = re.search(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', texto_normalizado)
    if patron_dd_mm_yyyy:
        dia, mes, anio = patron_dd_mm_yyyy.groups()
        return formatear_fecha(f"{dia}/{mes}/{anio}")
    
    return (None, None)


def formatear_fecha(fecha_str):
    """
    Convierte una fecha en string a objeto datetime.
    Maneja fechas relativas como "hoy", "mañana", etc.
    Retorna una tupla (fecha_datetime, granularidad) donde granularidad puede ser "dia" o "mes".
    """
    if not fecha_str:
        return (None, None)
    
    fecha_str = fecha_str.strip()
    hoy = timezone.now().date()
    
    # Fechas relativas
    if fecha_str.lower() == "hoy":
        return (timezone.make_aware(datetime.combine(hoy, datetime.min.time())), "dia")
    elif fecha_str.lower() == "mañana":
        manana = hoy + timedelta(days=1)
        return (timezone.make_aware(datetime.combine(manana, datetime.min.time())), "dia")
    
    # Intentar parsear fecha en formato YYYY-MM-DD
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        return (timezone.make_aware(datetime.combine(fecha_obj, datetime.min.time())), "dia")
    except:
        pass
    
    # Formato ISO con tiempo (YYYY-MM-DDTHH:MM:SS)
    try:
        fecha_obj = datetime.fromisoformat(fecha_str)
        if fecha_obj.tzinfo is None:
            fecha_obj = timezone.make_aware(fecha_obj)
        return (fecha_obj.replace(hour=0, minute=0, second=0, microsecond=0), "dia")
    except:
        pass
    
    # Formato YYYY-MM (mes completo)
    match_yyyy_mm = re.match(r'^(\d{4})-(\d{2})$', fecha_str)
    if match_yyyy_mm:
        year = int(match_yyyy_mm.group(1))
        month = int(match_yyyy_mm.group(2))
        fecha_obj = datetime(year, month, 1)
        return (timezone.make_aware(fecha_obj), "mes")
    
    # Formato MM/YYYY
    match_mm_yyyy = re.match(r'^(\d{1,2})/(\d{4})$', fecha_str)
    if match_mm_yyyy:
        month = int(match_mm_yyyy.group(1))
        year = int(match_mm_yyyy.group(2))
        fecha_obj = datetime(year, month, 1)
        return (timezone.make_aware(fecha_obj), "mes")
    
    # Intentar otros formatos comunes
    try:
        # Formato DD/MM/YYYY
        fecha_obj = datetime.strptime(fecha_str, '%d/%m/%Y').date()
        return (timezone.make_aware(datetime.combine(fecha_obj, datetime.min.time())), "dia")
    except:
        pass
    
    # Formatos con nombres de meses (ej. "3 de noviembre", "noviembre 2025", "noviembre")
    match_mes = re.match(
        r'^(?:(\d{1,2})\s+de\s+)?([a-záéíóú]+)(?:\s+de)?\s*(\d{4})?$', 
        fecha_str.lower()
    )
    if match_mes:
        dia_str, mes_str, anio_str = match_mes.groups()
        mes = SPANISH_MONTHS.get(mes_str)
        if mes:
            anio = int(anio_str) if anio_str else hoy.year
            dia = int(dia_str) if dia_str else 1
            fecha_obj = datetime(anio, mes, dia)
            granularidad = "dia" if dia_str else "mes"
            return (timezone.make_aware(fecha_obj), granularidad)
    
    return (None, None)


def _primer_dia_siguiente_mes(fecha):
    """
    Retorna un datetime aware correspondiente al primer día del mes siguiente.
    """
    year = fecha.year + (fecha.month // 12)
    month = fecha.month % 12 + 1
    return fecha.replace(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)


def ejecutar_consulta_eventos(parametros):
    """
    Ejecuta la consulta de eventos basada en los parámetros extraídos.
    Usa el ORM de Django para seguridad.
    """
    # Si es una recomendación, retornar lista vacía (se maneja en views.py)
    if parametros.get('es_recomendacion', False) or parametros.get('tipo_consulta') == 'recomendacion':
        return []
    
    # Base query: solo eventos activos
    query = Evento.objects.filter(activo=True)
    
    tipo_consulta = parametros.get('tipo_consulta', 'todos')
    
    # Filtrar eventos pasados automáticamente (excepto si se busca una fecha específica)
    # Si es consulta por fecha, no filtrar aquí (se filtra después según la fecha buscada)
    if tipo_consulta not in ['por_fecha', 'por_rango_fechas']:
        # Para otros tipos de consulta, filtrar eventos pasados automáticamente
        query = query.filter(fecha_inicio__gte=timezone.now())
    
    if tipo_consulta == 'por_fecha':
        fecha, granularidad = formatear_fecha(parametros.get('fecha'))
        if fecha:
            if granularidad == "mes":
                fecha_fin = _primer_dia_siguiente_mes(fecha)
            else:
                fecha_fin = fecha + timedelta(days=1)
            query = query.filter(fecha_inicio__gte=fecha, fecha_inicio__lt=fecha_fin)
        else:
            # Intentar con fecha_inicio o fecha_fin proporcionados
            fecha_inicio_aux, granularidad_inicio = formatear_fecha(parametros.get('fecha_inicio'))
            if fecha_inicio_aux:
                if granularidad_inicio == "mes":
                    fecha_fin_aux = _primer_dia_siguiente_mes(fecha_inicio_aux)
                else:
                    fecha_fin_aux = fecha_inicio_aux + timedelta(days=1)
                query = query.filter(fecha_inicio__gte=fecha_inicio_aux, fecha_inicio__lt=fecha_fin_aux)
            else:
                # Intentar detectar una fecha desde texto de búsqueda si existe
                texto = parametros.get('texto_busqueda', '')
                fecha_texto, granularidad_texto = detectar_fecha_en_texto(texto)
                if fecha_texto:
                    if granularidad_texto == "mes":
                        fecha_fin_texto = _primer_dia_siguiente_mes(fecha_texto)
                    else:
                        fecha_fin_texto = fecha_texto + timedelta(days=1)
                    query = query.filter(fecha_inicio__gte=fecha_texto, fecha_inicio__lt=fecha_fin_texto)
                else:
                    return Evento.objects.none()
    
    elif tipo_consulta == 'por_rango_fechas':
        fecha_inicio, granularidad_inicio = formatear_fecha(parametros.get('fecha_inicio'))
        fecha_fin, granularidad_fin = formatear_fecha(parametros.get('fecha_fin'))
        
        if fecha_inicio and fecha_fin:
            if granularidad_inicio == "mes":
                fecha_inicio = fecha_inicio  # ya es primer día del mes
            if granularidad_fin == "mes":
                fecha_fin_dia = _primer_dia_siguiente_mes(fecha_fin)
            else:
                fecha_fin_dia = fecha_fin + timedelta(days=1)
            query = query.filter(
                fecha_inicio__gte=fecha_inicio,
                fecha_inicio__lt=fecha_fin_dia
            )
        elif fecha_inicio:
            if granularidad_inicio == "mes":
                fecha_fin_dia = _primer_dia_siguiente_mes(fecha_inicio)
                query = query.filter(
                    fecha_inicio__gte=fecha_inicio,
                    fecha_inicio__lt=fecha_fin_dia
                )
            else:
                # Si solo hay fecha_inicio, buscar desde esa fecha
                query = query.filter(fecha_inicio__gte=fecha_inicio)
        elif fecha_fin:
            if granularidad_fin == "mes":
                fecha_fin_dia = _primer_dia_siguiente_mes(fecha_fin)
            else:
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
        fecha_detectada, granularidad_detectada = detectar_fecha_en_texto(texto)
        if fecha_detectada:
            if granularidad_detectada == "mes":
                fecha_fin_detectada = _primer_dia_siguiente_mes(fecha_detectada)
            else:
                fecha_fin_detectada = fecha_detectada + timedelta(days=1)
            query = query.filter(
                fecha_inicio__gte=fecha_detectada,
                fecha_inicio__lt=fecha_fin_detectada
            )
        elif texto:
            query = query.filter(
                Q(titulo__icontains=texto) |
                Q(descripcion__icontains=texto) |
                Q(ubicacion__icontains=texto)
            )
    
    # Filtrar por hora específica o rango de horas - se aplica a cualquier tipo de consulta
    hora = parametros.get('hora')
    hora_inicio = parametros.get('hora_inicio')
    hora_fin = parametros.get('hora_fin')
    
    if hora:
        # Hora específica: filtrar eventos que empiecen en esa hora (buscar toda esa hora)
        try:
            # Parsear hora en formato HH:MM
            hora_parts = hora.split(':')
            if len(hora_parts) == 2:
                hora_hh = int(hora_parts[0])
                hora_mm = int(hora_parts[1])
                # Buscar eventos que empiecen en esa hora (toda la hora si minutos son 0, o rango de ±30 min si hay minutos)
                if hora_mm == 0:
                    # Si es hora exacta (ej: 20:00), buscar toda esa hora
                    query = query.filter(fecha_inicio__hour=hora_hh)
                else:
                    # Si tiene minutos específicos (ej: 20:30), buscar eventos entre 20:00 y 21:00
                    query = query.filter(fecha_inicio__hour=hora_hh)
            elif len(hora_parts) == 1:
                # Solo se especificó la hora sin minutos, buscar toda esa hora
                hora_hh = int(hora_parts[0])
                query = query.filter(fecha_inicio__hour=hora_hh)
        except (ValueError, AttributeError):
            # Si no se puede parsear la hora, ignorar este filtro
            pass
    
    elif hora_inicio and hora_fin:
        # Rango de horas: filtrar eventos que empiecen en ese rango
        try:
            hora_inicio_parts = hora_inicio.split(':')
            hora_fin_parts = hora_fin.split(':')
            if len(hora_inicio_parts) == 2 and len(hora_fin_parts) == 2:
                hora_inicio_hh = int(hora_inicio_parts[0])
                hora_inicio_mm = int(hora_inicio_parts[1])
                hora_fin_hh = int(hora_fin_parts[0])
                hora_fin_mm = int(hora_fin_parts[1])
                
                # Si el rango cruza medianoche (ej: 22:00 a 02:00)
                if hora_fin_hh < hora_inicio_hh or (hora_fin_hh == hora_inicio_hh and hora_fin_mm <= hora_inicio_mm):
                    # Rango que cruza medianoche
                    query = query.filter(
                        Q(fecha_inicio__hour__gt=hora_inicio_hh) |
                        Q(fecha_inicio__hour__lt=hora_fin_hh) |
                        Q(fecha_inicio__hour=hora_inicio_hh, fecha_inicio__minute__gte=hora_inicio_mm) |
                        Q(fecha_inicio__hour=hora_fin_hh, fecha_inicio__minute__lt=hora_fin_mm)
                    )
                else:
                    # Rango normal dentro del mismo día
                    query = query.filter(
                        Q(fecha_inicio__hour__gt=hora_inicio_hh, fecha_inicio__hour__lt=hora_fin_hh) |
                        Q(fecha_inicio__hour=hora_inicio_hh, fecha_inicio__minute__gte=hora_inicio_mm) |
                        Q(fecha_inicio__hour=hora_fin_hh, fecha_inicio__minute__lt=hora_fin_mm)
                    )
        except (ValueError, AttributeError):
            # Si no se puede parsear la hora, ignorar este filtro
            pass
    
    elif hora_inicio:
        # Solo hora de inicio: filtrar eventos que empiecen desde esa hora
        try:
            hora_inicio_parts = hora_inicio.split(':')
            if len(hora_inicio_parts) == 2:
                hora_inicio_hh = int(hora_inicio_parts[0])
                hora_inicio_mm = int(hora_inicio_parts[1])
                query = query.filter(
                    Q(fecha_inicio__hour__gt=hora_inicio_hh) |
                    Q(fecha_inicio__hour=hora_inicio_hh, fecha_inicio__minute__gte=hora_inicio_mm)
                )
        except (ValueError, AttributeError):
            pass
    
    elif hora_fin:
        # Solo hora de fin: filtrar eventos que empiecen hasta esa hora
        try:
            hora_fin_parts = hora_fin.split(':')
            if len(hora_fin_parts) == 2:
                hora_fin_hh = int(hora_fin_parts[0])
                hora_fin_mm = int(hora_fin_parts[1])
                query = query.filter(
                    Q(fecha_inicio__hour__lt=hora_fin_hh) |
                    Q(fecha_inicio__hour=hora_fin_hh, fecha_inicio__minute__lt=hora_fin_mm)
                )
        except (ValueError, AttributeError):
            pass
    
    # Aplicar filtro de fecha SIEMPRE que esté presente en los parámetros, sin importar el tipo_consulta
    # Esto permite combinar filtros (ej: categoría + fecha + hora + precio)
    # Solo aplicar si no se aplicó ya en el bloque del tipo_consulta
    fecha_ya_aplicada = tipo_consulta in ['por_fecha', 'por_rango_fechas', 'proximos']
    
    if not fecha_ya_aplicada:
        # Verificar si hay una fecha en los parámetros que no se haya aplicado
        fecha_param = parametros.get('fecha')
        if fecha_param:
            fecha, granularidad = formatear_fecha(fecha_param)
            if fecha:
                if granularidad == "mes":
                    fecha_fin = _primer_dia_siguiente_mes(fecha)
                else:
                    fecha_fin = fecha + timedelta(days=1)
                query = query.filter(fecha_inicio__gte=fecha, fecha_inicio__lt=fecha_fin)
        
        # También verificar fecha_inicio si existe
        fecha_inicio_param = parametros.get('fecha_inicio')
        if fecha_inicio_param and not fecha_param:
            fecha_inicio, granularidad_inicio = formatear_fecha(fecha_inicio_param)
            if fecha_inicio:
                fecha_fin_param = parametros.get('fecha_fin')
                if fecha_fin_param:
                    # Hay un rango de fechas
                    fecha_fin, granularidad_fin = formatear_fecha(fecha_fin_param)
                    if fecha_fin:
                        if granularidad_fin == "mes":
                            fecha_fin_dia = _primer_dia_siguiente_mes(fecha_fin)
                        else:
                            fecha_fin_dia = fecha_fin + timedelta(days=1)
                        query = query.filter(
                            fecha_inicio__gte=fecha_inicio,
                            fecha_inicio__lt=fecha_fin_dia
                        )
                else:
                    # Solo fecha de inicio
                    if granularidad_inicio == "mes":
                        fecha_fin = _primer_dia_siguiente_mes(fecha_inicio)
                    else:
                        fecha_fin = fecha_inicio + timedelta(days=1)
                    query = query.filter(fecha_inicio__gte=fecha_inicio, fecha_inicio__lt=fecha_fin)
    
    # Filtrar por período del día - se aplica a cualquier tipo de consulta si está presente
    # Solo si no se especificó hora o rango de horas (ya que periodo_dia es más general)
    periodo_dia = parametros.get('periodo_dia')
    if periodo_dia and not hora and not hora_inicio and not hora_fin:
        if periodo_dia == "madrugada":
            # Madrugada: 00:00 - 05:59
            query = query.filter(fecha_inicio__hour__gte=0, fecha_inicio__hour__lte=5)
        elif periodo_dia == "mañana":
            # Mañana: 06:00 - 11:59
            query = query.filter(fecha_inicio__hour__gte=6, fecha_inicio__hour__lte=11)
        elif periodo_dia == "tarde":
            # Tarde: 12:00 - 18:59
            query = query.filter(fecha_inicio__hour__gte=12, fecha_inicio__hour__lte=18)
        elif periodo_dia == "noche":
            # Noche: 19:00 - 23:59
            query = query.filter(fecha_inicio__hour__gte=19, fecha_inicio__hour__lte=23)
    
    # Filtrar por categoría - se aplica a cualquier tipo de consulta si está presente
    # Esto permite combinar filtros (ej: categoría + fecha + hora + precio)
    categoria = parametros.get('categoria')
    if categoria:
        # Aplicar filtro de categoría siempre que esté presente, independientemente del tipo_consulta
        # (si tipo_consulta es 'por_categoria', ya se aplicó arriba, pero no importa aplicarlo de nuevo)
        query = query.filter(categoria=categoria)
    
    # Filtrar por precio máximo (incluye eventos gratuitos) - se aplica a cualquier tipo de consulta
    precio_maximo = parametros.get('precio_maximo')
    if precio_maximo is not None:
        from decimal import Decimal
        precio_max_decimal = Decimal(str(precio_maximo))
        # Incluir eventos gratuitos (precio=0) y eventos con precio <= precio_maximo
        query = query.filter(
            Q(precio=0) | Q(precio__lte=precio_max_decimal)
        )
    
    # REFUERZO FINAL DEL FILTRO DE FECHA: Asegurar que siempre se aplique correctamente
    # Esto garantiza que si hay un parámetro de fecha, siempre se respete, incluso si hubo otros filtros
    fecha_refuerzo = parametros.get('fecha')
    if fecha_refuerzo:
        fecha_ref, granularidad_ref = formatear_fecha(fecha_refuerzo)
        if fecha_ref:
            if granularidad_ref == "mes":
                # Para meses: filtrar SOLO eventos de ese mes específico
                fecha_fin_ref = _primer_dia_siguiente_mes(fecha_ref)
                query = query.filter(fecha_inicio__gte=fecha_ref, fecha_inicio__lt=fecha_fin_ref)
            else:
                # Para fechas específicas: filtrar solo ese día
                fecha_fin_ref = fecha_ref + timedelta(days=1)
                query = query.filter(fecha_inicio__gte=fecha_ref, fecha_inicio__lt=fecha_fin_ref)
    
    # También verificar fecha_inicio para refuerzo
    if not fecha_refuerzo:
        fecha_inicio_ref = parametros.get('fecha_inicio')
        if fecha_inicio_ref:
            fecha_inicio_ref_parsed, granularidad_inicio_ref = formatear_fecha(fecha_inicio_ref)
            if fecha_inicio_ref_parsed:
                fecha_fin_ref_param = parametros.get('fecha_fin')
                if fecha_fin_ref_param:
                    # Rango de fechas
                    fecha_fin_ref_parsed, granularidad_fin_ref = formatear_fecha(fecha_fin_ref_param)
                    if fecha_fin_ref_parsed:
                        if granularidad_fin_ref == "mes":
                            fecha_fin_rango_ref = _primer_dia_siguiente_mes(fecha_fin_ref_parsed)
                        else:
                            fecha_fin_rango_ref = fecha_fin_ref_parsed + timedelta(days=1)
                        query = query.filter(fecha_inicio__gte=fecha_inicio_ref_parsed, fecha_inicio__lt=fecha_fin_rango_ref)
                elif granularidad_inicio_ref == "mes":
                    # Solo mes de inicio: filtrar solo ese mes
                    fecha_fin_rango_ref = _primer_dia_siguiente_mes(fecha_inicio_ref_parsed)
                    query = query.filter(fecha_inicio__gte=fecha_inicio_ref_parsed, fecha_inicio__lt=fecha_fin_rango_ref)
    
    # Ordenar por fecha de inicio
    query = query.order_by('fecha_inicio')
    
    return query


def formatear_respuesta_eventos(eventos, parametros):
    """
    Formatea los eventos encontrados en una respuesta amigable usando Gemini.
    """
    # Manejar tanto QuerySets como listas
    if hasattr(eventos, 'exists'):
        # Es un QuerySet
        if not eventos.exists():
            return "No encontré eventos que coincidan con tu búsqueda. ¿Podrías intentar con otros criterios?", []
    else:
        # Es una lista u otra estructura iterable
        if not eventos or len(eventos) == 0:
            return "No encontré eventos que coincidan con tu búsqueda. ¿Podrías intentar con otros criterios?", []
    
    # Preparar información de eventos para Gemini
    eventos_info = []
    for evento in eventos:
        # Convertir la fecha de UTC a la zona horaria local antes de formatear
        fecha_inicio = timezone.localtime(evento.fecha_inicio)
        eventos_info.append({
            'titulo': evento.titulo,
            'descripcion': evento.descripcion[:200],  # Limitar descripción
            'fecha': fecha_inicio.strftime('%d/%m/%Y %H:%M'),
            'ubicacion': evento.ubicacion,
            'precio': 'Gratis' if evento.es_gratuito else f'${evento.precio}',
            'categoria': evento.get_categoria_display()
        })
    
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    # Detectar si hay criterios específicos para hacer la respuesta más bromista
    tiene_criterios = any([
        parametros.get('fecha'),
        parametros.get('fecha_inicio'),
        parametros.get('fecha_fin'),
        parametros.get('categoria'),
        parametros.get('ubicacion'),
        parametros.get('solo_gratuitos'),
        parametros.get('precio_maximo'),
        parametros.get('dias_proximos'),
        parametros.get('texto_busqueda')
    ])
    
    criterio_contexto = ""
    if parametros.get('precio_maximo'):
        criterio_contexto = f"El usuario buscó eventos de menos de ${parametros.get('precio_maximo')} dólares (los eventos gratuitos también cuentan)."
    elif parametros.get('solo_gratuitos'):
        criterio_contexto = "El usuario buscó eventos gratuitos."
    elif parametros.get('categoria'):
        criterio_contexto = f"El usuario buscó eventos de {parametros.get('categoria')}."
    
    prompt = f"""Eres un asistente amigable que informa sobre eventos en la ciudad de Loja, Ecuador.
El usuario hizo la siguiente consulta y encontré {len(eventos_info)} evento(s).
{criterio_contexto if criterio_contexto else ""}

Información de los eventos:
{json.dumps(eventos_info, ensure_ascii=False, indent=2)}

Genera una respuesta CORTA, PERSONAL, DESCRIPTIVA y con un toque de broma cuando hay criterios específicos:
1. Si hay 1 evento: Di algo como "Mmm, te recomiendo este evento, se ve que va a estar chevere" o "Este evento se ve interesante, te lo recomiendo"
2. Si hay varios eventos: Menciona brevemente que encontraste varios y que se ven cheveres
3. Si hay criterios específicos (precio, categoría, etc.): Puedes bromear un poco de forma amigable, por ejemplo:
   - Si buscó eventos baratos/precio máximo: "Mmm, encontré una lista de eventos que van a hacer que no te quede chiro daño" o "Encontré varios eventos que no te van a dejar en la quiebra"
   - Si buscó eventos gratuitos: "Encontré eventos que no te van a costar ni un centavo"
   - Si buscó por categoría: "Encontré varios eventos de [categoría] que se ven cheveres"
4. Usa palabras DESCRIPTIVAS sobre la actividad del evento (ej: "se ve entretenido", "va a estar genial", "suena interesante", "parece divertido", etc.)
5. Sé entusiasta pero natural, máximo 1-2 frases cortas
6. NO repitas información que ya está en las tarjetas (fecha, ubicación, precio)
7. NO digas "dime si quieres más info" - eso es implícito

JERGA LOJANA SUTIL (usa de forma natural):
- "Chevere" o "chévere" (genial, bueno)
- "Mmm" al inicio para pensar
- "Se ve que va a estar..." (expresión de expectativa positiva)
- "No más" al final ocasionalmente
- "Chiro daño" (mucho dinero/gasto) - ejemplo: "no te va a quedar chiro daño"
- "Quiebra" (sin dinero) - ejemplo: "no te va a dejar en la quiebra"

IMPORTANTE:
- Responde SOLO con 1-2 frases cortas y naturales
- Si hay criterios específicos, puedes bromear un poco de forma amigable
- Usa palabras descriptivas sobre la actividad (entretenido, genial, interesante, divertido, emocionante, etc.)
- Sé personal y entusiasta, como si le estuvieras recomendando a un amigo
- NO uses formato markdown, solo texto natural
- NO repitas información técnica que ya está en las tarjetas

Ejemplos de buenas respuestas:
- Sin criterios: "Mmm, te recomiendo este evento, se ve que va a estar chevere. Revisa la tarjeta para más detalles."
- Con precio máximo: "Mmm, encontré una lista de eventos que van a hacer que no te quede chiro daño. Revisa las tarjetas."
- Con varios eventos: "Encontré varios eventos que se ven interesantes. Te muestro las tarjetas."
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip(), eventos_info
    except Exception as e:
        # Fallback: respuesta simple si Gemini falla
        respuesta = (
            f"Encontré {len(eventos_info)} evento(s). "
            "Te muestro las tarjetas con los detalles; dime si quieres que profundice en alguno."
        )
        return respuesta, eventos_info


def generar_respuesta_recomendacion(evento, mensaje_usuario):
    """
    Genera una respuesta personalizada para recomendaciones de eventos,
    tomando en cuenta el contexto del mensaje del usuario.
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    fecha_inicio = timezone.localtime(evento.fecha_inicio)
    precio_texto = "Gratis" if evento.es_gratuito else f"${evento.precio}"
    ubicacion_texto = evento.ubicacion or "Ubicación por confirmar"
    
    prompt = f"""Eres un asistente amigable que recomienda eventos en la ciudad de Loja, Ecuador.
El usuario dijo: "{mensaje_usuario}"

Y le vas a recomendar este evento:
- Título: {evento.titulo}
- Categoría: {evento.get_categoria_display()}
- Descripción: {evento.descripcion or 'Sin descripción'}
- Fecha: {fecha_inicio.strftime('%d/%m/%Y a las %H:%M')}
- Ubicación: {ubicacion_texto}
- Precio: {precio_texto}

Genera una respuesta CORTA, PERSONAL y RELEVANTE (máximo 2 frases) que:
1. Tome en cuenta el contexto del mensaje del usuario (si dice que está aburrida, menciona que el evento la ayudará a no aburrirse; si dice que busca algo divertido, menciona que será divertido, etc.)
2. Use palabras descriptivas sobre la actividad (entretenido, genial, interesante, divertido, emocionante, etc.)
3. Sea entusiasta pero natural, como recomendando a un amigo
4. NO repitas toda la información técnica (fecha, ubicación, precio) - eso ya está en la tarjeta
5. Usa jerga lojana sutil (chevere, no más, mmm)

JERGA LOJANA SUTIL:
- "Chevere" o "chévere" (genial, bueno)
- "Mmm" al inicio para pensar
- "Se ve que va a estar..." (expresión de expectativa positiva)
- "No más" al final ocasionalmente

IMPORTANTE:
- Responde SOLO con 1-2 frases cortas y naturales
- Conecta el evento con el contexto del mensaje del usuario (si está aburrida, si busca algo específico, etc.)
- Sé personal y entusiasta
- NO uses formato markdown, solo texto natural
- NO repitas información técnica que ya está en la tarjeta

Ejemplos de buenas respuestas según contexto:
- Si dice "estoy aburrida": "Mmm, este evento se ve que va a estar chevere y te va a ayudar a no aburrirte. Revisa la tarjeta."
- Si dice "busco algo divertido": "Te recomiendo este evento, se ve súper divertido. Mira los detalles en la tarjeta."
- Si solo pide recomendación: "Mmm, te recomiendo este evento, se ve interesante. Revisa la tarjeta para más detalles."

Responde SOLO con el texto, sin explicaciones adicionales.
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        # Fallback: respuesta simple si Gemini falla
        return f"¡Claro mijo! Te recomiendo el {evento.titulo}. Se ve que va a estar chevere. Revisa la tarjeta para más detalles."


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
3. Usa jerga lojana sutil (no más, chevere, vaya) de forma natural

IMPORTANTE:
- Máximo una línea de respuesta
- Responde de forma amigable y natural con jerga lojana sutil
- Siempre termina redirigiendo a eventos
- No uses markdown, solo texto natural
- Usa expresiones como "no más", "chevere" de forma sutil

Ejemplos de respuestas:
- "No tengo esa información, pero puedo ayudarte a encontrar eventos en Loja. ¿Qué tipo de eventos te interesan?"
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

