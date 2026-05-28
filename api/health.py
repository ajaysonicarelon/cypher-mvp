"""
Vercel Serverless Function: Health Check Endpoint
Returns system status and configuration
"""

import json
import os

def handler(request):
    """Vercel serverless function handler - Modern format"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
    
    # Handle GET
    if request.method == 'GET':
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
            
            # Return response
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(response, indent=2)
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'status': 'error',
                    'error': str(e)
                })
            }
    
    # Method not allowed
    return {
        'statusCode': 405,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': 'Method not allowed'})
    }
