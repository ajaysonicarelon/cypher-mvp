/**
 * Cypher Chatbot Widget SDK
 * Pluggable, configurable chatbot widget for any web application
 */

(function() {
  'use strict';

  class CypherWidget {
    constructor(config) {
      // Default configuration
      this.config = {
        apiEndpoint: config.apiEndpoint || 'http://localhost:8000/chat',
        apiKey: config.apiKey || '',
        widgetId: config.widgetId || 'default',
        productName: config.productName || 'Cypher',
        productContext: config.productContext || 'general',
        theme: config.theme || {
          primaryColor: '#5009B5',
          accentColor: '#00D9FF',
          backgroundColor: '#0A0A1F',
          textColor: '#FFFFFF',
          position: 'bottom-right'
        },
        welcomeMessage: config.welcomeMessage || 'Cypher here. I see you need guidance. How can I help you?',
        suggestions: config.suggestions || [
          { label: 'How can you help?', question: 'What can you help me with?' },
          { label: 'Getting started', question: 'How do I get started?' }
        ],
        position: config.position || 'bottom-right',
        enabledFeatures: config.enabledFeatures || {
          accessibility: true,
          translation: true,
          resetChat: true
        }
      };

      // Generate unique session ID
      this.sessionId = `cypher_${this.config.widgetId}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      // Initialize widget
      this.init();
    }

    init() {
      // Check if widget already exists
      if (document.getElementById('cypher-chatbot-widget')) {
        console.warn('Cypher widget already initialized');
        return;
      }

      // Create and inject widget
      this.createWidget();
      this.injectStyles();
      this.attachEventListeners();
      
      console.log('✅ Cypher widget initialized:', this.config.widgetId);
    }

    createWidget() {
      const widgetHTML = `
        <div id="cypher-chatbot-widget">
          <!-- FAB Button -->
          <button id="cypher-fab" class="cypher-fab" aria-label="Activate ${this.config.productName}" title="${this.config.productName}">
            <div class="cypher-fab-hat-shadow"></div>
            <svg class="cypher-eye-icon" width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="eyeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:${this.config.theme.primaryColor};stop-opacity:1" />
                  <stop offset="100%" style="stop-color:${this.config.theme.accentColor};stop-opacity:1" />
                </linearGradient>
                <linearGradient id="irisGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#4A90E2;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:${this.config.theme.primaryColor};stop-opacity:1" />
                </linearGradient>
              </defs>
              <ellipse cx="16" cy="16" rx="14" ry="10" fill="url(#eyeGradient)" stroke="${this.config.theme.accentColor}" stroke-width="1.5"/>
              <ellipse cx="16" cy="16" rx="11" ry="7.5" fill="#E8F4FF"/>
              <circle cx="16" cy="16" r="5" fill="url(#irisGradient)"/>
              <circle cx="16" cy="16" r="2.5" fill="#0A0A1F"/>
              <circle cx="17" cy="14.5" r="1.5" fill="white" opacity="0.8"/>
            </svg>
          </button>

          <!-- Chat Window -->
          <div id="cypher-chat-window" class="cypher-chat-window cypher-hidden">
            <!-- Header -->
            <div class="cypher-chat-header">
              <div class="cypher-header-left">
                <div class="cypher-header-icon">
                  <svg width="24" height="24" viewBox="0 0 32 32" fill="none">
                    <ellipse cx="16" cy="16" rx="14" ry="10" fill="url(#eyeGradient)" stroke="${this.config.theme.accentColor}" stroke-width="1.5"/>
                    <ellipse cx="16" cy="16" rx="11" ry="7.5" fill="#E8F4FF"/>
                    <circle cx="16" cy="16" r="5" fill="url(#irisGradient)"/>
                    <circle cx="16" cy="16" r="2.5" fill="#0A0A1F"/>
                  </svg>
                </div>
                <div class="cypher-header-text">
                  <h3>${this.config.productName}</h3>
                  <p>Your Pathfinder</p>
                </div>
              </div>
              <div class="cypher-header-actions">
                ${this.config.enabledFeatures.resetChat ? `
                <button id="cypher-reset-chat-btn" class="cypher-icon-btn" aria-label="Reset chat" title="Reset Chat">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                    <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4C7.58 4 4.01 7.58 4.01 12C4.01 16.42 7.58 20 12 20C15.73 20 18.84 17.45 19.73 14H17.65C16.83 16.33 14.61 18 12 18C8.69 18 6 15.31 6 12C6 8.69 8.69 6 12 6C13.66 6 15.14 6.69 16.22 7.78L13 11H20V4L17.65 6.35Z"/>
                  </svg>
                </button>
                ` : ''}
                ${this.config.enabledFeatures.accessibility ? `
                <button id="cypher-accessibility-btn" class="cypher-icon-btn" aria-label="Accessibility settings" title="Accessibility">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM11 19.93C7.05 19.44 4 16.08 4 12C4 11.38 4.08 10.79 4.21 10.21L9 15V16C9 17.1 9.9 18 11 18V19.93ZM17.9 17.39C17.64 16.58 16.9 16 16 16H15V13C15 12.45 14.55 12 14 12H8V10H10V8H8V6H12V4H13C13.55 4 14 4.45 14 5V9H16C16.55 9 17 9.45 17 10V11.5C17 11.5 17.9 17.39 17.9 17.39Z"/>
                  </svg>
                </button>
                ` : ''}
                <button id="cypher-close-btn" class="cypher-icon-btn" aria-label="Close chat" title="Close">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                    <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Tabs -->
            <div class="cypher-tabs">
              <button class="cypher-tab cypher-tab-active" data-tab="chat">Chat</button>
              ${this.config.enabledFeatures.accessibility ? `
              <button class="cypher-tab" data-tab="accessibility">Toolkit</button>
              ` : ''}
            </div>

            <!-- Chat Tab Content -->
            <div id="cypher-chat-content" class="cypher-tab-content cypher-tab-content-active">
              <div id="cypher-messages" class="cypher-messages">
                <div class="cypher-welcome-message">
                  <h4>Cypher here. I see you need guidance.</h4>
                  <p>${this.config.welcomeMessage}</p>
                </div>
                <div class="cypher-suggestions">
                  ${this.config.suggestions.map(s => `
                    <button class="cypher-suggestion-chip" data-question="${s.question}">
                      ${s.label}
                    </button>
                  `).join('')}
                </div>
              </div>
              <div class="cypher-input-area">
                <input type="text" id="cypher-input" placeholder="Type your message..." aria-label="Type your message">
                <button id="cypher-send-btn" aria-label="Send message">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                    <path d="M2.01 21L23 12L2.01 3L2 10L15 12L2 14L2.01 21Z"/>
                  </svg>
                </button>
              </div>
            </div>

            ${this.config.enabledFeatures.accessibility ? `
            <!-- Accessibility Tab Content -->
            <div id="cypher-accessibility-content" class="cypher-tab-content cypher-accessibility-panel">
              <div class="cypher-accessibility-header">
                <h3>Cypher's Toolkit</h3>
                <p>Deploy gadgets to optimize your vision</p>
              </div>
              <!-- Accessibility features will be added here -->
            </div>
            ` : ''}
          </div>
        </div>
      `;

      document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }

    injectStyles() {
      const styleId = 'cypher-widget-styles';
      if (document.getElementById(styleId)) return;

      const styles = `
        <style id="${styleId}">
          #cypher-chatbot-widget {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            position: fixed;
            z-index: 999999;
          }

          .cypher-fab {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: none;
            background: ${this.config.theme.primaryColor};
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
          }

          .cypher-fab:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(0, 0, 0, 0.4);
          }

          .cypher-fab:active {
            transform: scale(0.95);
          }

          .cypher-chat-window {
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 380px;
            height: 600px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
            display: flex;
            flex-direction: column;
            transition: all 0.3s ease;
            overflow: hidden;
          }

          .cypher-hidden {
            display: none !important;
          }

          .cypher-chat-header {
            background: ${this.config.theme.primaryColor};
            color: white;
            padding: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
          }

          .cypher-header-left {
            display: flex;
            align-items: center;
            gap: 12px;
          }

          .cypher-header-text h3 {
            margin: 0;
            font-size: 18px;
            font-weight: 600;
          }

          .cypher-header-text p {
            margin: 0;
            font-size: 12px;
            opacity: 0.9;
          }

          .cypher-header-actions {
            display: flex;
            gap: 8px;
          }

          .cypher-icon-btn {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            border-radius: 8px;
            padding: 8px;
            cursor: pointer;
            transition: background 0.2s;
          }

          .cypher-icon-btn:hover {
            background: rgba(255, 255, 255, 0.3);
          }

          .cypher-tabs {
            display: flex;
            border-bottom: 1px solid #e0e0e0;
          }

          .cypher-tab {
            flex: 1;
            padding: 12px;
            border: none;
            background: white;
            cursor: pointer;
            font-weight: 500;
            color: #666;
            transition: all 0.2s;
          }

          .cypher-tab-active {
            color: ${this.config.theme.primaryColor};
            border-bottom: 2px solid ${this.config.theme.primaryColor};
          }

          .cypher-tab-content {
            flex: 1;
            display: none;
            overflow-y: auto;
          }

          .cypher-tab-content-active {
            display: flex;
            flex-direction: column;
          }

          .cypher-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
          }

          .cypher-welcome-message {
            text-align: center;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 12px;
            margin-bottom: 16px;
          }

          .cypher-welcome-message h4 {
            margin: 0 0 8px 0;
            color: ${this.config.theme.primaryColor};
          }

          .cypher-welcome-message p {
            margin: 0;
            color: #666;
            font-size: 14px;
          }

          .cypher-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 16px;
          }

          .cypher-suggestion-chip {
            background: ${this.config.theme.primaryColor};
            color: white;
            border: none;
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
          }

          .cypher-suggestion-chip:hover {
            background: ${this.config.theme.accentColor};
            transform: translateY(-2px);
          }

          .cypher-input-area {
            display: flex;
            gap: 8px;
            padding: 16px;
            border-top: 1px solid #e0e0e0;
          }

          .cypher-input-area input {
            flex: 1;
            padding: 12px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
          }

          .cypher-input-area input:focus {
            outline: none;
            border-color: ${this.config.theme.primaryColor};
          }

          .cypher-input-area button {
            background: ${this.config.theme.primaryColor};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 16px;
            cursor: pointer;
            transition: background 0.2s;
          }

          .cypher-input-area button:hover {
            background: ${this.config.theme.accentColor};
          }

          .cypher-accessibility-panel {
            padding: 16px;
            overflow-y: auto;
          }

          .cypher-accessibility-header {
            text-align: center;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 12px;
            margin-bottom: 16px;
          }

          .cypher-accessibility-header h3 {
            margin: 0 0 8px 0;
            color: ${this.config.theme.primaryColor};
          }

          .cypher-accessibility-header p {
            margin: 0;
            color: #666;
            font-size: 14px;
          }

          @media (max-width: 480px) {
            .cypher-chat-window {
              width: calc(100vw - 40px);
              height: calc(100vh - 100px);
              bottom: 80px;
              right: 20px;
            }
          }
        </style>
      `;

      document.head.insertAdjacentHTML('beforeend', styles);
    }

    attachEventListeners() {
      const fab = document.getElementById('cypher-fab');
      const chatWindow = document.getElementById('cypher-chat-window');
      const closeBtn = document.getElementById('cypher-close-btn');
      const input = document.getElementById('cypher-input');
      const sendBtn = document.getElementById('cypher-send-btn');
      const tabs = document.querySelectorAll('.cypher-tab');
      const resetBtn = document.getElementById('cypher-reset-chat-btn');
      const accessibilityBtn = document.getElementById('cypher-accessibility-btn');

      // Toggle chat window
      if (fab) {
        fab.addEventListener('click', () => {
          chatWindow.classList.toggle('cypher-hidden');
          if (!chatWindow.classList.contains('cypher-hidden')) {
            input.focus();
          }
        });
      }

      // Close button
      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          chatWindow.classList.add('cypher-hidden');
        });
      }

      // Tab switching
      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          const tabName = tab.dataset.tab;
          
          tabs.forEach(t => t.classList.remove('cypher-tab-active'));
          tab.classList.add('cypher-tab-active');
          
          document.querySelectorAll('.cypher-tab-content').forEach(content => {
            content.classList.remove('cypher-tab-content-active');
          });
          
          document.getElementById(`cypher-${tabName}-content`).classList.add('cypher-tab-content-active');
        });
      });

      // Send message
      const sendMessage = () => {
        const message = input.value.trim();
        if (message) {
          this.sendMessage(message);
          input.value = '';
        }
      };

      if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
      }

      if (input) {
        input.addEventListener('keypress', (e) => {
          if (e.key === 'Enter') sendMessage();
        });
      }

      // Suggestion chips
      document.querySelectorAll('.cypher-suggestion-chip').forEach(chip => {
        chip.addEventListener('click', () => {
          const question = chip.getAttribute('data-question');
          this.sendMessage(question);
        });
      });

      // Reset chat
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          this.resetChat();
        });
      }
    }

    async sendMessage(message) {
      const messagesContainer = document.getElementById('cypher-messages');
      
      // Add user message
      this.addMessage(message, 'user');
      
      // Show loading
      const loadingId = this.addMessage('Thinking...', 'bot', true);
      
      try {
        const response = await fetch(this.config.apiEndpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': this.config.apiKey,
            'X-Widget-ID': this.config.widgetId
          },
          body: JSON.stringify({
            message: message,
            session_id: this.sessionId,
            context: this.config.productContext
          })
        });
        
        const data = await response.json();
        
        // Remove loading message
        const loadingElement = document.getElementById(loadingId);
        if (loadingElement) loadingElement.remove();
        
        // Add bot response
        this.addMessage(data.answer || 'Sorry, I could not process your request.', 'bot');
        
      } catch (error) {
        console.error('Error sending message:', error);
        
        // Remove loading message
        const loadingElement = document.getElementById(loadingId);
        if (loadingElement) loadingElement.remove();
        
        this.addMessage('Sorry, something went wrong. Please try again.', 'bot');
      }
    }

    addMessage(text, sender, isLoading = false) {
      const messagesContainer = document.getElementById('cypher-messages');
      const messageId = `msg-${Date.now()}`;
      
      const messageHTML = `
        <div id="${messageId}" class="cypher-message cypher-message-${sender} ${isLoading ? 'cypher-loading' : ''}">
          <div class="cypher-message-content">${text}</div>
        </div>
      `;
      
      messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
      
      return messageId;
    }

    resetChat() {
      const messagesContainer = document.getElementById('cypher-messages');
      if (!messagesContainer) return;

      messagesContainer.innerHTML = `
        <div class="cypher-welcome-message">
          <h4>Cypher here. I see you need guidance.</h4>
          <p>${this.config.welcomeMessage}</p>
        </div>
        <div class="cypher-suggestions">
          ${this.config.suggestions.map(s => `
            <button class="cypher-suggestion-chip" data-question="${s.question}">
              ${s.label}
            </button>
          `).join('')}
        </div>
      `;

      // Re-attach suggestion chip listeners
      document.querySelectorAll('.cypher-suggestion-chip').forEach(chip => {
        chip.addEventListener('click', () => {
          const question = chip.getAttribute('data-question');
          this.sendMessage(question);
        });
      });

      // Switch back to chat tab
      const chatTab = document.querySelector('[data-tab="chat"]');
      const accessibilityTab = document.querySelector('[data-tab="accessibility"]');
      const chatContent = document.getElementById('cypher-chat-content');
      const accessibilityContent = document.getElementById('cypher-accessibility-content');

      if (chatTab && accessibilityTab && chatContent && accessibilityContent) {
        chatTab.classList.add('cypher-tab-active');
        accessibilityTab.classList.remove('cypher-tab-active');
        chatContent.classList.add('cypher-tab-content-active');
        accessibilityContent.classList.remove('cypher-tab-content-active');
      }
    }

    // Public API methods
    open() {
      const chatWindow = document.getElementById('cypher-chat-window');
      if (chatWindow) chatWindow.classList.remove('cypher-hidden');
    }

    close() {
      const chatWindow = document.getElementById('cypher-chat-window');
      if (chatWindow) chatWindow.classList.add('cypher-hidden');
    }

    destroy() {
      const widget = document.getElementById('cypher-chatbot-widget');
      const styles = document.getElementById('cypher-widget-styles');
      if (widget) widget.remove();
      if (styles) styles.remove();
    }
  }

  // Global API
  window.Cypher = {
    init: function(config) {
      return new CypherWidget(config);
    }
  };

})();
