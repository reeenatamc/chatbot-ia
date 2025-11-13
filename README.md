# CantaClaro - Chatbot de Eventos en Loja

CantaClaro es un asistente virtual inteligente diseñado para ayudar a los usuarios a encontrar información sobre eventos en la ciudad de Loja, Ecuador. Utiliza Google Gemini para interpretar consultas en lenguaje natural y proporciona respuestas amigables con jerga lojana.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Interfaz de Usuario](#interfaz-de-usuario)
- [Capacidades del Chatbot](#capacidades-del-chatbot)
- [Administración](#administración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)

## ✨ Características

- **Interfaz moderna y atractiva**: Diseño "liquid glass" con efectos visuales animados
- **Búsqueda inteligente de eventos**: Interpreta consultas en lenguaje natural usando Google Gemini
- **Múltiples criterios de búsqueda**: Por fecha, categoría, ubicación, precio, etc.
- **Tarjetas interactivas**: Visualización de eventos en formato de tarjetas con animaciones
- **Jerga lojana**: Respuestas personalizadas con expresiones locales
- **Panel de administración**: Gestión fácil de eventos con Django Unfold
- **Responsive**: Diseño adaptable a diferentes tamaños de pantalla

## 🔧 Requisitos

- Python 3.8 o superior
- Django 4.2 o superior
- PostgreSQL (recomendado) o SQLite
- Google Gemini API Key
- Node.js y npm (para assets estáticos, opcional)

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

### 6. Poblar la base de datos con eventos de prueba (opcional)

```bash
python manage.py poblar_eventos
```

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto o configura las siguientes variables en `config/settings.py`:

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

El proyecto está configurado para usar:
- **Django Unfold**: Para una interfaz de administración moderna
- **Timezone**: Configurado para Ecuador (America/Guayaquil)
- **Static Files**: Archivos estáticos en `static/` y `chatbot/static/`

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

## 🎨 Interfaz de Usuario

### Pantalla de Bienvenida

Al abrir CantaClaro, verás:

1. **Título**: "CantaClaro tu asistente de eventos"
2. **Video de introducción**: Se reproduce automáticamente al cargar
3. **Botones de control**:
   - **Repetir**: Reinicia el video de introducción
   - **Equipo**: Muestra información sobre el equipo de desarrollo
4. **Botón "Comenzar"**: Inicia la conversación con el chatbot

### Pantalla de Chat

Una vez que haces clic en "Comenzar":

1. **Mensaje de bienvenida**: El bot saluda con "Hola mijo como te puedo ayudar hoy"
2. **Preguntas frecuentes (FAQ)**: Píldoras interactivas con preguntas comunes
3. **Área de chat**: Donde aparecen los mensajes y respuestas
4. **Input de mensaje**: Campo de texto con botones de micrófono y envío
5. **Tarjetas de eventos**: Los eventos se muestran como tarjetas interactivas con:
   - Categoría y precio (tags)
   - Fecha y hora formateada
   - Título del evento
   - Ubicación
   - Imagen (si está disponible)

### Características Visuales

- **Efecto "Liquid Glass"**: Bordes translúcidos con blur y gradientes animados
- **Bordes animados**: Rotación de gradientes rojo-azul en tarjetas y contenedores
- **Burbujas de chat estilo iOS**: Mensajes con colas y fondos translúcidos
- **Animaciones suaves**: Transiciones y efectos al cargar contenido
- **Lazy loading**: Las tarjetas aparecen con animación al hacer scroll

## 💬 Capacidades del Chatbot

### Tipos de Consultas Soportadas

#### 1. Consultas por Fecha

- **"¿Qué eventos hay hoy?"**
- **"Eventos de mañana"**
- **"Eventos del 15 de noviembre"**
- **"Eventos en noviembre"**
- **"Eventos entre el 15 y el 20 de noviembre"**
- **"Eventos de esta semana"**
- **"Próximos eventos"**

#### 2. Consultas por Categoría

- **"Eventos de música"**
- **"Eventos de teatro"**
- **"Eventos deportivos"**
- **"Eventos culturales"**
- **"Eventos de gastronomía"**
- **"Eventos educativos"**
- **"Eventos religiosos"**
- **"Ferias"**
- **"Eventos de danza"**

#### 3. Consultas por Conceptos Amplios

- **"¿Qué actividades puedo realizar en artes vivas?"**
  - Busca en múltiples categorías relacionadas (teatro, danza, música)
- **"Eventos de espectáculos"**
- **"Actividades culturales"**

#### 4. Consultas por Precio

- **"Eventos gratuitos"**
- **"Eventos que cuesten menos de 20 dólares"**
- **"Eventos hasta $15"**
- **"Eventos de menos de 10 dólares"**

#### 5. Consultas por Ubicación

- **"Eventos en el Parque Central"**
- **"Eventos en el Teatro Bolívar"**
- **"Eventos en Jipiro"**

#### 6. Recomendaciones

- **"Recomiéndame un evento"**
- **"¿Qué evento me recomiendas?"**
- **"Me recomiendas algo"**
- **"Estoy aburrida, recomiéndame algo"**

#### 7. Información Detallada

- **"Dame más información sobre [nombre del evento]"**
  - Muestra detalles completos: fecha, hora, ubicación, descripción, precio, contacto, enlaces

#### 8. Búsquedas Generales

- **"Eventos de rock"**
- **"Festivales"**
- **"Conciertos"**

### Ejemplos de Interacción

```
Usuario: "¿Qué eventos hay hoy?"
Bot: "Mmm, encontré varios eventos cheveres para hoy. Aquí te dejo las tarjetas..."

Usuario: "Eventos de música que cuesten menos de 15 dólares"
Bot: "Mmm, encontré una lista de eventos de música que van a hacer que no te quede chiro daño..."

Usuario: "Recomiéndame un evento, estoy aburrida"
Bot: "Mmm, este evento se ve que va a estar chevere y te va a ayudar a no aburrirte, pues."
```

### Respuestas del Bot

- **Tono amigable**: Usa jerga lojana ("mijo", "chevere", "pues")
- **Respuestas concisas**: Directas, sin repetir información de las tarjetas
- **Contexto personalizado**: Adapta respuestas según el contexto de la pregunta
- **Fallback**: Si la pregunta no es sobre eventos, redirige amablemente

## 🛠️ Administración

### Panel de Administración (Django Admin)

Accede en `http://127.0.0.1:8000/admin/`

#### Gestión de Eventos

1. **Crear evento**: Click en "Añadir evento"
2. **Editar evento**: Click en el título del evento
3. **Eliminar evento**: Selecciona y usa la acción "Eliminar eventos seleccionados"
4. **Filtros disponibles**:
   - Por categoría
   - Por estado (activo/inactivo)
   - Por fecha de inicio
   - Por fecha de creación

#### Campos del Evento

- **Título**: Nombre del evento
- **Descripción**: Detalles del evento
- **Categoría**: Música, Deporte, Cultural, Gastronomía, Educativo, Religioso, Feria, Teatro, Danza, Otro
- **Fecha de inicio**: Fecha y hora cuando comienza
- **Fecha de fin**: (Opcional) Fecha y hora cuando termina
- **Ubicación**: Nombre del lugar
- **Dirección**: (Opcional) Dirección completa
- **Precio**: Costo (0.00 para eventos gratuitos)
- **Imagen**: (Opcional) Imagen del evento
- **Contacto**: Teléfono, email, etc.
- **Enlace**: (Opcional) URL adicional
- **Activo**: Checkbox para mostrar/ocultar el evento

#### Acciones Disponibles

1. **Eliminar eventos pasados**:
   - Selecciona eventos (o deja sin seleccionar para todos)
   - Elige "Eliminar eventos pasados" en el menú de acciones
   - Click en "Ir"
   - Elimina eventos cuya fecha de inicio ya pasó

### Comandos de Gestión

#### Poblar base de datos con eventos de prueba

```bash
python manage.py poblar_eventos
```

Crea una variedad de eventos de prueba con diferentes fechas, categorías y precios.

#### Eliminar eventos pasados (línea de comandos)

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

## 📁 Estructura del Proyecto

```
chatbot-ia/
├── chatbot/
│   ├── management/
│   │   └── commands/
│   │       ├── poblar_eventos.py          # Comando para crear eventos de prueba
│   │       └── eliminar_eventos_pasados.py # Comando para eliminar eventos pasados
│   ├── migrations/                        # Migraciones de base de datos
│   ├── static/
│   │   └── chatbot/
│   │       ├── css/
│   │       │   └── style.css              # Estilos principales
│   │       ├── js/
│   │       │   └── main.js                # Lógica del frontend
│   │       └── images/                    # Imágenes del chatbot
│   ├── templates/
│   │   └── chatbot/
│   │       └── index.html                 # Template principal
│   ├── admin.py                           # Configuración del admin
│   ├── evento_queries.py                  # Lógica de consultas con Gemini
│   ├── models.py                          # Modelo Evento
│   ├── views.py                           # Vistas del chatbot
│   └── urls.py                            # URLs del chatbot
├── config/
│   ├── settings.py                        # Configuración de Django
│   ├── urls.py                            # URLs principales
│   └── wsgi.py                            # WSGI config
├── static/
│   └── videos/                            # Videos del proyecto
├── manage.py                              # Script de gestión de Django
├── requirements.txt                        # Dependencias Python
└── README.md                              # Este archivo
```

## 🔑 Tecnologías Utilizadas

### Backend

- **Django 4.2+**: Framework web de Python
- **Django Unfold**: Interfaz de administración moderna
- **Google Gemini API**: Procesamiento de lenguaje natural
- **PostgreSQL/SQLite**: Base de datos

### Frontend

- **HTML5**: Estructura
- **CSS3**: Estilos con efectos avanzados (backdrop-filter, conic-gradient, animations)
- **JavaScript (Vanilla)**: Interactividad sin frameworks
- **Google Fonts (Poppins)**: Tipografía

### Características CSS Avanzadas

- **Glassmorphism**: Efecto "liquid glass" con `backdrop-filter`
- **Gradientes animados**: `conic-gradient` con animaciones CSS
- **Custom Properties**: Variables CSS con `@property` para animaciones
- **Intersection Observer**: Para lazy loading y animaciones al scroll

## 🎯 Funcionalidades Técnicas

### Interpretación de Consultas

El sistema usa Google Gemini para:
1. **Extraer parámetros** de la consulta del usuario
2. **Detectar tipo de consulta**: fecha, categoría, precio, ubicación, etc.
3. **Mapear conceptos amplios**: "artes vivas" → teatro, danza, música
4. **Generar respuestas personalizadas**: Con jerga lojana y contexto

### Base de Datos

- **Modelo Evento**: Almacena toda la información de eventos
- **Índices**: Optimizados para búsquedas por fecha, categoría y estado
- **Filtros**: Solo muestra eventos activos en el chatbot

### Seguridad

- **CSRF Protection**: Django protege contra ataques CSRF
- **ORM de Django**: Previene inyecciones SQL
- **Validación de datos**: En modelos y formularios

## 🐛 Solución de Problemas

### El video no se reproduce automáticamente

Los navegadores bloquean autoplay. El sistema intenta reproducir en múltiples eventos. Si no funciona, haz clic en el botón de repetir.

### No aparecen eventos

1. Verifica que hay eventos activos en el admin
2. Revisa que las fechas de los eventos no sean pasadas
3. Asegúrate de que `activo=True` en los eventos

### La API de Gemini no funciona

1. Verifica que `GEMINI_API_KEY` está configurada
2. Revisa que la API Key es válida
3. Verifica tu cuota de uso en Google AI Studio

### Los estilos no se cargan

1. Ejecuta `python manage.py collectstatic`
2. Verifica que `STATIC_URL` y `STATIC_ROOT` están configurados
3. Revisa la consola del navegador para errores

## 📝 Notas Adicionales

### Sobre el Diseño

- El diseño usa un aspecto 16:9 para el contenedor principal
- Los efectos visuales requieren navegadores modernos (Chrome, Firefox, Safari recientes)
- El efecto "liquid glass" usa `backdrop-filter` que puede no funcionar en navegadores antiguos

### Sobre las Consultas

- El chatbot entiende variaciones de las mismas preguntas
- Puede interpretar fechas relativas ("hoy", "mañana", "esta semana")
- Maneja errores gracefully con mensajes amigables

### Mantenimiento

- **Limpieza periódica**: Usa el comando o acción del admin para eliminar eventos pasados
- **Backups**: Realiza backups regulares de la base de datos
- **Actualizaciones**: Mantén Django y las dependencias actualizadas

## 👥 Equipo

Este proyecto fue desarrollado por:
- **Renata Maldonado** (Desarrolladora principal)
- **Juan David Garcia**
- **Renato Rojas**

## 📄 Licencia

MIT

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias, contacta al equipo de desarrollo.

---

**CantaClaro** - Tu asistente de eventos en Loja 🎉

