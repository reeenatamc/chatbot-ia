# 🎉 CantaClaro - Chatbot de Eventos en Loja

**CantaClaro** es un asistente virtual inteligente diseñado para ayudar a los usuarios a encontrar información sobre eventos en la ciudad de Loja, Ecuador. Utiliza Google Gemini para interpretar consultas en lenguaje natural y proporciona respuestas amigables con jerga lojana, combinando búsqueda inteligente con una interfaz visual moderna.

---

## 📋 Tabla de Contenidos

- [¿Qué es CantaClaro?](#qué-es-cantaclaro)
- [Características Principales](#características-principales)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Funcionalidades Detalladas](#funcionalidades-detalladas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [API y Endpoints](#api-y-endpoints)
- [Administración](#administración)
- [Comandos de Gestión](#comandos-de-gestión)
- [Troubleshooting](#troubleshooting)

---

## 🎯 ¿Qué es CantaClaro?

CantaClaro es un chatbot conversacional especializado en eventos de la ciudad de Loja que:

- **Interpreta lenguaje natural**: Entiende preguntas en español coloquial usando Google Gemini
- **Busca eventos inteligentemente**: Filtra por fecha, categoría, precio, ubicación, hora, etc.
- **Combina múltiples filtros**: Permite búsquedas complejas como "eventos de teatro el 7 de diciembre a partir de las 5pm que cuesten menos de 10 dólares"
- **Muestra eventos visualmente**: Tarjetas interactivas con información completa e integración de Google Maps
- **Tiene personalidad local**: Usa jerga lojana ("mijo", "ñaño", "chévere") para crear una experiencia más cercana

---

## ✨ Características Principales

### 🎨 Interfaz de Usuario

- **Pantalla de bienvenida animada**: Video de introducción con diseño "liquid glass"
- **Diseño moderno**: Efectos visuales avanzados con glassmorphism, gradientes animados y bordes translúcidos
- **Tarjetas de eventos interactivas**:
  - Altura uniforme para consistencia visual
  - Integración de Google Maps embebido debajo de cada tarjeta
  - Efectos hover con animaciones suaves
  - Chips de precio y categoría con gradientes animados
  - Lazy loading con Intersection Observer
- **Input animado**: Campo de texto con efectos de borde rotativo, gradientes cónicos y animación "pop" en el ícono de búsqueda
- **Scrollbar personalizado**: Diseño interno con gradientes para mejor estética
- **Responsive**: Diseño adaptable a diferentes tamaños de pantalla

### 🧠 Capacidades del Chatbot

- **Interpretación de lenguaje natural**: Usa Google Gemini para extraer parámetros de consultas complejas
- **Búsqueda multi-criterio**: Filtra por fecha, categoría, precio, ubicación, hora y período del día simultáneamente
- **Paginación inteligente**: Muestra 6 eventos por página con botón "Cargar más"
- **Preguntas frecuentes (FAQ)**: Acceso rápido a consultas comunes sin consumir API de Gemini
- **Recomendaciones personalizadas**: Sugiere eventos aleatorios cuando se solicita
- **Detalles de eventos**: Información completa al hacer clic en una tarjeta
- **Manejo de despedidas**: Sistema de confirmación para salir del chat con mensaje de despedida

### 🗄️ Sistema de Datos

- **Modelo completo de eventos**: Campos para título, descripción, categoría, fechas, ubicación, precio, imagen, contacto, enlaces
- **Filtrado automático**: Excluye eventos pasados automáticamente (excepto cuando se busca específicamente una fecha pasada)
- **Gestión de estado**: Campo `activo` para mostrar/ocultar eventos
- **Índices optimizados**: Para búsquedas rápidas por fecha, categoría y estado

---

## 🔧 Requisitos

- **Python**: 3.8 o superior
- **Django**: 5.2.8
- **Base de datos**: SQLite (incluido) o PostgreSQL (recomendado para producción)
- **Google Gemini API Key**: Para procesamiento de lenguaje natural
- **Navegador moderno**: Chrome, Firefox, Safari recientes (para efectos CSS avanzados)

---

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/chatbot-ia.git
cd chatbot-ia
```

### 2. Crear un entorno virtual

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

```bash
python manage.py migrate
```

### 5. Crear un superusuario

```bash
python manage.py createsuperuser
```

### 6. (Opcional) Poblar la base de datos con eventos de prueba

```bash
python manage.py poblar_eventos
```

---

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto o configura directamente en `config/settings.py`:

```python
# Google Gemini API Key
GEMINI_API_KEY = 'tu-api-key-aqui'
```

**Cómo obtener una API Key de Google Gemini:**
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Crea una nueva API Key
4. Copia la clave y agrégala a tu configuración

### Configuración de Django

El proyecto está configurado para:
- **Django Unfold**: Interfaz de administración moderna
- **Timezone**: Configurado para Ecuador (America/Guayaquil)
- **Idioma**: Español (es-es)
- **Static Files**: Archivos estáticos en `static/` y `chatbot/static/`
- **Media Files**: Archivos subidos en `media/`

---

## 🚀 Uso

### Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

Luego abre tu navegador en `http://127.0.0.1:8000/`

### Acceder al panel de administración

1. Ve a `http://127.0.0.1:8000/admin/`
2. Inicia sesión con las credenciales del superusuario
3. Gestiona eventos desde la sección "Eventos"

---

## 💬 Funcionalidades Detalladas

### Tipos de Consultas Soportadas

#### 1. Consultas por Fecha

- **Fechas específicas**: "eventos del 15 de noviembre", "eventos el 7 de diciembre"
- **Fechas relativas**: "eventos de hoy", "eventos de mañana", "eventos de esta semana"
- **Rangos de fechas**: "eventos entre el 15 y el 20 de noviembre"
- **Por mes**: "eventos en noviembre", "eventos de diciembre"
- **Próximos eventos**: "próximos eventos", "eventos próximos"

#### 2. Consultas por Categoría

- **Categorías específicas**: música, teatro, deporte, cultural, gastronomía, educativo, religioso, feria, danza
- **Consultas amplias**: "artes vivas" busca en teatro, danza y música
- **Múltiples categorías**: "eventos de música o teatro"

#### 3. Consultas por Precio

- **Eventos gratuitos**: "eventos gratis", "eventos gratuitos"
- **Precio máximo**: "eventos que cuesten menos de 20 dólares", "eventos hasta $15"
- **Combinado**: Los eventos gratuitos siempre se incluyen cuando se busca por precio máximo

#### 4. Consultas por Hora/Período del Día

- **Hora específica**: "eventos a las 8pm", "eventos a las 2 de la tarde"
- **Rango de horas**: "eventos entre las 7 y las 9 pm", "eventos de 5pm a 8pm"
- **Períodos del día**: "eventos en la mañana", "eventos de la tarde", "eventos nocturnos"

#### 5. Consultas por Ubicación

- **Lugares específicos**: "eventos en el Teatro Bolívar", "eventos en el Parque Central"
- **Búsqueda flexible**: Busca en nombres de ubicación y direcciones

#### 6. Consultas Combinadas

**Ejemplos de búsquedas complejas soportadas:**

- "eventos de teatro el 7 de diciembre a partir de las 5pm que cuesten menos de 10 dólares"
- "eventos de música o similares en noviembre solo en la tarde"
- "eventos de música del 15 de noviembre a las 8 pm"
- "eventos gratuitos de este mes en la mañana"

#### 7. Recomendaciones

- **"Recomiéndame un evento"**: Devuelve un evento aleatorio activo
- **"¿Qué evento me recomiendas?"**: Sugerencia personalizada con respuesta contextual
- **"Me recomiendas algo"**: Recomendación casual

#### 8. Información Detallada

- **"Dame más información sobre [nombre del evento]"**: Muestra todos los detalles del evento
- Incluye: fecha completa, ubicación con dirección, descripción, precio, categoría, contacto y enlaces

#### 9. Búsquedas Generales

- **Búsqueda por texto**: "eventos de rock", "festivales", "conciertos"
- Busca en títulos y descripciones de eventos

### Sistema de Respuestas

- **Tono amigable**: Usa jerga lojana ("mijo", "ñaño", "chévere") de forma natural
- **Respuestas contextuales**: Adapta el mensaje según el tipo de consulta
- **Bromas sutiles**: Cuando hay criterios específicos (ej: precio), puede hacer bromas amigables
- **Manejo de errores**: Mensajes amigables cuando no se encuentran eventos

### Características de la Interfaz

#### Pantalla de Bienvenida
- Video de introducción que se reproduce automáticamente
- Botón "Repetir" para reiniciar el video
- Botón "Equipo" para ver información del proyecto
- Botón "Comenzar" con animación para iniciar el chat

#### Pantalla de Chat
- Mensaje de bienvenida con GIF animado
- Píldoras FAQ que desaparecen al enviar un mensaje
- Input con efectos animados avanzados:
  - Bordes rotativos con gradientes cónicos
  - Efecto "pop" en el ícono de búsqueda al hacer focus
  - Múltiples capas de efectos visuales
- Botón de envío con GIF animado
- Scrollbar personalizado con gradientes

#### Tarjetas de Eventos
- **Diseño uniforme**: Todas las tarjetas tienen la misma altura (380px + 100px de mapa)
- **Información visible**:
  - Chips de precio y categoría en la parte superior
  - Fecha formateada en español (ej: "25 de noviembre de 2025, 7:30 PM")
  - Título del evento
  - Ubicación
  - Descripción truncada (máximo 140 caracteres)
- **Mapa integrado**: Google Maps embebido debajo de cada tarjeta mostrando la ubicación
- **Interactividad**: Click en la tarjeta para ver más información
- **Animaciones**: Aparecen con efecto fade-in al hacer scroll
- **Paginación**: Botón "Cargar más" para ver más eventos (6 por página)

#### Sistema de Despedida
- Detección automática de intenciones de salida
- Confirmación con botones "Continuar" y "Salir"
- Mensaje de despedida personalizado
- Transición suave de vuelta a la pantalla de bienvenida

---

## 📁 Estructura del Proyecto

```
chatbot-ia/
├── chatbot/                          # App principal del chatbot
│   ├── management/
│   │   └── commands/
│   │       ├── poblar_eventos.py     # Comando para crear eventos de prueba
│   │       └── eliminar_eventos_pasados.py  # Comando para limpiar eventos pasados
│   ├── migrations/                   # Migraciones de base de datos
│   ├── static/
│   │   └── chatbot/
│   │       ├── css/
│   │       │   └── style.css         # Estilos principales (2389 líneas)
│   │       ├── js/
│   │       │   └── main.js           # Lógica del frontend (938 líneas)
│   │       └── images/               # Imágenes del chatbot
│   ├── templates/
│   │   └── chatbot/
│   │       └── index.html            # Template principal (220 líneas)
│   ├── admin.py                      # Configuración del admin Django
│   ├── evento_queries.py             # Lógica de consultas con Gemini (879 líneas)
│   ├── models.py                     # Modelo Evento (96 líneas)
│   ├── views.py                      # Vistas del chatbot (302 líneas)
│   └── urls.py                       # URLs del chatbot
├── config/                           # Configuración de Django
│   ├── settings.py                   # Configuración principal
│   ├── urls.py                       # URLs principales
│   ├── wsgi.py                       # WSGI config
│   └── asgi.py                       # ASGI config
├── static/                           # Archivos estáticos globales
│   ├── videos/                       # Videos del proyecto
│   └── images/                       # Imágenes globales
├── media/                            # Archivos subidos por usuarios
│   └── eventos/                      # Imágenes de eventos
├── manage.py                         # Script de gestión de Django
├── requirements.txt                  # Dependencias Python
├── db.sqlite3                        # Base de datos SQLite (desarrollo)
└── README.md                         # Este archivo
```

### Archivos Principales

#### Backend
- **`chatbot/models.py`**: Define el modelo `Evento` con todos los campos necesarios
- **`chatbot/views.py`**: Maneja las peticiones HTTP y la lógica de negocio principal
- **`chatbot/evento_queries.py`**: Contiene la lógica de interpretación de consultas y búsqueda de eventos
  - `interpretar_consulta_usuario()`: Usa Gemini para extraer parámetros
  - `ejecutar_consulta_eventos()`: Ejecuta búsquedas en la base de datos
  - `formatear_respuesta_eventos()`: Genera respuestas amigables con Gemini
- **`chatbot/admin.py`**: Configuración del panel de administración con Django Unfold

#### Frontend
- **`chatbot/templates/chatbot/index.html`**: Estructura HTML principal
- **`chatbot/static/chatbot/js/main.js`**: Lógica JavaScript
  - Gestión del chat y mensajes
  - Creación de tarjetas de eventos
  - Integración con Google Maps
  - Paginación y "Cargar más"
  - Sistema de despedida
- **`chatbot/static/chatbot/css/style.css`**: Estilos CSS con efectos avanzados
  - Glassmorphism y efectos "liquid glass"
  - Animaciones de bordes con gradientes cónicos
  - Estilos de tarjetas con múltiples capas
  - Input animado con efectos complejos

---

## 🔑 Tecnologías Utilizadas

### Backend
- **Django 5.2.8**: Framework web de Python
- **Django Unfold 0.71.0**: Interfaz de administración moderna
- **Google Gemini API (google-genai 1.50.0)**: Procesamiento de lenguaje natural
- **SQLite**: Base de datos (desarrollo), PostgreSQL recomendado para producción
- **Pillow 12.0.0**: Procesamiento de imágenes

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos avanzados con:
  - Glassmorphism (`backdrop-filter`)
  - Gradientes cónicos animados (`conic-gradient`)
  - Custom Properties con `@property` para animaciones
  - Transiciones y transformaciones
- **JavaScript (Vanilla)**: Sin frameworks, JavaScript puro
- **Google Fonts (Poppins)**: Tipografía moderna
- **Google Maps Embed**: Mapas embebidos sin API key

### Características CSS Avanzadas
- **Glassmorphism**: Efecto "liquid glass" con `backdrop-filter: blur()`
- **Gradientes animados**: `conic-gradient` con rotaciones en múltiples capas
- **Custom Properties**: Variables CSS con `@property` para animaciones suaves
- **Intersection Observer**: Para lazy loading y animaciones al scroll
- **Scrollbar personalizado**: Estilos webkit y estándar para scrollbars internos

---

## 🔌 API y Endpoints

### POST `/api/chat/`

Endpoint principal para la comunicación con el chatbot.

**Request Body:**
```json
{
  "message": "eventos de música en noviembre",
  "offset": 0
}
```

**Response Success:**
```json
{
  "response": "Mmm, encontré varios eventos de música...",
  "events": [
    {
      "titulo": "Concierto de Rock Nacional",
      "descripcion": "Los mejores grupos...",
      "fecha": "26/11/2025 14:00",
      "ubicacion": "Coliseo Ciudad de Loja",
      "precio": "$25.00",
      "categoria": "Música"
    }
  ],
  "has_more": true,
  "total_events": 12
}
```

**Response Error:**
```json
{
  "error": "Error al procesar la solicitud: [descripción]"
}
```

**Parámetros:**
- `message` (string, requerido): Mensaje del usuario
- `offset` (integer, opcional): Offset para paginación (default: 0)

**Casos especiales:**
- Si `offset > 0`: Solo retorna eventos, sin respuesta de texto
- Si `confirm_exit: true`: Indica que debe mostrar botones de confirmación

---

## 🛠️ Administración

### Panel de Administración

Accede en `http://127.0.0.1:8000/admin/` con credenciales de superusuario.

#### Gestión de Eventos

**Campos del modelo Evento:**
- **Título** (CharField, 200 caracteres): Nombre del evento
- **Descripción** (TextField): Detalles completos del evento
- **Categoría** (CharField con choices): Música, Deporte, Cultural, Gastronomía, Educativo, Religioso, Feria, Teatro, Danza, Otro
- **Fecha de inicio** (DateTimeField): Fecha y hora cuando comienza
- **Fecha de fin** (DateTimeField, opcional): Fecha y hora cuando termina
- **Ubicación** (CharField, 200 caracteres): Nombre del lugar
- **Dirección** (TextField, opcional): Dirección completa
- **Precio** (DecimalField): Costo (0.00 para eventos gratuitos)
- **Imagen** (ImageField, opcional): Imagen del evento
- **Contacto** (CharField, opcional): Teléfono, email, etc.
- **Enlace** (URLField, opcional): URL adicional
- **Activo** (BooleanField): Checkbox para mostrar/ocultar el evento

**Funcionalidades del Admin:**
- Filtros por categoría, estado, fecha de inicio, fecha de creación
- Búsqueda en título, descripción y ubicación
- Jerarquía de fechas para navegación rápida
- Acción personalizada: "Eliminar eventos pasados"
- Vista de solo lectura para fecha_creacion y fecha_actualizacion

---

## 🎮 Comandos de Gestión

### Poblar base de datos con eventos de prueba

```bash
python manage.py poblar_eventos
```

Crea una variedad de eventos de prueba con diferentes:
- Fechas (después del 25 de noviembre de 2025)
- Categorías (todas las disponibles)
- Precios (gratuitos y pagos)
- Ubicaciones (lugares reales de Loja)
- Horarios diversos

### Eliminar eventos pasados

```bash
# Ver qué se eliminaría (sin eliminar)
python manage.py eliminar_eventos_pasados --dry-run

# Eliminar todos los eventos pasados
python manage.py eliminar_eventos_pasados

# Eliminar eventos pasados hace más de 30 días
python manage.py eliminar_eventos_pasados --dias 30

# Ver eventos pasados hace más de 7 días (sin eliminar)
python manage.py eliminar_eventos_pasados --dias 7 --dry-run
```

**Nota:** El sistema también filtra automáticamente eventos pasados en las consultas del chatbot, excepto cuando se busca específicamente una fecha pasada.

---

## 🐛 Troubleshooting

### El video no se reproduce automáticamente

Los navegadores bloquean autoplay por defecto. El sistema intenta reproducir el video en múltiples eventos de interacción. Si no funciona, haz clic en el botón "Repetir".

### No aparecen eventos

1. Verifica que hay eventos activos en el admin (`activo=True`)
2. Revisa que las fechas de los eventos no sean pasadas (se filtran automáticamente)
3. Asegúrate de ejecutar las migraciones: `python manage.py migrate`

### La API de Gemini no funciona

1. Verifica que `GEMINI_API_KEY` está configurada en `config/settings.py`
2. Revisa que la API Key es válida
3. Verifica tu cuota de uso en [Google AI Studio](https://makersuite.google.com/app/apikey)
4. Revisa los logs del servidor para errores específicos

### Los estilos no se cargan

1. Ejecuta `python manage.py collectstatic` (en producción)
2. Verifica que `STATIC_URL` y `STATIC_ROOT` están configurados
3. Revisa la consola del navegador para errores 404
4. Limpia la caché del navegador

### Los mapas no se muestran

1. Verifica que los eventos tienen `ubicacion` definida
2. Revisa la consola del navegador por errores de iframe
3. Asegúrate de que no hay bloqueadores de contenido activos
4. Los mapas usan Google Maps Embed (sin API key), verifica conectividad a internet

### El filtrado de fechas no funciona correctamente

El sistema filtra automáticamente eventos pasados EXCEPTO cuando:
- Se busca una fecha específica pasada (ej: "eventos del 15 de noviembre" cuando ya pasó)
- Se busca un rango de fechas que incluye fechas pasadas

Si necesitas mostrar eventos pasados, busca específicamente por esa fecha.

### Problemas de paginación

- Verifica que `has_more` está siendo retornado correctamente
- Revisa que el offset se está enviando en las peticiones
- Asegúrate de que hay más de 6 eventos en la consulta

---

## 📝 Notas Adicionales

### Sobre el Diseño

- El diseño usa efectos visuales modernos que requieren navegadores actualizados
- El efecto "liquid glass" usa `backdrop-filter` que puede no funcionar en navegadores antiguos
- Los gradientes cónicos animados requieren soporte para `@property` y animaciones CSS avanzadas
- Las tarjetas tienen altura fija (380px + 100px mapa) para mantener uniformidad visual

### Sobre las Consultas

- El chatbot entiende variaciones de las mismas preguntas gracias a Gemini
- Puede interpretar fechas relativas ("hoy", "mañana", "esta semana") y absolutas
- Maneja errores gracefully con mensajes amigables
- Las preguntas frecuentes (FAQ) se procesan directamente sin usar Gemini para optimizar costos

### Optimizaciones

- **FAQ directas**: Consultas comunes van directamente a la base de datos sin pasar por Gemini
- **Paginación**: Solo se generan respuestas de Gemini en la primera carga (offset=0)
- **Lazy loading**: Mapas y tarjetas se cargan solo cuando son visibles
- **Filtrado automático**: Eventos pasados se excluyen automáticamente de las búsquedas

### Mantenimiento

- **Limpieza periódica**: Usa el comando o acción del admin para eliminar eventos pasados
- **Backups**: Realiza backups regulares de la base de datos
- **Actualizaciones**: Mantén Django y las dependencias actualizadas
- **Monitoreo de API**: Revisa el uso de la API de Gemini para controlar costos

---

## 👥 Equipo

Este proyecto fue desarrollado por:
- **Renata Maldonado** - Desarrollo Principal
- **Juan David Garcia** - Colaborador
- **Renato Rojas** - Colaborador

---

## 📄 Licencia

MIT

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📧 Contacto

Para preguntas o sugerencias, contacta al equipo de desarrollo.

---

**CantaClaro** - Tu asistente de eventos en Loja 🎉

*Versión: 1.0.0 | Última actualización: Diciembre 2025*
