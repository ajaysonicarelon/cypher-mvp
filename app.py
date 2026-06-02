"""
Flask API for AI Chatbot - Render Deployment
Updated: 2026-06-01 - Added comprehensive onboarding data (101 Q&A pairs)
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from supabase import create_client
import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Global cache
_supabase = None
_vectorizer = None
_knowledge_vectors = None
_knowledge_base_cache = []
_initialized = False

# Session storage for conversation context
_conversation_sessions = {}

CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', '0.35'))

def get_supabase():
    """Get or create Supabase client"""
    global _supabase
    if _supabase is None:
        print("🔌 Creating Supabase client...")
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_KEY')
        print(f"🔑 SUPABASE_URL configured: {bool(url)}")
        print(f"🔑 SUPABASE_KEY configured: {bool(key)}")
        if not url or not key:
            raise Exception('SUPABASE_URL and SUPABASE_KEY must be set')
        _supabase = create_client(url, key)
        print("✅ Supabase client created")
    return _supabase

def initialize_system():
    """Initialize vectorizer and load knowledge base"""
    global _vectorizer, _knowledge_vectors, _knowledge_base_cache, _initialized
    
    if _initialized:
        print("✅ System already initialized")
        return
    
    print("🔌 Initializing system...")
    supabase = get_supabase()
    print("📊 Fetching knowledge base from Supabase...")
    result = supabase.table('knowledge_base').select('question, answer, media_url, tags').eq('status', 'active').execute()
    
    # Expand questions with pipe separator (multiple questions → one answer)
    expanded_cache = []
    for item in result.data:
        question = item["question"]
        tags = item.get("tags") or []
        
        # Check if question contains pipe separator
        if '|' in question:
            # Split by pipe and create separate entries for each question
            questions = [q.strip() for q in question.split('|')]
            for q in questions:
                expanded_cache.append({
                    'question': q,
                    'answer': item['answer'],
                    'media_url': item.get('media_url'),
                    'tags': tags
                })
        else:
            expanded_cache.append(item)
    
    _knowledge_base_cache = expanded_cache
    print(f"✅ Loaded {len(result.data)} knowledge base entries (expanded to {len(_knowledge_base_cache)} questions)")
    
    print("🤖 Creating TF-IDF vectorizer...")
    _vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2), max_features=1000)
    
    # Include tags in the searchable text for better matching
    searchable_texts = []
    for item in _knowledge_base_cache:
        # Combine question with tags for better search
        tags_text = ' '.join(item.get('tags', [])) if item.get('tags') else ''
        combined_text = f"{item['question']} {tags_text}"
        searchable_texts.append(combined_text)
    
    print("🔢 Fitting vectorizer...")
    _knowledge_vectors = _vectorizer.fit_transform(searchable_texts)
    _initialized = True
    print("✅ System initialization complete")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    print("🏥 Health check called")
    
    supabase_url = os.environ.get('SUPABASE_URL', '')
    supabase_key = os.environ.get('SUPABASE_KEY', '')
    
    return jsonify({
        'status': 'healthy' if (supabase_url and supabase_key) else 'degraded',
        'environment': {
            'supabase_url_configured': bool(supabase_url),
            'supabase_key_configured': bool(supabase_key),
            'confidence_threshold': CONFIDENCE_THRESHOLD
        },
        'message': 'AI Chatbot API is running on Render',
        'version': '2.0.0'
    })

def extract_keywords_from_text(text, max_keywords=20):
    """Extract keywords from text for better searchability"""
    # Simple keyword extraction - get important words
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    
    # Common stop words to exclude
    stop_words = {'that', 'this', 'with', 'from', 'have', 'will', 'your', 'about', 'when', 'what', 'where', 'which', 'their', 'there', 'these', 'those', 'would', 'could', 'should'}
    
    # Filter and count
    from collections import Counter
    word_counts = Counter([w for w in words if w not in stop_words])
    
    # Get top keywords
    keywords = [word for word, count in word_counts.most_common(max_keywords)]
    
    return keywords

def store_confluence_in_supabase(page_id, title, url, content, keywords):
    """Store Confluence content in Supabase"""
    try:
        print(f"💾 Storing Confluence content in Supabase...")
        supabase = get_supabase()
        
        # Check if page already exists
        existing = supabase.table('confluence_pages').select('*').eq('page_id', page_id).execute()
        
        data = {
            'page_id': page_id,
            'title': title,
            'url': url,
            'content': content,
            'keywords': keywords,
            'updated_at': 'now()'
        }
        
        if existing.data:
            # Update existing
            result = supabase.table('confluence_pages').update(data).eq('page_id', page_id).execute()
            print(f"✅ Updated existing Confluence page in Supabase")
        else:
            # Insert new
            data['created_at'] = 'now()'
            result = supabase.table('confluence_pages').insert(data).execute()
            print(f"✅ Stored new Confluence page in Supabase")
        
        return True
    except Exception as e:
        print(f"❌ Error storing in Supabase: {str(e)}")
        return False

def search_confluence_in_supabase(page_id, query):
    """Search for specific content within a stored Confluence page"""
    try:
        print(f"🔍 Searching Confluence content in Supabase...")
        supabase = get_supabase()
        
        # Get the page content
        result = supabase.table('confluence_pages').select('*').eq('page_id', page_id).execute()
        
        if not result.data:
            print(f"⚠️ Page not found in Supabase")
            return None
        
        page_data = result.data[0]
        content = page_data['content']
        
        # Extract query keywords
        query_keywords = [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', query)]
        
        # Split content into sections
        sections = content.split('\n\n')
        
        # Score each section based on keyword matches
        scored_sections = []
        for section in sections:
            if not section.strip():
                continue
            section_lower = section.lower()
            score = sum(1 for keyword in query_keywords if keyword in section_lower)
            if score > 0:
                scored_sections.append((score, section))
        
        # Sort by score and get top sections
        scored_sections.sort(reverse=True, key=lambda x: x[0])
        
        if scored_sections:
            top_sections = [section for score, section in scored_sections[:3]]
            return '\n\n'.join(top_sections)
        else:
            # Return first part of content if no match
            return content[:1500]
            
    except Exception as e:
        print(f"❌ Error searching Supabase: {str(e)}")
        return None

def extract_confluence_content(url):
    """Extract text content from Confluence page"""
    try:
        print(f"📄 Extracting Confluence content from: {url}")
        
        # Confluence PAT token from environment
        pat_token = os.environ.get('CONFLUENCE_PAT_TOKEN')
        if not pat_token:
            print("⚠️ CONFLUENCE_PAT_TOKEN not configured")
            return None, None, None
        
        base_url = 'https://confluence.elevancehealth.com'
        
        # Extract page ID from URL
        # URL format: https://confluence.elevancehealth.com/spaces/ICUX/pages/1638826393/Data+Mapper
        page_id_match = re.search(r'/pages/(\d+)', url)
        if not page_id_match:
            print("⚠️ Could not extract page ID from URL")
            return None, None, None
        
        page_id = page_id_match.group(1)
        
        # Use Confluence REST API
        api_url = f'{base_url}/rest/api/content/{page_id}?expand=body.storage'
        
        # Make request with Bearer token
        headers = {
            'Authorization': f'Bearer {pat_token}',
            'Accept': 'application/json',
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Parse JSON response from Confluence API
            data = response.json()
            
            # Get HTML content from body.storage
            html_content = data.get('body', {}).get('storage', {}).get('value', '')
            
            if not html_content:
                print("⚠️ No content found in Confluence page")
                return None
            
            # Parse HTML content and convert to formatted text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Convert HTML to formatted markdown-like text
            formatted_text = []
            
            # Process headers
            for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                level = int(header.name[1])
                formatted_text.append(f"\n{'#' * level} **{header.get_text().strip()}**\n")
                header.decompose()
            
            # Process lists
            for ul in soup.find_all('ul'):
                for li in ul.find_all('li', recursive=False):
                    formatted_text.append(f"• {li.get_text().strip()}")
                formatted_text.append("")
                ul.decompose()
            
            for ol in soup.find_all('ol'):
                for idx, li in enumerate(ol.find_all('li', recursive=False), 1):
                    formatted_text.append(f"{idx}. {li.get_text().strip()}")
                formatted_text.append("")
                ol.decompose()
            
            # Process tables
            for table in soup.find_all('table'):
                formatted_text.append("\n**Table:**")
                for row in table.find_all('tr'):
                    cells = [cell.get_text().strip() for cell in row.find_all(['td', 'th'])]
                    if cells:
                        formatted_text.append(" | ".join(cells))
                formatted_text.append("")
                table.decompose()
            
            # Process bold text
            for strong in soup.find_all(['strong', 'b']):
                strong.string = f"**{strong.get_text()}**"
            
            # Process italic text
            for em in soup.find_all(['em', 'i']):
                em.string = f"*{em.get_text()}*"
            
            # Process paragraphs
            for p in soup.find_all('p'):
                text = p.get_text().strip()
                if text:
                    formatted_text.append(text)
                    formatted_text.append("")
            
            # Get remaining text
            remaining_text = soup.get_text()
            lines = [line.strip() for line in remaining_text.splitlines() if line.strip()]
            formatted_text.extend(lines)
            
            # Join and clean up
            text = '\n'.join(formatted_text)
            
            # Remove excessive blank lines
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            # Limit to first 3000 characters for better content
            text = text[:3000]
            
            title = data.get('title', 'Unknown')
            print(f"✅ Extracted {len(text)} characters from Confluence page: {title}")
            
            return page_id, title, text
        else:
            print(f"❌ Failed to fetch Confluence page: {response.status_code}")
            return None, None, None
            
    except Exception as e:
        print(f"❌ Error extracting Confluence content: {str(e)}")
        return None, None, None

def extract_links_from_message(message):
    """Extract Confluence and Figma links from message"""
    print(f"🔍 Searching for links in message: {message[:100]}...")
    
    # Updated pattern for Elevance Confluence
    confluence_pattern = r'https?://confluence\.elevancehealth\.com/[^\s]+'
    figma_pattern = r'https?://(?:www\.)?figma\.com/[^\s]+'
    
    confluence_links = re.findall(confluence_pattern, message)
    figma_links = re.findall(figma_pattern, message)
    
    print(f"📎 Found {len(confluence_links)} Confluence links: {confluence_links}")
    print(f"📎 Found {len(figma_links)} Figma links: {figma_links}")
    
    return {
        'confluence': confluence_links,
        'figma': figma_links
    }

def extract_topic(question):
    """Extract main topic from question for structured responses"""
    question_lower = question.lower()
    
    # Topic mapping
    if 'food' in question_lower or 'hunger' in question_lower or 'cafeteria' in question_lower:
        return "Food & Meals"
    elif 'transport' in question_lower or 'cab' in question_lower or 'commute' in question_lower:
        return "Transport & Cab"
    elif 'laptop' in question_lower or 'asset' in question_lower or 'equipment' in question_lower:
        return "Laptop & Assets"
    elif 'kiran' in question_lower:
        return "Asset Team Contact"
    elif 'workday' in question_lower:
        return "Workday Portal"
    elif 'leave' in question_lower or 'vacation' in question_lower:
        return "Leave Application"
    elif 'timesheet' in question_lower or 'time entry' in question_lower:
        return "Timesheet"
    elif 'vpn' in question_lower:
        return "VPN Access"
    elif 'id card' in question_lower or 'badge' in question_lower:
        return "ID Card"
    elif 'training' in question_lower:
        return "Training"
    elif 'figma' in question_lower:
        return "Figma"
    elif 'buddy' in question_lower:
        return "Onboarding Buddy"
    elif 'manager' in question_lower:
        return "Manager"
    else:
        # Extract first meaningful part
        return question.split('?')[0].split('.')[0][:40]

def combine_answers(matches, query):
    """Combine multiple relevant answers into structured format"""
    
    if len(matches) == 1:
        return matches[0]['answer'], matches[0]['confidence']
    
    # Build structured response
    response = "Here's the information you requested:\n\n"
    
    seen_topics = set()
    included_count = 0
    
    for match in matches:
        topic = extract_topic(match['question'])
        
        # Avoid duplicate topics
        if topic in seen_topics:
            continue
        
        seen_topics.add(topic)
        included_count += 1
        
        response += f"**{included_count}. {topic.upper()}**\n"
        response += f"{match['answer']}\n\n"
        
        # Limit to top 3-4 topics
        if included_count >= 4:
            break
    
    # Calculate average confidence
    avg_confidence = sum(m['confidence'] for m in matches[:included_count]) / included_count
    
    return response.strip(), avg_confidence

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Chat endpoint with multi-topic support"""
    print("🚀 Chat endpoint called")
    print(f"📥 HTTP Method: {request.method}")
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        print("✅ OPTIONS request handled")
        return '', 200
    
    try:
        print("🔄 Initializing system...")
        initialize_system()
        print("✅ System initialized")
        
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')  # Get session ID from request
        print(f"📝 Message received: {message}")
        print(f"🔑 Session ID: {session_id}")
        
        if not message:
            print("❌ Empty message")
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Initialize session if not exists
        if session_id not in _conversation_sessions:
            _conversation_sessions[session_id] = {
                'confluence_content': None,
                'confluence_url': None,
                'history': []
            }
            print(f"🆕 Created new session: {session_id}")
        
        session = _conversation_sessions[session_id]
        
        # Extract links from message
        print("🔗 Extracting links from message...")
        links = extract_links_from_message(message)
        confluence_content = None
        
        print(f"🔗 Links extracted: {links}")
        
        # Extract Confluence content if link is present
        if links['confluence']:
            print(f"✅ Confluence link detected!")
            confluence_url = links['confluence'][0]  # Use first link
            print(f"📄 Extracting content from: {confluence_url}")
            
            page_id, title, confluence_content = extract_confluence_content(confluence_url)
            
            if confluence_content and page_id:
                print(f"✅ Confluence content extracted successfully! Length: {len(confluence_content)}")
                print(f"📄 Page: {title} (ID: {page_id})")
                
                # Extract keywords from content
                keywords = extract_keywords_from_text(confluence_content)
                print(f"🏷️ Extracted {len(keywords)} keywords: {keywords[:10]}...")
                
                # Store in Supabase
                stored = store_confluence_in_supabase(page_id, title, confluence_url, confluence_content, keywords)
                
                if stored:
                    print(f"✅ Content stored in Supabase")
                
                # Store in session
                session['confluence_page_id'] = page_id
                session['confluence_url'] = confluence_url
                session['confluence_title'] = title
                session['history'].append({'user': message, 'bot': confluence_content})
                
                # Return the Confluence content directly as the answer
                return jsonify({
                    'reply': f"**{title}**\n\n{confluence_content}\n\n_Note: This content has been extracted and stored. You can ask follow-up questions about this content._",
                    'confidence': 1.0,
                    'media_url': None
                })
            else:
                print(f"❌ Failed to extract Confluence content")
        
        # Check if we have Confluence context from previous messages
        if session.get('confluence_page_id') and not links['confluence']:
            print(f"💬 Using stored Confluence context for follow-up question")
            
            # Search Supabase for relevant content
            page_id = session['confluence_page_id']
            title = session.get('confluence_title', 'Confluence Page')
            
            answer = search_confluence_in_supabase(page_id, message)
            
            if answer:
                print(f"✅ Found relevant content from Supabase")
                return jsonify({
                    'reply': f"**From: {title}**\n\n{answer}\n\n_Note: This answer is from the previously shared Confluence page._",
                    'confidence': 0.9,
                    'media_url': None
                })
            else:
                print(f"⚠️ Could not find content in Supabase, falling back to knowledge base")
        
        print("🔍 Vectorizing message...")
        user_vector = _vectorizer.transform([message])
        print("🔍 Computing similarities...")
        similarities = sklearn_cosine_similarity(user_vector, _knowledge_vectors)[0]
        
        # Get top matches for potential multi-topic response
        top_indices = np.argsort(similarities)[-10:][::-1]  # Get top 10 for better multi-topic coverage
        
        relevant_matches = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= 0.20:  # Lower threshold for multi-topic detection
                item = _knowledge_base_cache[idx].copy()
                item['confidence'] = score
                relevant_matches.append(item)
        
        if not relevant_matches:
            print(f"⚠️ No matches above threshold")
            return jsonify({
                'reply': "I'm not confident enough to answer that question. Could you please rephrase or ask something else from my knowledge base?",
                'confidence': 0.0,
                'media_url': None
            })
        
        best_score = relevant_matches[0]['confidence']
        print(f"📊 Best match score: {best_score}, Total relevant: {len(relevant_matches)}")
        
        # Detect multi-topic query
        message_lower = message.lower()
        multi_topic_indicators = [' and ', ',', ' also ', ' about ', 'tell me about', 'know about', 'info about', 'information about']
        has_multiple_topics = any(indicator in message_lower for indicator in multi_topic_indicators)
        
        # Count distinct topics mentioned
        topic_keywords = ['food', 'transport', 'laptop', 'workday', 'leave', 'timesheet', 'vpn', 'training', 'figma', 'buddy', 'manager', 'kiran', 'asset', 'cab', 'hunger']
        topics_mentioned = sum(1 for keyword in topic_keywords if keyword in message_lower)
        
        # Use multi-topic response if:
        # 1. Query has multi-topic indicators OR multiple topics mentioned
        # 2. Multiple relevant matches found
        # 3. Best match confidence is not overwhelmingly high
        if (has_multiple_topics or topics_mentioned >= 2) and len(relevant_matches) > 1 and best_score < 0.75:
            print(f"🔀 Multi-topic query detected, combining {len(relevant_matches)} answers")
            combined_answer, avg_confidence = combine_answers(relevant_matches[:4], message)
            
            response_data = {
                'reply': combined_answer,
                'confidence': avg_confidence,
                'media_url': None
            }
            print(f"📤 Sending multi-topic response: avg_confidence={avg_confidence}")
        else:
            # Single best answer
            if best_score < CONFIDENCE_THRESHOLD:
                print(f"⚠️ Low confidence ({best_score} < {CONFIDENCE_THRESHOLD})")
                return jsonify({
                    'reply': "I'm not confident enough to answer that question. Could you please rephrase or ask something else from my knowledge base?",
                    'confidence': best_score,
                    'media_url': None
                })
            
            matched_item = relevant_matches[0]
            print(f"✅ Single answer: {matched_item['answer'][:50]}...")
            
            response_data = {
                'reply': matched_item['answer'],
                'confidence': best_score,
                'media_url': matched_item.get('media_url')
            }
            print(f"📤 Sending single response: confidence={best_score}")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'AI Chatbot API',
        'endpoints': {
            'health': '/health (GET)',
            'chat': '/chat (POST)'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
