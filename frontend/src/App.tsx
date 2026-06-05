import React, { useState, useEffect, useRef } from 'react';
import './App.css';

// Lean IDS imports
import { 
  Button, 
  InputField, 
  Chip, 
  Avatar, 
  Breadcrumbs,
  SideNavigation,
  MenuItem,
  Icon,
  PageLayout,
  TopHeader,
  ThemeProvider,
  Badge,
  AddIcon,
  SettingsIcon
} from '@ajaysoni7832/lean-ids-components';

// Import theme tokens
import { carelonTheme } from '@ajaysoni7832/lean-ids-tokens';

// Import custom icons
import { HomeIcon, DatabaseIcon, ChatIcon } from './components/CustomIcons';
import InSyncHome from './pages/InSyncHome';
import AdminDashboard from './pages/admin/AdminDashboard';

interface Message {
  text: string;
  isUser: boolean;
  confidence?: number;
  mediaUrl?: string | null;
}

const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT || 'http://localhost:8000/chat';

const SUGGESTIONS = [
  { label: 'Onboarding Steps?', question: 'Show me the complete onboarding checklist' },
  { label: 'Laptop Allocation?', question: 'How do I get my laptop?' },
  { label: 'What do I need on Day 1?', question: 'What documents do I need on Day 1?' },
  { label: 'First week schedule?', question: 'What is my first week schedule?' },
  { label: 'Design Sync Meeting?', question: 'What is a design sync?' },
  { label: 'Training Modules?', question: 'What training modules do I need to complete?' },
];

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showWelcome, setShowWelcome] = useState(true);
  const [currentPage, setCurrentPage] = useState<'chat' | 'insync' | 'admin'>('chat');
  const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatMarkdown = (text: string): string => {
    // Process line by line first
    const lines = text.split('\n');
    const formattedLines = lines.map((line) => {
      // Numbered lists
      if (/^\d+\.\s/.test(line)) {
        return `<div class="list-item numbered">${line}</div>`;
      }
      // Bullet lists (with - or •)
      if (/^[-•]\s/.test(line)) {
        return `<div class="list-item bullet">${line}</div>`;
      }
      // Indented lists
      if (/^\s{2,}[-•]\s/.test(line)) {
        return `<div class="list-item indented">${line.trim()}</div>`;
      }
      // Empty lines
      if (line.trim() === '') {
        return '<div class="line-break"></div>';
      }
      // Regular text
      return `<div class="text-line">${line}</div>`;
    });

    let formatted = formattedLines.join('');

    // Convert URLs to clickable links
    const urlPattern = /(https?:\/\/[^\s<]+)/g;
    formatted = formatted.replace(urlPattern, '<a href="$1" target="_blank" rel="noopener noreferrer" class="message-link">$1</a>');

    // Apply inline formatting
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');

    return formatted;
  };

  const sendMessage = async (messageText?: string) => {
    const text = messageText || inputValue.trim();
    if (!text) return;

    // Hide welcome and suggestions after first message
    if (showWelcome) {
      setShowWelcome(false);
    }

    // Add user message
    setMessages((prev) => [...prev, { text, isUser: true }]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: text,
          session_id: sessionId 
        }),
      });

      const data = await response.json();

      // Add bot response
      setMessages((prev) => [
        ...prev,
        {
          text: data.reply,
          isUser: false,
          confidence: data.confidence,
          mediaUrl: data.media_url,
        },
      ]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [
        ...prev,
        {
          text: 'Sorry, I encountered an error. Please try again.',
          isUser: false,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <ThemeProvider theme={carelonTheme}>
      <PageLayout
        variant="sidebar-only"
        pageTitle=""
        breadcrumbs={[]}
        sideNav={{
          groups: [
            {
              title: 'BASICS',
              items: [
                { id: 'home', label: 'Home', icon: <HomeIcon size="medium" color="white" />, onClick: () => {} },
                { id: 'database', label: 'Database', icon: <DatabaseIcon size="medium" color="white" />, onClick: () => {} },
                { id: 'chat', label: 'Chat', icon: <ChatIcon size="medium" color="white" />, active: true, onClick: () => {} }
              ]
            },
            {
              title: 'PRODUCTS',
              items: [
                { 
                  id: 'insync', 
                  label: 'InSync BCP', 
                  icon: <SettingsIcon size="medium" color="white" />, 
                  active: currentPage === 'insync',
                  onClick: () => setCurrentPage('insync')
                },
                { 
                  id: 'admin', 
                  label: 'Admin Dashboard', 
                  icon: <SettingsIcon size="medium" color="white" />, 
                  active: currentPage === 'admin',
                  onClick: () => setCurrentPage('admin')
                },
                { id: 'add-product', label: 'Add Product', icon: <AddIcon size="medium" color="white" />, onClick: () => {} }
              ]
            }
          ],
          user: {
            name: 'Ajay Soni',
            subtitle: 'AM07832',
            initials: 'AS'
          }
        }}
      >
        {currentPage === 'admin' ? (
          <AdminDashboard />
        ) : currentPage === 'insync' ? (
          <InSyncHome />
        ) : showWelcome ? (
          <div className="empty-state-container">
            <div className="empty-state-content">
              <h1 className="empty-state-title">Welcome to Cypher!</h1>
              <p className="empty-state-subtitle">
                I can help you with everything you need to know about joining the team!
              </p>
              
              <div className="empty-state-input">
                <InputField
                  placeholder="Start typing your prompt here..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  disabled={isLoading}
                  helperText="You can attach Confluence page link, Figma frame link to ask questions"
                  leadingIcon={<AddIcon size="medium" />}
                  trailingIcon={
                    <Button
                      onClick={() => sendMessage()}
                      disabled={isLoading || !inputValue.trim()}
                      variant="primary"
                      size="small"
                    >
                      ↑
                    </Button>
                  }
                  fullWidth
                />
              </div>

              <div className="empty-state-suggestions">
                {SUGGESTIONS.map((suggestion, index) => (
                  <Chip
                    key={index}
                    label={suggestion.label}
                    onClick={() => sendMessage(suggestion.question)}
                    type="default"
                    variant="outlined"
                  />
                ))}
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <div key={index} className={`chat-message ${message.isUser ? 'user-message' : 'bot-message'}`}>
                {message.isUser ? (
                  <div className="message-text">{message.text}</div>
                ) : (
                  <div className="message-text">
                    <div dangerouslySetInnerHTML={{ __html: formatMarkdown(message.text) }} />
                    {message.confidence !== undefined && (
                      <div style={{ marginTop: '8px' }}>
                        <Badge 
                          label={`Confidence: ${(message.confidence * 100).toFixed(1)}%`}
                          type="info"
                          style="subdued"
                        />
                      </div>
                    )}
                  </div>
                )}
                {message.mediaUrl && (
                  <img src={message.mediaUrl} alt="Response" className="message-image" />
                )}
              </div>
            ))}
            {isLoading && (
              <div className="chat-message bot-message">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />

            <div className="input-field-sticky">
              <InputField
                placeholder="Start typing your prompt here......"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
                helperText="You can attach Confluence page link, Figma frame link, or ask any question"
                leadingIcon={<AddIcon size="medium" />}
                trailingIcon={
                  <Button
                    onClick={() => sendMessage()}
                    disabled={isLoading || !inputValue.trim()}
                    variant="primary"
                    size="small"
                  >
                    ↑
                  </Button>
                }
                fullWidth
              />
            </div>
          </>
        )}
    </PageLayout>
    </ThemeProvider>
  );
}

export default App;
