"""
Netlify Serverless Function: Health Check
"""
import json
import os

def handler(event, context):
    """Netlify function handler"""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    supabase_url = os.environ.get('SUPABASE_URL', '')
    supabase_key = os.environ.get('SUPABASE_KEY', '')
    
    response = {
        'status': 'healthy' if (supabase_url and supabase_key) else 'degraded',
        'environment': {
            'supabase_url_configured': bool(supabase_url),
            'supabase_key_configured': bool(supabase_key),
            'confidence_threshold': float(os.environ.get('CONFIDENCE_THRESHOLD', '0.40'))
        },
        'message': 'AI Chatbot API is running on Netlify',
        'version': '2.0.0'
    }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(response, indent=2)
    }
