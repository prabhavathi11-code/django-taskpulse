/**
 * NexusAI Studio - Frontend Chat Engine
 * Handles real-time messaging, markdown parsing, voice recognition, and conversation state.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatContainer = document.getElementById('chatContainer');
    const messagesStream = document.getElementById('messagesStream');
    const welcomeHero = document.getElementById('welcomeHero');
    const promptInput = document.getElementById('promptInput');
    const sendBtn = document.getElementById('sendBtn');
    const typingBubble = document.getElementById('typingBubble');
    const charCount = document.getElementById('charCount');
    const activeChatTitle = document.getElementById('activeChatTitle');
    const currentModelTag = document.getElementById('currentModelTag');
    const modelSelector = document.getElementById('modelSelector');

    // Sidebar & Actions
    const sidebar = document.getElementById('sidebar');
    const openSidebarBtn = document.getElementById('openSidebarBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');
    const newChatBtn = document.getElementById('newChatBtn');
    const historyList = document.getElementById('historyList');
    const clearAllBtn = document.getElementById('clearAllBtn');
    const exportChatBtn = document.getElementById('exportChatBtn');
    const toggleThemeBtn = document.getElementById('toggleThemeBtn');
    const themeIcon = document.getElementById('themeIcon');

    // Voice & Audio
    const voiceBtn = document.getElementById('voiceBtn');
    const voiceIcon = document.getElementById('voiceIcon');

    // Settings Modal
    const settingsBtn = document.getElementById('settingsBtn');
    const settingsModal = document.getElementById('settingsModal');
    const closeSettingsBtn = document.getElementById('closeSettingsBtn');
    const cancelSettingsBtn = document.getElementById('cancelSettingsBtn');
    const saveSettingsBtn = document.getElementById('saveSettingsBtn');
    const customApiKeyInput = document.getElementById('customApiKey');
    const autoSpeechToggle = document.getElementById('autoSpeechToggle');

    // State
    let activeConversationId = null;
    let isProcessing = false;
    let recognition = null;
    let isRecording = false;

    // Load persisted settings
    const storedApiKey = localStorage.getItem('nexus_api_key') || '';
    const storedTheme = localStorage.getItem('nexus_theme') || 'dark';
    const autoSpeech = localStorage.getItem('nexus_auto_speech') === 'true';

    if (customApiKeyInput) customApiKeyInput.value = storedApiKey;
    if (autoSpeechToggle) autoSpeechToggle.checked = autoSpeech;

    // Apply saved theme
    if (storedTheme === 'light') {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
        themeIcon.classList.replace('fa-moon', 'fa-sun');
    }

    // Configure marked.js options
    if (window.marked) {
        marked.setOptions({
            breaks: true,
            gfm: true
        });
    }

    // Initialize Web Speech API
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isRecording = true;
            voiceBtn.classList.add('recording');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            promptInput.value = (promptInput.value ? promptInput.value + ' ' : '') + transcript;
            updateInputHeight();
            updateCharCount();
        };

        recognition.onerror = () => {
            stopRecording();
        };

        recognition.onend = () => {
            stopRecording();
        };
    } else {
        voiceBtn.style.display = 'none';
    }

    function toggleRecording() {
        if (!recognition) return;
        if (isRecording) {
            recognition.stop();
        } else {
            try {
                recognition.start();
            } catch (err) {
                console.error(err);
            }
        }
    }

    function stopRecording() {
        isRecording = false;
        voiceBtn.classList.remove('recording');
    }

    // Auto resize textarea
    function updateInputHeight() {
        promptInput.style.height = 'auto';
        promptInput.style.height = Math.min(promptInput.scrollHeight, 150) + 'px';
    }

    function updateCharCount() {
        const length = promptInput.value.length;
        charCount.textContent = `${length}/4000`;
    }

    promptInput.addEventListener('input', () => {
        updateInputHeight();
        updateCharCount();
    });

    // Enter key handling
    promptInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', () => {
        sendMessage();
    });

    // Voice button
    voiceBtn.addEventListener('click', toggleRecording);

    // Prompt chip shortcuts
    document.querySelectorAll('.prompt-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const text = chip.getAttribute('data-prompt');
            promptInput.value = text;
            updateInputHeight();
            updateCharCount();
            sendMessage();
        });
    });

    // Send Message Logic
    async function sendMessage() {
        const text = promptInput.value.trim();
        if (!text || isProcessing) return;

        isProcessing = true;
        sendBtn.disabled = true;

        // Hide welcome hero on first message
        if (welcomeHero) {
            welcomeHero.style.display = 'none';
        }

        // Render User Message
        appendMessage('user', text, formatTime(new Date()));

        // Clear input
        promptInput.value = '';
        updateInputHeight();
        updateCharCount();
        scrollToBottom();

        // Show typing indicator
        typingBubble.style.display = 'flex';
        scrollToBottom();

        try {
            const apiKey = localStorage.getItem('nexus_api_key') || '';
            const response = await fetch('/chatbot/api/send/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt: text,
                    conversation_id: activeConversationId,
                    api_key: apiKey
                })
            });

            const data = await response.json();

            // Hide typing indicator
            typingBubble.style.display = 'none';

            if (response.ok && data.success) {
                // Update active conversation
                activeConversationId = data.conversation_id;
                activeChatTitle.textContent = data.conversation_title;

                // Render Bot Message
                appendMessage('assistant', data.reply, data.timestamp);

                // Auto speech synthesis if enabled
                if (autoSpeechToggle && autoSpeechToggle.checked) {
                    speakText(data.reply);
                }

                // Refresh history list
                loadConversations();
            } else {
                appendMessage('assistant', `⚠️ **Error:** ${data.error || 'Failed to generate response.'}`, formatTime(new Date()));
            }
        } catch (err) {
            typingBubble.style.display = 'none';
            appendMessage('assistant', `⚠️ **Connection Error:** Could not contact server. Please verify Django server is running.`, formatTime(new Date()));
        } finally {
            isProcessing = false;
            sendBtn.disabled = false;
            scrollToBottom();
        }
    }

    // Append Message to Stream
    function appendMessage(role, content, timestamp) {
        const row = document.createElement('div');
        row.className = `message-row ${role === 'user' ? 'user-row' : 'bot-row'}`;

        const isUser = role === 'user';
        const avatarHtml = isUser 
            ? `<div class="message-avatar user-avatar"><i class="fa-solid fa-user"></i></div>`
            : `<div class="message-avatar bot-avatar"><i class="fa-solid fa-sparkles"></i></div>`;

        let formattedContent = '';
        if (isUser) {
            formattedContent = escapeHtml(content);
        } else {
            formattedContent = formatMarkdown(content);
        }

        const toolsHtml = !isUser ? `
            <div class="bubble-tools">
                <button class="bubble-tool-btn copy-msg-btn" title="Copy text">
                    <i class="fa-regular fa-copy"></i> Copy
                </button>
                <button class="bubble-tool-btn read-msg-btn" title="Listen">
                    <i class="fa-solid fa-volume-high"></i> Listen
                </button>
            </div>
        ` : '';

        row.innerHTML = `
            ${!isUser ? avatarHtml : ''}
            <div class="message-bubble ${isUser ? 'user-bubble' : 'bot-bubble'}">
                <div class="bubble-body">${formattedContent}</div>
                ${toolsHtml}
                <span class="message-time">${timestamp || ''}</span>
            </div>
            ${isUser ? avatarHtml : ''}
        `;

        messagesStream.appendChild(row);

        // Highlight newly added code blocks
        row.querySelectorAll('pre code').forEach(block => {
            if (window.hljs) hljs.highlightElement(block);
        });

        // Add copy event to message
        const copyBtn = row.querySelector('.copy-msg-btn');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(content);
                showToast('Message copied to clipboard!');
            });
        }

        // Add read-aloud event
        const readBtn = row.querySelector('.read-msg-btn');
        if (readBtn) {
            readBtn.addEventListener('click', () => {
                speakText(content);
            });
        }

        // Setup copy buttons inside code blocks
        row.querySelectorAll('.code-card').forEach(card => {
            const btn = card.querySelector('.copy-code-btn');
            const code = card.querySelector('code');
            if (btn && code) {
                btn.addEventListener('click', () => {
                    navigator.clipboard.writeText(code.innerText);
                    showToast('Code copied to clipboard!');
                });
            }
        });

        scrollToBottom();
    }

    // Markdown & Code block wrapper
    function formatMarkdown(rawText) {
        if (!window.marked) return escapeHtml(rawText);

        let parsed = marked.parse(rawText);

        // Wrap pre tags in custom code-cards with header & copy button
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = parsed;

        tempDiv.querySelectorAll('pre').forEach(pre => {
            const codeEl = pre.querySelector('code');
            let lang = 'code';
            if (codeEl) {
                const classes = codeEl.className.split(' ');
                for (const cls of classes) {
                    if (cls.startsWith('language-')) {
                        lang = cls.replace('language-', '');
                        break;
                    }
                }
            }

            const codeCard = document.createElement('div');
            codeCard.className = 'code-card';
            codeCard.innerHTML = `
                <div class="code-header">
                    <span>${lang}</span>
                    <button class="copy-code-btn">
                        <i class="fa-regular fa-clone"></i> Copy
                    </button>
                </div>
            `;
            pre.parentNode.insertBefore(codeCard, pre);
            codeCard.appendChild(pre);
        });

        return tempDiv.innerHTML;
    }

    // Speech Synthesis
    function speakText(text) {
        if (!('speechSynthesis' in window)) return;
        window.speechSynthesis.cancel();

        // Strip markdown and code blocks for speech
        const cleanText = text.replace(/```[\s\S]*?```/g, 'Code block omitted.')
                              .replace(/[`*#_>~]/g, '');

        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
    }

    // Load conversations list
    async function loadConversations() {
        try {
            const res = await fetch('/chatbot/api/conversations/');
            const data = await res.json();
            if (data.conversations) {
                renderHistoryList(data.conversations);
            }
        } catch (e) {
            console.error(e);
        }
    }

    function renderHistoryList(conversations) {
        historyList.innerHTML = '';
        if (conversations.length === 0) {
            historyList.innerHTML = `
                <div class="empty-history" id="emptyHistoryMsg">
                    <i class="fa-regular fa-comment-dots"></i>
                    <p>No conversations yet. Start one!</p>
                </div>
            `;
            return;
        }

        conversations.forEach(conv => {
            const item = document.createElement('div');
            item.className = `history-item ${conv.id === activeConversationId ? 'active' : ''}`;
            item.setAttribute('data-id', conv.id);
            item.innerHTML = `
                <i class="fa-regular fa-message"></i>
                <span class="item-title">${escapeHtml(conv.title)}</span>
                <button class="delete-conv-btn" data-id="${conv.id}" title="Delete chat">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            `;

            // Click to load
            item.addEventListener('click', (e) => {
                if (!e.target.closest('.delete-conv-btn')) {
                    loadChatSession(conv.id);
                    if (window.innerWidth <= 768) {
                        sidebar.classList.remove('open');
                    }
                }
            });

            // Delete single chat
            const delBtn = item.querySelector('.delete-conv-btn');
            delBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                deleteConversation(conv.id);
            });

            historyList.appendChild(item);
        });
    }

    // Load Chat Session
    async function loadChatSession(convId) {
        try {
            const res = await fetch(`/chatbot/api/conversations/${convId}/messages/`);
            const data = await res.json();

            if (res.ok) {
                activeConversationId = data.conversation_id;
                activeChatTitle.textContent = data.title;
                messagesStream.innerHTML = '';

                if (welcomeHero) welcomeHero.style.display = 'none';

                data.messages.forEach(msg => {
                    appendMessage(msg.role, msg.content, msg.timestamp);
                });

                // Update active list state
                document.querySelectorAll('.history-item').forEach(el => {
                    el.classList.toggle('active', el.getAttribute('data-id') === activeConversationId);
                });

                scrollToBottom();
            }
        } catch (err) {
            console.error(err);
        }
    }

    // Delete single conversation
    async function deleteConversation(convId) {
        if (!confirm('Are you sure you want to delete this conversation?')) return;
        try {
            const res = await fetch(`/chatbot/api/conversations/${convId}/delete/`, { method: 'POST' });
            if (res.ok) {
                if (activeConversationId === convId) {
                    startNewChat();
                }
                loadConversations();
                showToast('Conversation deleted.');
            }
        } catch (err) {
            console.error(err);
        }
    }

    // Clear All Conversations
    clearAllBtn.addEventListener('click', async () => {
        if (!confirm('Clear all conversation history? This cannot be undone.')) return;
        try {
            const res = await fetch('/chatbot/api/clear-all/', { method: 'POST' });
            if (res.ok) {
                startNewChat();
                loadConversations();
                showToast('All chat history cleared.');
            }
        } catch (err) {
            console.error(err);
        }
    });

    // Start New Chat
    function startNewChat() {
        activeConversationId = null;
        activeChatTitle.textContent = 'New Session';
        messagesStream.innerHTML = '';
        if (welcomeHero) welcomeHero.style.display = 'block';
        promptInput.value = '';
        updateInputHeight();
        updateCharCount();
        document.querySelectorAll('.history-item').forEach(el => el.classList.remove('active'));
    }

    newChatBtn.addEventListener('click', startNewChat);

    // Keyboard shortcut for New Chat (Ctrl+N or Alt+N)
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'n') {
            e.preventDefault();
            startNewChat();
        }
    });

    // Export conversation as Markdown
    exportChatBtn.addEventListener('click', () => {
        const rows = messagesStream.querySelectorAll('.message-row');
        if (rows.length === 0) {
            showToast('No messages to export.');
            return;
        }

        let mdContent = `# ${activeChatTitle.textContent}\nExported on: ${new Date().toLocaleString()}\n\n---\n\n`;

        rows.forEach(r => {
            const isUser = r.classList.contains('user-row');
            const bubble = r.querySelector('.bubble-body');
            const role = isUser ? 'User' : 'NexusAI';
            mdContent += `### **${role}**\n\n${bubble.innerText.trim()}\n\n---\n\n`;
        });

        const blob = new Blob([mdContent], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Chat_${activeChatTitle.textContent.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.md`;
        a.click();
        URL.revokeObjectURL(url);
        showToast('Chat exported successfully!');
    });

    // Theme Toggle
    toggleThemeBtn.addEventListener('click', () => {
        const isDark = document.body.classList.contains('dark-mode');
        if (isDark) {
            document.body.classList.remove('dark-mode');
            document.body.classList.add('light-mode');
            themeIcon.classList.replace('fa-moon', 'fa-sun');
            localStorage.setItem('nexus_theme', 'light');
        } else {
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');
            themeIcon.classList.replace('fa-sun', 'fa-moon');
            localStorage.setItem('nexus_theme', 'dark');
        }
    });

    // Model Selector Change
    modelSelector.addEventListener('change', (e) => {
        const val = e.target.value;
        if (val === 'gemini-1.5') {
            currentModelTag.innerHTML = `<i class="fa-solid fa-sparkles"></i> Gemini 1.5`;
        } else if (val === 'gpt-4o-mini') {
            currentModelTag.innerHTML = `<i class="fa-solid fa-brain"></i> GPT-4o Mini`;
        } else {
            currentModelTag.innerHTML = `<i class="fa-solid fa-bolt"></i> Nexus Core`;
        }
    });

    // Settings Modal Open/Close
    settingsBtn.addEventListener('click', () => {
        settingsModal.classList.add('open');
    });

    [closeSettingsBtn, cancelSettingsBtn].forEach(b => {
        if (b) b.addEventListener('click', () => settingsModal.classList.remove('open'));
    });

    saveSettingsBtn.addEventListener('click', () => {
        const key = customApiKeyInput.value.trim();
        localStorage.setItem('nexus_api_key', key);
        localStorage.setItem('nexus_auto_speech', autoSpeechToggle.checked);
        settingsModal.classList.remove('open');
        showToast('Settings saved successfully!');
    });

    // Mobile Sidebar Toggle
    if (openSidebarBtn) {
        openSidebarBtn.addEventListener('click', () => sidebar.classList.add('open'));
    }
    if (closeSidebarBtn) {
        closeSidebarBtn.addEventListener('click', () => sidebar.classList.remove('open'));
    }

    // Toast Notification helper
    function showToast(msg) {
        const toast = document.getElementById('appToast');
        if (!toast) return;
        toast.textContent = msg;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 2800);
    }

    // Scroll helper
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Escape helper
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    // Initial load
    loadConversations();
});
