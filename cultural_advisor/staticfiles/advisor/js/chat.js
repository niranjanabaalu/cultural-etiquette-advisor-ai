let currentSessionId = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    setupEventListeners();
});

function setupEventListeners() {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const toggleSidebar = document.getElementById('toggle-sidebar');
    const sidebar = document.getElementById('sidebar');

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    toggleSidebar.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });
}

// Load Chat History for Sidebar
async function loadHistory() {
    try {
        const response = await fetch(historyUrl);
        const data = await response.json();
        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '';

        data.history.forEach(session => {
            const item = document.createElement('div');
            item.className = `history-item ${session.id === currentSessionId ? 'active' : ''}`;
            item.onclick = () => loadSession(session.id);
            item.innerHTML = `
                <span class="title">${session.title}</span>
                <span class="date">${session.timestamp}</span>
            `;
            historyList.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Load Messages for a specific session
async function loadSession(sessionId) {
    currentSessionId = sessionId;
    updateActiveHistoryItem();
    
    try {
        const response = await fetch(`/messages/${sessionId}/`);
        const data = await response.json();
        const chatWindow = document.getElementById('chat-window');
        chatWindow.innerHTML = '';

        data.messages.forEach(msg => {
            appendMessage(msg.is_bot ? 'bot' : 'user', msg.content);
        });
        
        chatWindow.scrollTop = chatWindow.scrollHeight;
    } catch (error) {
        console.error('Error loading session:', error);
    }
}

function updateActiveHistoryItem() {
    document.querySelectorAll('.history-item').forEach(item => {
        item.classList.remove('active');
    });
    // Find the current item and mark active if possible
    // (Simplified: reload history also works)
    loadHistory(); 
}

// Start New Chat
async function startNewChat() {
    const greetings = [
        "Ready to bridge cultures? How can I help you today?",
        "Where are we traveling today? Ask me about any country's etiquette!",
        "Let's explore global manners together! What's on your mind?",
        "Welcome! I'm your guide to cultural etiquette. How can I assist?",
        "Curious about a different culture? Let's dive in!",
        "Traveling soon? Let's make sure you know the local customs!"
    ];
    const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];

    currentSessionId = null;
    document.getElementById('chat-window').innerHTML = `
        <div class="message bot">
            <div class="bubble">
                ${randomGreeting}
            </div>
        </div>
    `;
    document.querySelectorAll('.history-item').forEach(item => item.classList.remove('active'));

    // Reset backend context
    try {
        await fetch('/reset-context/');
        console.log('Context memory cleared for new session.');
    } catch (e) {
        console.warn('Could not reset context:', e);
    }
}

// Send Message
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    appendMessage('user', message);
    input.value = '';
    
    const chatWindow = document.getElementById('chat-window');
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Show typing indicator
    document.getElementById('typing-indicator').style.display = 'block';

    try {
        const response = await fetch(chatUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                message: message,
                session_id: currentSessionId
            })
        });

        const data = await response.json();
        document.getElementById('typing-indicator').style.display = 'none';

        if (data.reply) {
            appendMessage('bot', data.reply);
            currentSessionId = data.session_id; // Set session ID if it was a new chat
            loadHistory(); // Refresh history to show new/updated session
        }
        
        chatWindow.scrollTop = chatWindow.scrollHeight;
    } catch (error) {
        document.getElementById('typing-indicator').style.display = 'none';
        appendMessage('bot', 'Sorry, I encountered an error. Please try again.');
    }
}

function appendMessage(role, content) {
    const chatWindow = document.getElementById('chat-window');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    
    // Convert newlines to breaks and wrap in descriptive paragraphs if needed
    // The AI is instructed to use paragraphs, but we handle formatting just in case
    let htmlContent = content
        .trim()
        .replace(/### (.*)/g, '<h3>$1</h3>') // Headers
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" class="bot-flag">') // Images
        .replace(/\n---\n/g, '<hr>') // Horizontal rule
        .replace(/^\s*[\-\*]\s+(.*)/gm, '<li>$1</li>') // Bullet points
        .replace(/\n\n/g, '</p><p>') // Double newlines to paragraphs
        .replace(/\n/g, '<br>'); // Single newlines to breaks

    // Ensure it starts and ends with paragraph tags if it has multiple sections
    if (htmlContent.includes('</p>')) {
        htmlContent = `<p>${htmlContent}</p>`;
    }

    msgDiv.innerHTML = `
        <div class="bubble">
            ${htmlContent}
        </div>
    `;
    
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}