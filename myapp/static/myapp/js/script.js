document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('submit-btn').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the form from submitting traditionally

        var userInput = document.getElementById('user-input').value;
        if (userInput.trim() !== '') {
            addMessage('user', userInput);
            document.getElementById('user-input').value = '';

            fetch('/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ message: userInput })
            })
            .then(response => response.json())
            .then(data => {
                addMessage('bot', data.message);
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage('bot', 'Sorry, there was an error processing your request.');
            });
        }
    });
});

function addMessage(sender, text) {
    var chatHistory = document.getElementById('chat-history');
    var message = document.createElement('div');
    message.classList.add('message', sender);

    var avatar = document.createElement('div');
    avatar.classList.add('avatar', sender === 'user' ? 'user-avatar' : 'bot-avatar');
    message.appendChild(avatar);

    var messageText = document.createElement('div');
    messageText.classList.add('text');
    messageText.textContent = text;
    message.appendChild(messageText);

    chatHistory.appendChild(message);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
