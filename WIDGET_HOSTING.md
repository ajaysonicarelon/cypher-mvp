# Widget Hosting Instructions

## Option 1: Host on Netlify (Recommended)

### Steps:
1. Create a new Netlify site
2. Upload the `cypher-widget-sdk/dist/` folder
3. Get the CDN URL from Netlify
4. Use this URL in the integration guide

### Example URL:
```
https://cypher-widget.netlify.app/cypher-widget.umd.js
```

## Option 2: Host on Cloudflare R2

### Steps:
1. Create a Cloudflare R2 bucket
2. Upload `cypher-widget-sdk/dist/` files
3. Enable public access
4. Get the CDN URL
5. Use this URL in the integration guide

### Example URL:
```
https://pub-xxxxxxxx.r2.dev/cypher-widget.umd.js
```

## Option 3: Host on GitHub Pages

### Steps:
1. Create a new GitHub repository for the widget
2. Push `cypher-widget-sdk/dist/` files
3. Enable GitHub Pages
4. Get the URL
5. Use this URL in the integration guide

### Example URL:
```
https://username.github.io/cypher-widget/cypher-widget.umd.js
```

## Option 4: Host on Your Own Server

### Steps:
1. Upload `cypher-widget-sdk/dist/` files to your server
2. Configure Nginx/Apache to serve the files
3. Enable CORS if needed
4. Get the URL
5. Use this URL in the integration guide

### Nginx Configuration:
```nginx
location /widget/ {
    alias /path/to/cypher-widget-sdk/dist/;
    add_header Access-Control-Allow-Origin *;
}
```

## Files to Host

From `cypher-widget-sdk/dist/`:
- `cypher-widget.umd.js` (18.46 kB) - Main widget file
- `cypher-widget.es.js` (20.92 kB) - ES module version
- Source maps (optional, for debugging)

## Updating the Integration Guide

After hosting, update the CDN URL in `INTEGRATION_GUIDE.md`:

```html
<script src="https://your-actual-cdn-url.com/cypher-widget.umd.js"></script>
```

## Versioning

For production, consider:
1. Using versioned filenames (e.g., `cypher-widget.v1.0.0.umd.js`)
2. Creating a symlink to the latest version
3. Implementing cache-busting strategies
