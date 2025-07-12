/**
 * OPTEEE Chat Interface JavaScript
 * Advanced chat functionality with local storage and history management
 */

class ChatManager {
    constructor() {
        this.currentSessionId = null;
        this.sessions = this.loadSessions();
        this.isTyping = false;
        this.typingTimeout = null;
        this.initializeChat();
        this.setupEventListeners();
    }

    /**
     * Load chat sessions from localStorage
     */
    loadSessions() {
        try {
            const stored = localStorage.getItem('opteee_chat_sessions');
            return stored ? JSON.parse(stored) : {};
        } catch (error) {
            console.error('Error loading chat sessions:', error);
            return {};
        }
    }

    /**
     * Save chat sessions to localStorage
     */
    saveSessions() {
        try {
            localStorage.setItem('opteee_chat_sessions', JSON.stringify(this.sessions));
            this.updateChatHistoryDisplay();
        } catch (error) {
            console.error('Error saving chat sessions:', error);
        }
    }

    /**
     * Create a new chat session
     */
    createNewSession() {
        const sessionId = 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        
        this.sessions[sessionId] = {
            id: sessionId,
            title: 'New Chat',
            created: new Date().toISOString(),
            lastUpdated: new Date().toISOString(),
            messages: [],
            settings: {
                provider: 'openai',
                numResults: 5
            }
        };
        
        this.currentSessionId = sessionId;
        this.saveSessions();
        
        console.log('Created new chat session:', sessionId);
        return sessionId;
    }

    /**
     * Generate a meaningful title from the first message
     */
    generateChatTitle(firstMessage) {
        if (!firstMessage || typeof firstMessage !== 'string') {
            return 'New Chat';
        }
        
        // Clean up the message
        const cleanMessage = firstMessage.replace(/[^\w\s]/gi, '').trim();
        
        // Extract key terms for better titles
        const keyTerms = cleanMessage.split(' ').filter(word => 
            word.length > 3 && 
            !['what', 'when', 'where', 'why', 'how', 'can', 'will', 'does', 'is', 'are', 'the', 'and', 'or', 'but'].includes(word.toLowerCase())
        );
        
        let title;
        if (keyTerms.length > 0) {
            title = keyTerms.slice(0, 3).join(' ');
        } else {
            title = cleanMessage;
        }
        
        // Limit title length
        if (title.length > 50) {
            title = title.substring(0, 47) + '...';
        }
        
        return title || 'New Chat';
    }

    /**
     * Add a message to a chat session
     */
    addMessage(sessionId, role, content, metadata = null) {
        if (!sessionId) {
            sessionId = this.createNewSession();
        }

        if (!this.sessions[sessionId]) {
            this.sessions[sessionId] = {
                id: sessionId,
                title: 'New Chat',
                created: new Date().toISOString(),
                lastUpdated: new Date().toISOString(),
                messages: [],
                settings: {
                    provider: 'openai',
                    numResults: 5
                }
            };
        }

        const message = {
            id: 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
            role: role,
            content: content,
            timestamp: new Date().toISOString(),
            metadata: metadata
        };

        this.sessions[sessionId].messages.push(message);
        this.sessions[sessionId].lastUpdated = new Date().toISOString();

        // Update title if this is the first user message
        if (role === 'user' && this.sessions[sessionId].messages.filter(m => m.role === 'user').length === 1) {
            this.sessions[sessionId].title = this.generateChatTitle(content);
        }

        this.saveSessions();
        return message;
    }

    /**
     * Get a chat session by ID
     */
    getSession(sessionId) {
        return this.sessions[sessionId] || null;
    }

    /**
     * Get all chat sessions sorted by last update
     */
    getAllSessions() {
        return Object.values(this.sessions).sort((a, b) => 
            new Date(b.lastUpdated) - new Date(a.lastUpdated)
        );
    }

    /**
     * Delete a chat session
     */
    deleteSession(sessionId) {
        if (this.sessions[sessionId]) {
            delete this.sessions[sessionId];
            this.saveSessions();
            
            // If we deleted the current session, create a new one
            if (this.currentSessionId === sessionId) {
                this.createNewSession();
            }
        }
    }

    /**
     * Switch to a different chat session
     */
    switchToSession(sessionId) {
        if (this.sessions[sessionId]) {
            this.currentSessionId = sessionId;
            this.updateChatHistoryDisplay();
            return this.sessions[sessionId];
        }
        return null;
    }

    /**
     * Initialize the chat interface
     */
    initializeChat() {
        // Initialize with a new session if none exists
        if (Object.keys(this.sessions).length === 0) {
            this.createNewSession();
        } else {
            // Load the most recent session
            const recentSession = this.getAllSessions()[0];
            this.currentSessionId = recentSession.id;
        }
        
        // Update the UI
        this.updateChatHistoryDisplay();
    }

    /**
     * Update the chat history display in the sidebar
     */
    updateChatHistoryDisplay() {
        const container = document.getElementById('chat-history-container');
        if (!container) return;

        const sessions = this.getAllSessions();
        
        if (sessions.length === 0) {
            container.innerHTML = '<div class="no-chats">No chat history yet</div>';
            return;
        }

        let html = '';
        sessions.forEach(session => {
            const isActive = session.id === this.currentSessionId;
            const date = new Date(session.lastUpdated).toLocaleDateString();
            const preview = session.messages.length > 0 
                ? session.messages.find(m => m.role === 'user')?.content?.substring(0, 50) + '...' 
                : 'No messages yet';

            html += `
                <div class="chat-history-item ${isActive ? 'active' : ''}" 
                     data-session-id="${session.id}"
                     onclick="chatManager.switchToSession('${session.id}')">
                    <div class="chat-history-title">${session.title}</div>
                    <div class="chat-history-preview">${preview}</div>
                    <div class="chat-history-date">${date}</div>
                    <button class="delete-chat-btn" onclick="event.stopPropagation(); chatManager.deleteSession('${session.id}')" title="Delete chat">
                        🗑️
                    </button>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    /**
     * Export chat history as JSON
     */
    exportChatHistory() {
        try {
            const dataStr = JSON.stringify(this.sessions, null, 2);
            const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
            
            const exportFileDefaultName = 'opteee_chat_history_' + new Date().toISOString().split('T')[0] + '.json';
            
            const linkElement = document.createElement('a');
            linkElement.setAttribute('href', dataUri);
            linkElement.setAttribute('download', exportFileDefaultName);
            linkElement.click();
            
            this.showNotification('Chat history exported successfully!', 'success');
        } catch (error) {
            console.error('Error exporting chat history:', error);
            this.showNotification('Error exporting chat history', 'error');
        }
    }

    /**
     * Import chat history from JSON file
     */
    importChatHistory(file) {
        return new Promise((resolve, reject) => {
            if (!file) {
                reject(new Error('No file selected'));
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const imported = JSON.parse(e.target.result);
                    
                    // Validate the imported data
                    if (typeof imported !== 'object' || imported === null) {
                        throw new Error('Invalid file format');
                    }
                    
                    // Merge with existing sessions
                    this.sessions = { ...this.sessions, ...imported };
                    this.saveSessions();
                    
                    this.showNotification('Chat history imported successfully!', 'success');
                    resolve(true);
                } catch (error) {
                    console.error('Error importing chat history:', error);
                    this.showNotification('Error importing chat history: ' + error.message, 'error');
                    reject(error);
                }
            };
            reader.readAsText(file);
        });
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        this.isTyping = true;
        // This would be implemented with Gradio's chat interface
        console.log('Showing typing indicator...');
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        this.isTyping = false;
        // This would be implemented with Gradio's chat interface
        console.log('Hiding typing indicator...');
    }

    /**
     * Show notification to user
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }

    /**
     * Search within chat history
     */
    searchChats(query) {
        if (!query.trim()) {
            this.updateChatHistoryDisplay();
            return;
        }

        const sessions = this.getAllSessions();
        const filteredSessions = sessions.filter(session => {
            // Search in title
            if (session.title.toLowerCase().includes(query.toLowerCase())) {
                return true;
            }
            
            // Search in messages
            return session.messages.some(message => 
                message.content.toLowerCase().includes(query.toLowerCase())
            );
        });

        this.displayFilteredSessions(filteredSessions);
    }

    /**
     * Display filtered chat sessions
     */
    displayFilteredSessions(sessions) {
        const container = document.getElementById('chat-history-container');
        if (!container) return;

        if (sessions.length === 0) {
            container.innerHTML = '<div class="no-chats">No matching chats found</div>';
            return;
        }

        let html = '';
        sessions.forEach(session => {
            const isActive = session.id === this.currentSessionId;
            const date = new Date(session.lastUpdated).toLocaleDateString();
            const preview = session.messages.length > 0 
                ? session.messages.find(m => m.role === 'user')?.content?.substring(0, 50) + '...' 
                : 'No messages yet';

            html += `
                <div class="chat-history-item ${isActive ? 'active' : ''}" 
                     data-session-id="${session.id}"
                     onclick="chatManager.switchToSession('${session.id}')">
                    <div class="chat-history-title">${session.title}</div>
                    <div class="chat-history-preview">${preview}</div>
                    <div class="chat-history-date">${date}</div>
                    <button class="delete-chat-btn" onclick="event.stopPropagation(); chatManager.deleteSession('${session.id}')" title="Delete chat">
                        🗑️
                    </button>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    /**
     * Setup event listeners for keyboard shortcuts and other interactions
     */
    setupEventListeners() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + N: New chat
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                this.createNewSession();
            }
            
            // Ctrl/Cmd + E: Export chat history
            if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
                e.preventDefault();
                this.exportChatHistory();
            }
            
            // Escape: Clear search
            if (e.key === 'Escape') {
                const searchInput = document.getElementById('chat-search');
                if (searchInput) {
                    searchInput.value = '';
                    this.updateChatHistoryDisplay();
                }
            }
        });

        // Auto-save on page unload
        window.addEventListener('beforeunload', () => {
            this.saveSessions();
        });

        // Auto-save periodically
        setInterval(() => {
            this.saveSessions();
        }, 30000); // Save every 30 seconds
    }

    /**
     * Get current session settings
     */
    getCurrentSettings() {
        const session = this.getSession(this.currentSessionId);
        return session ? session.settings : { provider: 'openai', numResults: 5 };
    }

    /**
     * Update current session settings
     */
    updateCurrentSettings(settings) {
        if (this.currentSessionId && this.sessions[this.currentSessionId]) {
            this.sessions[this.currentSessionId].settings = { ...this.sessions[this.currentSessionId].settings, ...settings };
            this.saveSessions();
        }
    }

    /**
     * Get statistics about chat usage
     */
    getStats() {
        const sessions = this.getAllSessions();
        const totalMessages = sessions.reduce((sum, session) => sum + session.messages.length, 0);
        const totalChats = sessions.length;
        const averageMessagesPerChat = totalChats > 0 ? Math.round(totalMessages / totalChats) : 0;
        
        return {
            totalChats,
            totalMessages,
            averageMessagesPerChat,
            oldestChat: sessions.length > 0 ? sessions[sessions.length - 1].created : null,
            newestChat: sessions.length > 0 ? sessions[0].created : null
        };
    }
}

// Global chat manager instance
let chatManager = null;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 OPTEEE Chat Interface loaded');
    chatManager = new ChatManager();
    
    // Setup additional UI interactions
    setupUIInteractions();
});

/**
 * Setup additional UI interactions
 */
function setupUIInteractions() {
    // Add search functionality
    const searchInput = document.getElementById('chat-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            chatManager.searchChats(e.target.value);
        });
    }

    // Add export/import functionality
    const exportBtn = document.getElementById('export-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            chatManager.exportChatHistory();
        });
    }

    const importBtn = document.getElementById('import-btn');
    const importFile = document.getElementById('import-file');
    if (importBtn && importFile) {
        importBtn.addEventListener('click', () => {
            importFile.click();
        });
        
        importFile.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                chatManager.importChatHistory(file);
            }
        });
    }
}

/**
 * Helper functions for Gradio integration
 */

// Create a new chat session
function createNewChat() {
    if (chatManager) {
        const sessionId = chatManager.createNewSession();
        return [[], sessionId]; // Return empty chat history and new session ID
    }
    return [[], null];
}

// Load a chat session
function loadChatSession(sessionId) {
    if (chatManager) {
        const session = chatManager.getSession(sessionId);
        if (session) {
            chatManager.currentSessionId = sessionId;
            return session.messages.map(msg => ({
                role: msg.role,
                content: msg.content,
                metadata: msg.metadata
            }));
        }
    }
    return [];
}

// Save a chat message
function saveChatMessage(sessionId, role, content, metadata = null) {
    if (chatManager) {
        return chatManager.addMessage(sessionId, role, content, metadata);
    }
    return null;
}

// Get all chat sessions
function getChatSessions() {
    if (chatManager) {
        return chatManager.getAllSessions();
    }
    return [];
}

// Delete a chat session
function deleteChatSession(sessionId) {
    if (chatManager) {
        chatManager.deleteSession(sessionId);
        return chatManager.getAllSessions();
    }
    return [];
}

// Export chat history
function exportChatHistory() {
    if (chatManager) {
        chatManager.exportChatHistory();
    }
}

// Import chat history
function importChatHistory(file) {
    if (chatManager) {
        return chatManager.importChatHistory(file);
    }
    return Promise.reject(new Error('Chat manager not initialized'));
}

// Show typing indicator
function showTypingIndicator() {
    if (chatManager) {
        chatManager.showTypingIndicator();
    }
}

// Hide typing indicator
function hideTypingIndicator() {
    if (chatManager) {
        chatManager.hideTypingIndicator();
    }
}

/**
 * Copy text to clipboard with visual feedback
 */
function copyToClipboard(text, buttonElement) {
    console.log('Copying text:', text); // Debug log
    
    // Use the modern Clipboard API if available
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function() {
            // Visual feedback - change icon temporarily
            const originalContent = buttonElement.innerHTML;
            buttonElement.innerHTML = '✅';
            buttonElement.style.color = '#28a745';
            buttonElement.style.background = '#e8f5e8';
            
            // Reset after 2 seconds
            setTimeout(() => {
                buttonElement.innerHTML = originalContent;
                buttonElement.style.color = '';
                buttonElement.style.background = '';
            }, 2000);
            
            console.log('✅ Text copied successfully');
        }).catch(function(err) {
            console.error('Clipboard API failed:', err);
            fallbackCopy(text, buttonElement);
        });
    } else {
        // Use fallback for older browsers or non-secure contexts
        fallbackCopy(text, buttonElement);
    }
}

/**
 * Fallback copy method for older browsers
 */
function fallbackCopy(text, buttonElement) {
    try {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
        
        if (successful) {
            // Visual feedback
            const originalContent = buttonElement.innerHTML;
            buttonElement.innerHTML = '✅';
            buttonElement.style.color = '#28a745';
            buttonElement.style.background = '#e8f5e8';
            
            setTimeout(() => {
                buttonElement.innerHTML = originalContent;
                buttonElement.style.color = '';
                buttonElement.style.background = '';
            }, 2000);
            
            console.log('✅ Text copied successfully (fallback)');
        } else {
            throw new Error('execCommand failed');
        }
    } catch (fallbackErr) {
        console.error('Fallback copy failed:', fallbackErr);
        
        // Show error feedback
        const originalContent = buttonElement.innerHTML;
        buttonElement.innerHTML = '❌';
        buttonElement.style.color = '#dc3545';
        
        setTimeout(() => {
            buttonElement.innerHTML = originalContent;
            buttonElement.style.color = '';
        }, 2000);
        
        alert('Failed to copy link. Please copy manually: ' + text);
    }
}

// Global utility functions - make sure they're available immediately
window.copyToClipboard = copyToClipboard;
window.chatManager = chatManager;
window.createNewChat = createNewChat;
window.loadChatSession = loadChatSession;
window.saveChatMessage = saveChatMessage;
window.getChatSessions = getChatSessions;
window.deleteChatSession = deleteChatSession;
window.exportChatHistory = exportChatHistory;
window.importChatHistory = importChatHistory;
window.showTypingIndicator = showTypingIndicator;
window.hideTypingIndicator = hideTypingIndicator; 