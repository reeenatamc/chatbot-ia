document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');

    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.innerHTML = `<p>${text}</p>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function setLoading(isLoading) {
        sendButton.disabled = isLoading;
        sendButton.textContent = isLoading ? 'Enviando...' : 'Enviar';
        userInput.disabled = isLoading;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        // Agregar mensaje del usuario
        addMessage(message, true);
        userInput.value = '';
        setLoading(true);

        try {
            // Enviar petición al backend
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            if (response.ok) {
                addMessage(data.response);
            } else {
                addMessage('Error: ' + (data.error || 'No se pudo obtener respuesta'));
            }
        } catch (error) {
            addMessage('Error de conexión. Por favor, intenta de nuevo.');
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !sendButton.disabled) {
            sendMessage();
        }
    });
});

