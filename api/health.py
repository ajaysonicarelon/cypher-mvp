"""
Vercel Serverless Function: Health Check Endpoint
Returns system status and configuration
"""

from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            # Check environment variables
            supabase_url = os.environ.get('SUPABASE_URL', '')
            supabase_key = os.environ.get('SUPABASE_KEY', '')
            
            has_supabase_url = bool(supabase_url)
            has_supabase_key = bool(supabase_key)
            
            # Build response
            response = {
                'status': 'healthy' if (has_supabase_url and has_supabase_key) else 'degraded',
                'environment': {
                    'supabase_url_configured': has_supabase_url,
                    'supabase_key_configured': has_supabase_key,
                    'confidence_threshold': float(os.environ.get('CONFIDENCE_THRESHOLD', '0.40'))
                },
                'message': 'AI Chatbot API is running on Vercel',
                'version': '2.0.0'
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'error',
                'error': str(e)
            }).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests (CORS preflight)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
