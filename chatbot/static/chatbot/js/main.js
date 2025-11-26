document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.container');
    const welcomeScreen = document.getElementById('welcomeScreen');
    const chatContainer = document.getElementById('chatContainer');
    const aboutContainer = document.getElementById('aboutContainer');
    const startButton = document.getElementById('startButton');
    const aboutButton = document.getElementById('aboutButton');
    const backToWelcomeButton = document.getElementById('backToWelcomeButton');
    const repeatButton = document.getElementById('repeatButton');
    const welcomeVideo = document.querySelector('.welcome-video');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');

    function isNearBottom() {
        if (!chatMessages) return true;
        const threshold = 120;
        return chatMessages.scrollTop + chatMessages.clientHeight >= chatMessages.scrollHeight - threshold;
    }

    function scrollToBottom() {
        if (!chatMessages) return;
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }

    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.remove('event-card--hidden');
                entry.target.classList.add('event-card--visible');
                cardObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });
    
    // Variables para paginación
    let lastMessage = '';
    let currentOffset = 0;
    let hasMoreEvents = false;
    
    // Reproducir video automáticamente al cargar la pantalla principal
    if (welcomeVideo) {
        const playVideo = () => {
            if (welcomeVideo && welcomeScreen) {
                const computedStyle = window.getComputedStyle(welcomeScreen);
                const isWelcomeVisible = computedStyle.display !== 'none' && 
                                        computedStyle.visibility !== 'hidden' &&
                                        computedStyle.opacity !== '0';
                
                if (isWelcomeVisible) {
                    welcomeVideo.play().catch((error) => {
                        // Autoplay puede estar bloqueado; se reintentará con la interacción del usuario
                    });
                }
            }
        };
        
        // Cuando el video termine, pausarlo en el último frame
        welcomeVideo.addEventListener('ended', () => {
            if (welcomeVideo) {
                welcomeVideo.pause();
                // Asegurarse de que esté en el último frame
                if (welcomeVideo.duration) {
                    welcomeVideo.currentTime = welcomeVideo.duration;
                }
            }
        });
        
        // Intentar reproducir cuando el video esté listo
        welcomeVideo.addEventListener('loadeddata', playVideo, { once: true });
        welcomeVideo.addEventListener('canplay', playVideo, { once: true });
        welcomeVideo.addEventListener('canplaythrough', playVideo, { once: true });
        
        // Intentar después de delays progresivos
        setTimeout(playVideo, 100);
        setTimeout(playVideo, 300);
        
        // Si el autoplay está bloqueado, intentar con cualquier interacción
        const tryPlayOnInteraction = (event) => {
            // No reproducir si el click es en el botón de comenzar
            if (event && event.target && (event.target.id === 'startButton' || event.target.closest('#startButton'))) {
                return;
            }
            playVideo();
        };
        
        // Escuchar múltiples eventos de interacción
        document.addEventListener('click', tryPlayOnInteraction, { once: true });
        document.addEventListener('keydown', tryPlayOnInteraction, { once: true });
        document.addEventListener('touchstart', tryPlayOnInteraction, { once: true });
        document.addEventListener('mousemove', tryPlayOnInteraction, { once: true });
    }

    // Preguntas frecuentes con respuestas quemadas
    const faqQuestions = [
        { text: '¿Qué eventos hay hoy?', query: 'eventos de hoy' },
        { text: '¿Qué eventos hay esta semana?', query: 'eventos de esta semana' },
        { text: '¿Qué eventos hay este mes?', query: 'eventos de este mes' },
        { text: '¿Qué eventos son gratis?', query: 'eventos gratis' },
        { text: '¿Qué eventos hay de música?', query: 'eventos de música' },
        { text: '¿Qué eventos hay de teatro?', query: 'eventos de teatro' }
    ];

    // Función para crear y mostrar las pastillas de preguntas frecuentes
    function hideFaqPills() {
        const faqContainer = document.getElementById('faqPillsContainer');
        if (!faqContainer) return;
        
        // Solo ocultar si está visible
        if (faqContainer.style.display !== 'none') {
            faqContainer.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            faqContainer.style.opacity = '0';
            faqContainer.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                faqContainer.style.display = 'none';
            }, 300);
        }
    }

    function createFaqPills() {
        const faqContainer = document.getElementById('faqPillsContainer');
        if (!faqContainer) return;

        faqContainer.innerHTML = '';
        faqContainer.style.display = 'flex';
        faqContainer.style.opacity = '1';
        faqContainer.style.transform = 'translateY(0)';
        faqQuestions.forEach(faq => {
            const pill = document.createElement('button');
            pill.className = 'faq-pill';
            pill.textContent = faq.text;
            pill.setAttribute('data-query', faq.query);
            pill.addEventListener('click', () => {
                // Ocultar suavemente el contenedor de pastillas
                hideFaqPills();
                // Enviar mensaje mostrando el texto amigable de la pastilla
                sendMessageWithText(faq.query, { displayText: faq.text });
            });
            faqContainer.appendChild(pill);
        });
    }

    // Función para iniciar el chat
    function startChat() {
        // Agregar clase al welcome-screen para activar el efecto de borde
        if (welcomeScreen) {
            welcomeScreen.classList.add('activated');
            
            // Esperar a que termine la animación (1.5s) antes de cambiar de pantalla
            setTimeout(() => {
                // Remover la clase después de la animación
                welcomeScreen.classList.remove('activated');
                
                // Cambiar de pantalla después de la animación
                welcomeScreen.style.display = 'none';
                aboutContainer.style.display = 'none';
                aboutContainer.classList.remove('active');
                chatContainer.style.display = 'flex';
                chatContainer.classList.add('active');
                if (welcomeVideo) {
                    try {
                        welcomeVideo.pause();
                    } catch (error) {
                        console.warn('Error al detener el video:', error);
                    }
                }
                // Crear las pastillas de preguntas frecuentes
                createFaqPills();
            }, 1500);
        } else {
            // Si no hay welcomeScreen, cambiar inmediatamente (fallback)
            welcomeScreen.style.display = 'none';
            aboutContainer.style.display = 'none';
            aboutContainer.classList.remove('active');
            chatContainer.style.display = 'flex';
            chatContainer.classList.add('active');
            if (welcomeVideo) {
                try {
                    welcomeVideo.pause();
                } catch (error) {
                    console.warn('Error al detener el video:', error);
                }
            }
            createFaqPills();
        }
    }
    
    // Función para mostrar información del equipo
    function showAbout() {
        welcomeScreen.style.display = 'none';
        chatContainer.style.display = 'none';
        chatContainer.classList.remove('active');
        aboutContainer.style.display = 'flex';
        aboutContainer.classList.add('active');
        if (welcomeVideo) {
            try {
                welcomeVideo.pause();
            } catch (error) {
                console.warn('Error al detener el video:', error);
            }
        }
    }
    
    // Función para cerrar el chat después de mostrar despedida del servidor
    function closeChatAfterGoodbye(mensajeDespedida) {
        // Iniciar transición de fade out del chat container
        if (chatContainer) {
            chatContainer.classList.add('closing');
        }
        
        // Esperar a que termine la transición de fade out
        setTimeout(() => {
            // Limpiar todos los mensajes excepto el mensaje de bienvenida inicial
            const allMessages = chatMessages.querySelectorAll('.message:not(.welcome-chat-message)');
            allMessages.forEach(msg => msg.remove());
            
            // Ocultar el chat container
            chatContainer.style.display = 'none';
            chatContainer.classList.remove('active');
            chatContainer.classList.remove('closing');
            
            // Mostrar welcome screen con fade in
            if (welcomeScreen) {
                welcomeScreen.style.display = 'flex';
                welcomeScreen.style.opacity = '0';
                
                // Forzar reflow para que la transición funcione
                void welcomeScreen.offsetWidth;
                
                // Iniciar fade in
                setTimeout(() => {
                    welcomeScreen.style.opacity = '1';
                }, 10);
            }
            
            // Reiniciar y reproducir el video
            if (welcomeVideo) {
                welcomeVideo.currentTime = 0;
                welcomeVideo.play().catch(() => {});
            }
            
            // Limpiar el input
            if (userInput) {
                userInput.value = '';
            }
        }, 500); // Esperar el tiempo de la transición CSS (0.5s)
    }
    
    // Función para cerrar el chat con mensaje de despedida (usado por el botón X)
    function closeChat() {
        // Mensajes de despedida naturales y variados
        const despedidas = [
            '¡Nos vemos luego, mijo! Que disfrutes los eventos en Loja. 😊',
            '¡Hasta pronto! Espero haberte ayudado a encontrar eventos chéveres. 👋',
            '¡Chao! Recuerda apoyar lo local. Nos vemos en los eventos de Loja. 🎉',
            '¡Hasta la próxima! Que la pases bien en los eventos. 😄',
            '¡Nos vemos! Si necesitas más información sobre eventos, aquí estaré. 👋'
        ];
        
        // Seleccionar un mensaje aleatorio
        const mensajeDespedida = despedidas[Math.floor(Math.random() * despedidas.length)];
        
        // Agregar mensaje de despedida del bot
        addMessage(mensajeDespedida, false);
        
        // Esperar 3 segundos para que el usuario pueda leer el mensaje de despedida antes de cerrar
        setTimeout(() => {
            closeChatAfterGoodbye(mensajeDespedida);
        }, 3000);
    }
    
    // Función para volver a la pantalla de bienvenida
    function backToWelcome() {
        aboutContainer.style.display = 'none';
        aboutContainer.classList.remove('active');
        chatContainer.style.display = 'none';
        chatContainer.classList.remove('active');
        welcomeScreen.style.display = 'flex';
        if (welcomeVideo) {
            welcomeVideo.currentTime = 0;
            welcomeVideo.play().catch(() => {});
        }
    }
    
    // Event listeners
    if (startButton) {
        startButton.addEventListener('click', startChat);
    }
    if (aboutButton) {
        aboutButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            showAbout();
        });
    }
    if (backToWelcomeButton) {
        backToWelcomeButton.addEventListener('click', backToWelcome);
    }
    
    // Event listener para el botón repetir (reinicia el video)
    if (repeatButton) {
        repeatButton.addEventListener('click', function() {
            console.log('🔴 Botón repetir clickeado');
            console.log('Video existe?', !!welcomeVideo);
            
            if (welcomeVideo) {
                console.log('Estado del video antes:', {
                    paused: welcomeVideo.paused,
                    currentTime: welcomeVideo.currentTime,
                    duration: welcomeVideo.duration,
                    readyState: welcomeVideo.readyState
                });
                
                // Pausar primero
                welcomeVideo.pause();
                console.log('✅ Video pausado');
                
                // Reiniciar al inicio
                welcomeVideo.currentTime = 0;
                console.log('✅ currentTime establecido a 0');
                
                // Forzar la actualización del frame
                welcomeVideo.load();
                console.log('✅ load() llamado');
                
                // Reproducir después de un pequeño delay
                setTimeout(() => {
                    console.log('Intentando reproducir video...');
                    console.log('Estado del video antes de play():', {
                        paused: welcomeVideo.paused,
                        currentTime: welcomeVideo.currentTime,
                        readyState: welcomeVideo.readyState
                    });
                    
                    const playPromise = welcomeVideo.play();
                    console.log('play() retornó:', playPromise);
                    
                    if (playPromise !== undefined) {
                        playPromise.then(() => {
                            console.log('✅ Video reproducido exitosamente');
                        }).catch((error) => {
                            console.error('❌ Error al reproducir el video:', error);
                        });
                    } else {
                        console.log('⚠️ play() no retornó una promesa');
                    }
                }, 100);
            } else {
                console.error('❌ welcomeVideo no existe');
            }
        });
    } else {
        console.error('❌ repeatButton no existe');
    }

    const ICON_LINE_REGEX = /^\[([a-z]+)\]\s*(.*)$/;

    function escapeHTML(str) {
        return str.replace(/[&<>"']/g, function(match) {
            switch (match) {
                case '&': return '&amp;';
                case '<': return '&lt;';
                case '>': return '&gt;';
                case '"': return '&quot;';
                case "'": return '&#39;';
                default: return match;
            }
        });
    }

    function formatWithStrong(text) {
        return text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    }

    function createMessageParagraph(text) {
        const container = document.createElement('div');
        container.className = 'message-content-inner';

        const lines = text.split('\n');
        lines.forEach((line) => {
            const trimmed = line.trim();
            if (trimmed === '') {
                return;
            }

            const lineElement = document.createElement('div');
            lineElement.className = 'message-line';

            const iconMatch = trimmed.match(ICON_LINE_REGEX);
            if (iconMatch) {
                const iconType = iconMatch[1];
                const iconSpan = document.createElement('span');
                iconSpan.className = 'message-icon';
                iconSpan.dataset.icon = iconType;

                const contentSpan = document.createElement('span');
                let safeContent = escapeHTML(iconMatch[2]);
                safeContent = formatWithStrong(safeContent);
                contentSpan.innerHTML = safeContent;

                lineElement.classList.add('with-icon');
                lineElement.appendChild(iconSpan);
                lineElement.appendChild(contentSpan);
            } else {
                let safeContent = escapeHTML(trimmed);
                safeContent = formatWithStrong(safeContent);
                lineElement.innerHTML = safeContent;
            }

            container.appendChild(lineElement);
        });

        return container;
    }

    function addMessage(text, isUser = false) {
        const shouldScroll = isNearBottom();
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        // Contenedor del mensaje
        const messageContentWrapper = document.createElement('div');
        messageContentWrapper.className = 'message-content-wrapper';
        messageContentWrapper.appendChild(createMessageParagraph(text));
        
        messageDiv.appendChild(messageContentWrapper);
        chatMessages.appendChild(messageDiv);
        
        // Agregar clase "last" al último mensaje del mismo tipo
        const allMessages = chatMessages.querySelectorAll('.message');
        const lastMessage = allMessages[allMessages.length - 1];
        const previousMessage = allMessages[allMessages.length - 2];
        
        // Remover "last" de todos los mensajes
        allMessages.forEach(msg => msg.classList.remove('last'));
        
        // Si no hay mensaje anterior o es de diferente tipo, este es el último
        if (!previousMessage || 
            (previousMessage.classList.contains('user-message') !== isUser)) {
            lastMessage.classList.add('last');
        } else {
            // Si el anterior es del mismo tipo, quitarle "last" y dárselo a este
            previousMessage.classList.remove('last');
            lastMessage.classList.add('last');
        }
        
        if (shouldScroll) {
            scrollToBottom();
        }
    }

    function createEventCard(event) {
        const card = document.createElement('article');
        card.className = 'event-card event-card--hidden';

        const lightLayer = document.createElement('div');
        lightLayer.className = 'event-card__light-layer';

        const slit = document.createElement('div');
        slit.className = 'event-card__slit';

        const lumen = document.createElement('div');
        lumen.className = 'event-card__lumen';

        ['min', 'mid', 'hi'].forEach(level => {
            const span = document.createElement('span');
            span.className = `event-card__lumen-${level}`;
            lumen.appendChild(span);
        });

        const darken = document.createElement('div');
        darken.className = 'event-card__darken';
        ['sl', 'll', 'slt', 'srt'].forEach(layer => {
            const span = document.createElement('span');
            span.className = `event-card__${layer}`;
            darken.appendChild(span);
        });

        const orbs = document.createElement('div');
        orbs.className = 'event-card__orbs';

        const orbBlue = document.createElement('span');
        orbBlue.className = 'event-card__orb event-card__orb--blue';

        const orbPink = document.createElement('span');
        orbPink.className = 'event-card__orb event-card__orb--pink';

        orbs.appendChild(orbBlue);
        orbs.appendChild(orbPink);

        lightLayer.appendChild(slit);
        lightLayer.appendChild(lumen);
        lightLayer.appendChild(darken);

        const content = document.createElement('div');
        content.className = 'event-card__content';

        const body = document.createElement('div');
        body.className = 'event-card__body';

        const title = document.createElement('h4');
        title.className = 'event-card__title';
        title.textContent = event.titulo;

        const location = document.createElement('p');
        location.className = 'event-card__location';
        location.textContent = event.ubicacion;

        // Formatear fecha con AM/PM
        let fechaFormateada = '';
        if (event.fecha) {
            try {
                // Parsear fecha en formato DD/MM/YYYY HH:MM
                const [fechaPart, horaPart] = event.fecha.split(' ');
                const [dia, mes, anio] = fechaPart.split('/');
                const [hora, minutos] = horaPart ? horaPart.split(':') : ['00', '00'];
                
                const fechaObj = new Date(anio, mes - 1, dia, hora, minutos);
                const horas12 = fechaObj.getHours() % 12 || 12;
                const ampm = fechaObj.getHours() >= 12 ? 'PM' : 'AM';
                const minutosStr = minutos.padStart(2, '0');
                
                // Formato: "15 de noviembre de 2025, 7:30 PM"
                const meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
                              'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
                fechaFormateada = `${dia} de ${meses[parseInt(mes) - 1]} de ${anio}, ${horas12}:${minutosStr} ${ampm}`;
            } catch (e) {
                fechaFormateada = event.fecha;
            }
        }

        const chips = document.createElement('div');
        chips.className = 'event-card__chips';

        const priceChip = document.createElement('span');
        priceChip.className = 'event-card__chip event-card__chip--price';
        priceChip.textContent = event.precio;

        const categoryChip = document.createElement('span');
        categoryChip.className = 'event-card__chip event-card__chip--category';
        categoryChip.textContent = event.categoria;

        chips.appendChild(priceChip);
        chips.appendChild(categoryChip);

        // Reordenar: chips primero, luego fecha, luego título
        body.appendChild(chips);
        
        const datetime = document.createElement('p');
        datetime.className = 'event-card__datetime';
        datetime.textContent = fechaFormateada || event.fecha;
        body.appendChild(datetime);
        
        body.appendChild(title);
        body.appendChild(location);
        if (event.descripcion) {
            const description = document.createElement('p');
            description.className = 'event-card__description';
            const maxLength = 140;
            const text = event.descripcion.trim();
            description.textContent = text.length > maxLength ? `${text.slice(0, maxLength)}…` : text;
            body.appendChild(description);
        }

        content.appendChild(body);

        card.appendChild(orbs);
        card.appendChild(lightLayer);
        card.appendChild(content);

        // Crear wrapper que contiene la tarjeta y el mapa
        const cardWrapper = document.createElement('div');
        cardWrapper.className = 'event-card-wrapper';
        
        // Agregar la tarjeta al wrapper
        cardWrapper.appendChild(card);
        
        // Crear div para el mapa de Google Maps (SIEMPRE crear para mantener consistencia)
        const mapContainer = document.createElement('div');
        mapContainer.className = 'event-card__map';
        
        // Crear iframe de Google Maps (formato simple sin API key)
        if (event.ubicacion) {
            const locationQuery = encodeURIComponent(event.ubicacion + ', Loja, Ecuador');
            const mapUrl = `https://www.google.com/maps?q=${locationQuery}&output=embed`;
            const mapIframe = document.createElement('iframe');
            mapIframe.src = mapUrl;
            mapIframe.width = '100%';
            mapIframe.height = '100';
            mapIframe.frameBorder = '0';
            mapIframe.style.border = '0';
            mapIframe.allowFullscreen = true;
            mapIframe.loading = 'lazy';
            mapIframe.referrerPolicy = 'no-referrer-when-downgrade';
            
            mapContainer.appendChild(mapIframe);
        } else {
            // Si no hay ubicación, mostrar un placeholder o mapa genérico de Loja
            const locationQuery = encodeURIComponent('Loja, Ecuador');
            const mapUrl = `https://www.google.com/maps?q=${locationQuery}&output=embed`;
            const mapIframe = document.createElement('iframe');
            mapIframe.src = mapUrl;
            mapIframe.width = '100%';
            mapIframe.height = '100';
            mapIframe.frameBorder = '0';
            mapIframe.style.border = '0';
            mapIframe.allowFullscreen = true;
            mapIframe.loading = 'lazy';
            mapIframe.referrerPolicy = 'no-referrer-when-downgrade';
            mapIframe.style.opacity = '0.6';
            
            mapContainer.appendChild(mapIframe);
        }
        
        // SIEMPRE agregar el contenedor del mapa para mantener todas las tarjetas iguales
        cardWrapper.appendChild(mapContainer);
        
        attachCardInteraction(card, event);
        return cardWrapper;
    }

    function addEventCards(events, showLoadMore = false) {
        if (!events || !events.length) {
            return;
        }

        const shouldScroll = isNearBottom();

        const wrapper = document.createElement('div');
        wrapper.className = 'event-cards-wrapper';

        const grid = document.createElement('div');
        grid.className = 'event-cards-grid';

        events.forEach((event) => {
            const cardWrapper = createEventCard(event);
            const card = cardWrapper.querySelector('.event-card');
            grid.appendChild(cardWrapper);
            if (card) {
                cardObserver.observe(card);
            }
        });

        wrapper.appendChild(grid);
        chatMessages.appendChild(wrapper);

        requestAnimationFrame(() => {
            wrapper.classList.add('event-cards-wrapper--visible');
        });

        // Agregar botón "Cargar más" fuera del contenedor de tarjetas
        if (showLoadMore) {
            const loadMoreWrapper = document.createElement('div');
            loadMoreWrapper.className = 'load-more-wrapper';
            
            const loadMoreButton = document.createElement('button');
            loadMoreButton.className = 'load-more-button';
            loadMoreButton.textContent = 'Cargar más';
            loadMoreButton.addEventListener('click', loadMoreEvents);
            
            loadMoreWrapper.appendChild(loadMoreButton);
            chatMessages.appendChild(loadMoreWrapper);
        }

        if (shouldScroll) {
            scrollToBottom();
        }
    }
    
    async function loadMoreEvents() {
        if (!hasMoreEvents) return;
        
        currentOffset += 6;
        setLoading(true);
        
        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: lastMessage,
                    offset: currentOffset
                })
            });

            const data = await response.json();
            
            if (data.error) {
                console.error('Error al cargar más eventos:', data.error);
            } else if (data.events && data.events.length > 0) {
                // Remover el botón "Cargar más" anterior
                const previousLoadMore = chatMessages.querySelector('.load-more-wrapper');
                if (previousLoadMore) {
                    previousLoadMore.remove();
                }
                
                // Agregar solo los nuevos eventos (sin mensaje del bot)
                addEventCards(data.events, data.has_more || false);
                hasMoreEvents = data.has_more || false;
                
                // Hacer scroll hacia abajo para mostrar los nuevos eventos
                scrollToBottom();
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    }

    function addBotResponse(text, events = [], hasMore = false) {
        addMessage(text, false);
        if (events && events.length) {
            addEventCards(events, hasMore);
        }
    }

    function addBotResponseWithActions(text, events = []) {
        const shouldScroll = isNearBottom();
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        
        // Contenedor del mensaje
        const messageContentWrapper = document.createElement('div');
        messageContentWrapper.className = 'message-content-wrapper';
        messageContentWrapper.appendChild(createMessageParagraph(text));
        
        // Contenedor para los botones de acción
        const actionsContainer = document.createElement('div');
        actionsContainer.className = 'message-actions';
        
        // Botón Continuar
        const continueButton = document.createElement('button');
        continueButton.className = 'action-button action-button--continue';
        continueButton.textContent = 'Continuar';
        continueButton.addEventListener('click', () => {
            // Simplemente continuar, no hacer nada especial
            actionsContainer.remove();
        });
        
        // Botón Salir
        const exitButton = document.createElement('button');
        exitButton.className = 'action-button action-button--exit';
        exitButton.textContent = 'Salir';
        exitButton.addEventListener('click', () => {
            // Confirmar salida y cerrar el chat
            confirmExitChat();
        });
        
        actionsContainer.appendChild(continueButton);
        actionsContainer.appendChild(exitButton);
        messageContentWrapper.appendChild(actionsContainer);
        
        messageDiv.appendChild(messageContentWrapper);
        chatMessages.appendChild(messageDiv);
        
        // Agregar clase "last"
        const allMessages = chatMessages.querySelectorAll('.message');
        allMessages.forEach(msg => msg.classList.remove('last'));
        messageDiv.classList.add('last');
        
        if (events && events.length) {
            addEventCards(events);
        }
        
        if (shouldScroll) {
            scrollToBottom();
        }
    }

    function confirmExitChat() {
        // Generar mensaje de despedida final
        const despedidas = [
            '¡Nos vemos luego, mijo! Que disfrutes los eventos en Loja. 😊',
            '¡Hasta pronto! Espero haberte ayudado a encontrar eventos chéveres. 👋',
            '¡Chao! Recuerda apoyar lo local. Nos vemos en los eventos de Loja. 🎉',
            '¡Hasta la próxima! Que la pases bien en los eventos. 😄',
            '¡Nos vemos! Si necesitas más información sobre eventos, aquí estaré. 👋'
        ];
        const mensajeDespedida = despedidas[Math.floor(Math.random() * despedidas.length)];
        
        // Mostrar mensaje de despedida
        addMessage(mensajeDespedida, false);
        
        // Esperar 3 segundos antes de cerrar
        setTimeout(() => {
            closeChatAfterGoodbye(mensajeDespedida);
        }, 3000);
    }

    function setLoading(isLoading) {
        sendButton.disabled = isLoading;
        userInput.disabled = isLoading;
        
        if (isLoading) {
            // Agregar animación simple
            sendButton.classList.add('bounce');
            setTimeout(() => {
                sendButton.classList.remove('bounce');
            }, 300);
        }
    }

    // Función para mostrar indicador de "escribiendo"
    function showTypingIndicator() {
        const shouldScroll = isNearBottom();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator last';
        typingDiv.id = 'typingIndicator';
        
        // Contenedor del mensaje
        const messageContentWrapper = document.createElement('div');
        messageContentWrapper.className = 'message-content-wrapper';
        messageContentWrapper.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
        
        typingDiv.appendChild(messageContentWrapper);
        chatMessages.appendChild(typingDiv);
        if (shouldScroll) {
            scrollToBottom();
        }
    }

    // Función para ocultar indicador de "escribiendo"
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    async function sendMessageWithText(message, options = {}) {
        const { hideUserMessage = false, displayText } = options;
        const trimmed = message.trim();
        if (trimmed === '') return;

        // Ocultar las FAQ pills cuando se envía cualquier mensaje
        hideFaqPills();

        // Solo mostrar mensaje del usuario si no viene de una pastilla
        if (!hideUserMessage) {
            addMessage(displayText || trimmed, true);
        }
        userInput.value = '';
        setLoading(true);
        
        // Mostrar indicador de escribiendo
        showTypingIndicator();

        try {
            // Guardar el mensaje para la paginación
            if (!options.hideUserMessage) {
                lastMessage = trimmed;
                currentOffset = 0;
            }
            
            // Enviar petición al backend
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: trimmed,
                    offset: currentOffset
                })
            });

            const data = await response.json();

            // Ocultar indicador de escribiendo
            hideTypingIndicator();

            if (data.error) {
                addBotResponse('Lo siento, hubo un error al procesar tu mensaje.');
            } else {
                // Guardar estado de paginación
                hasMoreEvents = data.has_more || false;
                
                // Si hay confirmación de salida, agregar botones de acción
                if (data.confirm_exit) {
                    addBotResponseWithActions(data.response, data.events || []);
                } else {
                    addBotResponse(data.response, data.events || [], hasMoreEvents);
                }
                
                // Si la respuesta indica que debe cerrarse el chat (despedida confirmada)
                if (data.close_chat) {
                    // Esperar 3 segundos para que el usuario pueda leer el mensaje de despedida
                    setTimeout(() => {
                        closeChatAfterGoodbye(data.response);
                    }, 3000);
                }
            }
        } catch (error) {
            hideTypingIndicator();
            addBotResponse('Lo siento, hubo un error al procesar tu mensaje.');
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    }

    async function sendMessage() {
        const message = userInput.value;
        await sendMessageWithText(message);
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !sendButton.disabled) {
            sendMessage();
        }
    });

    // Event listener para el botón de micrófono

    function attachCardInteraction(cardElement, event) {
        cardElement.classList.add('event-card--interactive');
        cardElement.setAttribute('role', 'button');
        cardElement.setAttribute('tabindex', '0');
        cardElement.addEventListener('click', () => {
            sendMessageWithText(`Dame más información sobre ${event.titulo}`);
        });
        cardElement.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                sendMessageWithText(`Dame más información sobre ${event.titulo}`);
            }
        });
    }
});

