# Cypher Widget SDK

Pluggable, configurable chatbot widget for any web application.

## Installation

### Vanilla HTML/JS
```html
<script src="https://cdn.cypher.ai/cypher-widget.umd.js"></script>
<script>
  Cypher.init({
    apiEndpoint: 'https://api.yourdomain.com/chat',
    apiKey: 'your-api-key',
    widgetId: 'your-widget-id'
  });
</script>
```

### React
```javascript
import { useEffect } from 'react';

function App() {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdn.cypher.ai/cypher-widget.umd.js';
    script.onload = () => {
      window.Cypher.init({
        apiEndpoint: 'https://api.yourdomain.com/chat',
        apiKey: 'your-api-key',
        widgetId: 'your-widget-id'
      });
    };
    document.body.appendChild(script);
  }, []);

  return <div>Your App</div>;
}
```

## Configuration

```javascript
Cypher.init({
  // Required
  apiEndpoint: 'https://api.yourdomain.com/chat',
  apiKey: 'your-api-key',
  widgetId: 'your-widget-id',
  
  // Optional
  productName: 'Your Product Name',
  productContext: 'general',
  theme: {
    primaryColor: '#5009B5',
    accentColor: '#00D9FF',
    backgroundColor: '#0A0A1F',
    textColor: '#FFFFFF',
    position: 'bottom-right'
  },
  welcomeMessage: 'Custom welcome message',
  suggestions: [
    { label: 'Help', question: 'How can you help?' }
  ],
  position: 'bottom-right',
  enabledFeatures: {
    accessibility: true,
    translation: true,
    resetChat: true
  }
});
```

## Development

```bash
npm install
npm run dev    # Watch mode
npm run build  # Build for production
```

## API Methods

```javascript
const widget = Cypher.init(config);

widget.open();    // Open chat window
widget.close();   // Close chat window
widget.destroy(); // Remove widget from DOM
```
