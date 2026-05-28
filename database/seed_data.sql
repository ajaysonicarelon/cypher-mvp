-- ============================================================================
-- Seed Data for AI Chatbot Knowledge Base
-- ============================================================================
-- This file populates the database with initial Q&A entries
-- Run this AFTER schema.sql
-- ============================================================================

-- Clear existing data (optional - uncomment if you want fresh start)
-- TRUNCATE TABLE knowledge_base RESTART IDENTITY CASCADE;

-- ============================================================================
-- Insert initial knowledge base entries
-- ============================================================================

INSERT INTO knowledge_base (
    question, 
    answer, 
    media_url, 
    source_type, 
    source_id,
    category, 
    tags, 
    metadata,
    last_synced
) VALUES

-- AI/ML Basics
(
    'What is machine learning?',
    'Machine learning is a branch of artificial intelligence that enables computers to learn from data and improve their performance without being explicitly programmed. It uses algorithms to identify patterns and make decisions based on input data.',
    NULL,
    'manual',
    'seed-001',
    'ai-basics',
    ARRAY['ai', 'machine-learning', 'basics'],
    '{"difficulty": "beginner", "views": 0}'::jsonb,
    NOW()
),

(
    'How do neural networks work?',
    'Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers that process information through weighted connections, learning to recognize patterns through training.',
    NULL,
    'manual',
    'seed-002',
    'ai-basics',
    ARRAY['neural-networks', 'deep-learning', 'ai'],
    '{"difficulty": "intermediate", "views": 0}'::jsonb,
    NOW()
),

(
    'What is deep learning?',
    'Deep learning is a subset of machine learning that uses neural networks with multiple layers (deep neural networks) to progressively extract higher-level features from raw input. It excels at tasks like image recognition, natural language processing, and speech recognition.',
    NULL,
    'manual',
    'seed-003',
    'ai-basics',
    ARRAY['deep-learning', 'neural-networks', 'ai'],
    '{"difficulty": "intermediate", "views": 0}'::jsonb,
    NOW()
),

(
    'Explain natural language processing',
    'Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language. It enables machines to read, understand, and derive meaning from human languages, powering applications like chatbots, translation services, and sentiment analysis.',
    NULL,
    'manual',
    'seed-004',
    'nlp',
    ARRAY['nlp', 'ai', 'language'],
    '{"difficulty": "intermediate", "views": 0}'::jsonb,
    NOW()
),

-- Visual content with images
(
    'Show me a diagram of AI architecture',
    'Here''s a visual representation of a typical AI system architecture showing the data flow from input through processing layers to output.',
    'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80',
    'manual',
    'seed-005',
    'architecture',
    ARRAY['ai', 'architecture', 'diagram', 'visual'],
    '{"difficulty": "intermediate", "has_media": true, "media_type": "image"}'::jsonb,
    NOW()
),

(
    'What does a data science workflow look like?',
    'A data science workflow typically includes data collection, cleaning, exploration, modeling, and deployment. Here''s a visual guide to the process.',
    'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80',
    'manual',
    'seed-006',
    'data-science',
    ARRAY['data-science', 'workflow', 'process', 'visual'],
    '{"difficulty": "beginner", "has_media": true, "media_type": "image"}'::jsonb,
    NOW()
),

-- Additional helpful entries
(
    'What is the difference between AI and ML?',
    'AI (Artificial Intelligence) is the broader concept of machines being able to carry out tasks in a smart way. ML (Machine Learning) is a subset of AI that focuses on the ability of machines to receive data and learn for themselves without being explicitly programmed.',
    NULL,
    'manual',
    'seed-007',
    'ai-basics',
    ARRAY['ai', 'machine-learning', 'comparison'],
    '{"difficulty": "beginner", "views": 0}'::jsonb,
    NOW()
),

(
    'What are the types of machine learning?',
    'There are three main types of machine learning: 1) Supervised Learning - learning from labeled data, 2) Unsupervised Learning - finding patterns in unlabeled data, and 3) Reinforcement Learning - learning through trial and error with rewards and penalties.',
    NULL,
    'manual',
    'seed-008',
    'ai-basics',
    ARRAY['machine-learning', 'supervised', 'unsupervised', 'reinforcement'],
    '{"difficulty": "beginner", "views": 0}'::jsonb,
    NOW()
);

-- ============================================================================
-- Verify insertion
-- ============================================================================

DO $$
DECLARE
    entry_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO entry_count FROM knowledge_base;
    RAISE NOTICE '✅ Seed data inserted successfully!';
    RAISE NOTICE '📊 Total entries in database: %', entry_count;
    RAISE NOTICE '';
    RAISE NOTICE '📝 Entries by category:';
END $$;

-- Show summary
SELECT 
    category,
    COUNT(*) as count,
    STRING_AGG(DISTINCT source_type, ', ') as sources
FROM knowledge_base
GROUP BY category
ORDER BY count DESC;

-- Show entries with media
SELECT 
    question,
    CASE WHEN media_url IS NOT NULL THEN '✅ Has media' ELSE '❌ No media' END as media_status
FROM knowledge_base
ORDER BY id;

-- ============================================================================
-- Success message
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '🎉 Database is ready!';
    RAISE NOTICE '';
    RAISE NOTICE '📝 Next steps:';
    RAISE NOTICE '   1. Test connection with: python database/test_connection.py';
    RAISE NOTICE '   2. Migrate existing data with: python database/migrate_existing.py';
    RAISE NOTICE '   3. Start syncing from MCP sources';
END $$;
