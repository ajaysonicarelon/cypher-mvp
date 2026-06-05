# Cypher Chatbot Widget - Integration Guide

## Quick Integration (2 Steps)

### Step 1: Add Widget Script
Add this script tag to your website's HTML (before the closing `</body>` tag):

```html
<script src="https://your-cdn-url.com/cypher-widget.umd.js"></script>
```

### Step 2: Initialize Widget
Add this script after the widget script:

```html
<script>
  Cypher.init({
    apiKey: 'your-api-key',
    widgetId: 'your-widget-id',
    theme: {
      primaryColor: '#5009B5',
      position: 'bottom-right'
    }
  });
</script>
```

## Configuration Options

### Required Parameters
- `apiKey`: Your unique API key (get from admin dashboard)
- `widgetId`: Your widget ID (get from admin dashboard)

### Optional Theme Options
```javascript
theme: {
  primaryColor: '#5009B5',      // Primary brand color
  position: 'bottom-right',     // 'bottom-right' or 'bottom-left'
  welcomeMessage: 'Hi! How can I help you today?',
  headerText: 'Chat Support'
}
```

## Getting Your API Key

1. Contact Cypher team to set up your account
2. Access the admin dashboard
3. Create a product (your website domain)
4. Create a widget for your product
5. Click "Generate" to create an API key
6. Copy the API key and use it in the initialization

## Testing Integration

1. Add the widget script to your staging environment
2. Initialize with your API key
3. The widget should appear in the bottom-right corner
4. Test the chat functionality
5. Verify responses match your knowledge base

## Troubleshooting

### Widget Not Appearing
- Check browser console for errors
- Verify the CDN URL is correct
- Ensure API key is valid

### API Key Errors
- Verify API key is active in admin dashboard
- Check that your domain is whitelisted
- Contact support if issues persist

### Chat Not Working
- Verify backend API is running
- Check CORS settings
- Ensure knowledge base is configured

## Support

For integration support, contact:
- Email: support@cypher.com
- Admin Dashboard: https://admin.cypher.com
