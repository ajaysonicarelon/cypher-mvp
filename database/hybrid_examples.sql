-- ============================================================================
-- HYBRID SCHEMA EXAMPLES
-- ============================================================================
-- This file demonstrates the flexibility of the hybrid schema
-- showing various document types and content structures
-- ============================================================================

-- Example 1: Simple Q&A (Default - Chatbot style)
INSERT INTO knowledge_base (
    question, answer, content_type, category, tags
) VALUES (
    'What is machine learning?',
    'Machine learning is a branch of AI that enables computers to learn from data.',
    'qa',
    'ai-basics',
    ARRAY['ai', 'ml', 'basics']
);

-- Example 2: Q&A with Image
INSERT INTO knowledge_base (
    question, answer, media_url, media_type, content_type, category, tags
) VALUES (
    'Show me AI architecture',
    'Here is a visual representation of AI system architecture.',
    'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800',
    'image',
    'qa',
    'architecture',
    ARRAY['ai', 'architecture', 'visual']
);

-- Example 3: Q&A with Multiple Media (Images + PDF + Video)
INSERT INTO knowledge_base (
    question, 
    answer, 
    media_url,
    media_urls,
    content_type, 
    category, 
    tags
) VALUES (
    'How to set up development environment?',
    'Follow these steps to set up your development environment. See the video tutorial and reference documentation.',
    'https://youtube.com/watch?v=setup-guide',  -- Primary media
    '{
        "images": [
            "https://example.com/screenshot1.png",
            "https://example.com/screenshot2.png"
        ],
        "videos": [
            "https://youtube.com/watch?v=setup-guide",
            "https://youtube.com/watch?v=troubleshooting"
        ],
        "pdfs": [
            "https://docs.company.com/setup-guide.pdf"
        ]
    }'::jsonb,
    'tutorial',
    'development',
    ARRAY['setup', 'dev', 'tutorial']
);

-- Example 4: Full Document (Confluence Page)
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content,
    source_type,
    source_id,
    source_url,
    category,
    subcategory,
    tags,
    department,
    last_synced
) VALUES (
    'What is our vacation policy?',
    'Employees receive 20 days of paid vacation per year. See full policy document for details.',
    'policy',
    '{
        "title": "Vacation Policy 2026",
        "sections": [
            {
                "heading": "Eligibility",
                "content": "All full-time employees are eligible after 90 days"
            },
            {
                "heading": "Accrual",
                "content": "Vacation days accrue at 1.67 days per month"
            },
            {
                "heading": "Carryover",
                "content": "Up to 5 days can be carried over to next year"
            }
        ],
        "effective_date": "2026-01-01",
        "last_reviewed": "2026-01-15"
    }'::jsonb,
    'confluence',
    'page-12345',
    'https://company.atlassian.net/wiki/spaces/HR/pages/12345',
    'hr-policies',
    'time-off',
    ARRAY['vacation', 'pto', 'benefits', 'hr'],
    'HR',
    NOW()
);

-- Example 5: Code Snippet (from GitHub)
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content,
    source_type,
    source_id,
    source_url,
    category,
    tags,
    priority
) VALUES (
    'How to connect to the database?',
    'Use this code snippet to establish a database connection.',
    'code',
    '{
        "language": "python",
        "code": "from supabase import create_client\\n\\nsupabase = create_client(url, key)\\nresult = supabase.table(\"users\").select(\"*\").execute()",
        "description": "Basic Supabase connection example",
        "dependencies": ["supabase"],
        "version": "2.3.0"
    }'::jsonb,
    'github',
    'repo/examples/db-connection.py',
    'https://github.com/company/repo/blob/main/examples/db-connection.py',
    'code-examples',
    ARRAY['python', 'database', 'supabase', 'code'],
    5  -- High priority
);

-- Example 6: Troubleshooting Guide (Step-by-step)
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content,
    category,
    tags,
    priority
) VALUES (
    'How to fix "Connection Timeout" error?',
    'Follow these troubleshooting steps to resolve connection timeout errors.',
    'troubleshooting',
    '{
        "problem": "Connection Timeout Error",
        "symptoms": [
            "Request takes longer than 30 seconds",
            "Error message: Connection timeout",
            "Application becomes unresponsive"
        ],
        "steps": [
            {
                "step": 1,
                "action": "Check network connectivity",
                "command": "ping api.example.com"
            },
            {
                "step": 2,
                "action": "Verify firewall settings",
                "details": "Ensure port 443 is open"
            },
            {
                "step": 3,
                "action": "Increase timeout value",
                "code": "timeout = 60  # seconds"
            },
            {
                "step": 4,
                "action": "Contact IT if issue persists",
                "contact": "it-support@company.com"
            }
        ],
        "related_issues": ["DNS-001", "NETWORK-042"]
    }'::jsonb,
    'troubleshooting',
    ARRAY['error', 'timeout', 'network', 'troubleshooting'],
    8  -- Very high priority
);

-- Example 7: Tutorial with Steps (from Figma)
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content,
    media_url,
    media_type,
    source_type,
    source_id,
    source_url,
    category,
    tags,
    last_synced
) VALUES (
    'How to create a new component in Figma?',
    'Follow this step-by-step tutorial to create reusable components in Figma.',
    'tutorial',
    '{
        "title": "Creating Figma Components",
        "difficulty": "beginner",
        "duration": "10 minutes",
        "steps": [
            {
                "number": 1,
                "title": "Select your design",
                "description": "Select the layers you want to turn into a component",
                "shortcut": "Cmd/Ctrl + Click"
            },
            {
                "number": 2,
                "title": "Create component",
                "description": "Right-click and select Create Component",
                "shortcut": "Cmd/Ctrl + Alt + K"
            },
            {
                "number": 3,
                "title": "Name your component",
                "description": "Give it a descriptive name using / for organization",
                "example": "Button/Primary/Large"
            },
            {
                "number": 4,
                "title": "Add variants",
                "description": "Create variants for different states",
                "tip": "Use consistent naming for properties"
            }
        ],
        "tips": [
            "Use auto-layout for responsive components",
            "Document your components with descriptions"
        ]
    }'::jsonb,
    'https://figma.com/file/abc123/tutorial-screenshot',
    'image',
    'figma',
    'file-abc123-node-456',
    'https://figma.com/file/abc123/Design-System',
    'design',
    ARRAY['figma', 'components', 'tutorial', 'design-system'],
    NOW()
);

-- Example 8: Reference Documentation (API Docs)
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content,
    category,
    subcategory,
    tags,
    is_public,
    required_role
) VALUES (
    'What are the available API endpoints?',
    'Complete reference of all API endpoints with parameters and examples.',
    'reference',
    '{
        "api_version": "v2",
        "base_url": "https://api.company.com/v2",
        "authentication": "Bearer token required",
        "endpoints": [
            {
                "method": "GET",
                "path": "/users",
                "description": "List all users",
                "parameters": {
                    "limit": "integer (optional, default: 50)",
                    "offset": "integer (optional, default: 0)"
                },
                "response": {
                    "200": "Success - returns user array",
                    "401": "Unauthorized",
                    "500": "Server error"
                },
                "example": "curl -H \"Authorization: Bearer TOKEN\" https://api.company.com/v2/users"
            },
            {
                "method": "POST",
                "path": "/users",
                "description": "Create new user",
                "body": {
                    "email": "string (required)",
                    "name": "string (required)",
                    "role": "string (optional)"
                }
            }
        ],
        "rate_limits": "1000 requests per hour",
        "support": "api-support@company.com"
    }'::jsonb,
    'api-docs',
    'endpoints',
    ARRAY['api', 'reference', 'documentation', 'rest'],
    false,  -- Not public
    'developer'  -- Requires developer role
);

-- Example 9: FAQ Entry (Multiple related Q&As)
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    content,
    category,
    tags
) VALUES (
    'Common questions about password reset',
    'Here are the most frequently asked questions about password reset.',
    'faq',
    '{
        "faqs": [
            {
                "q": "How do I reset my password?",
                "a": "Click Forgot Password on the login page and follow the email instructions."
            },
            {
                "q": "How long is the reset link valid?",
                "a": "Password reset links expire after 24 hours."
            },
            {
                "q": "I did not receive the reset email",
                "a": "Check your spam folder. If still missing, contact IT support."
            },
            {
                "q": "Can I reuse an old password?",
                "a": "No, you cannot reuse any of your last 5 passwords."
            }
        ]
    }'::jsonb,
    'account-management',
    ARRAY['password', 'reset', 'faq', 'security']
);

-- Example 10: Hierarchical Content (Parent-Child relationship)
-- Parent page
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    source_type,
    source_id,
    source_url,
    category,
    tags,
    priority,
    last_synced
) VALUES (
    'Employee Onboarding Guide',
    'Complete guide for new employee onboarding process.',
    'document',
    'confluence',
    'page-parent-001',
    'https://company.atlassian.net/wiki/spaces/HR/pages/parent-001',
    'hr',
    ARRAY['onboarding', 'hr', 'new-hire'],
    10,  -- Highest priority
    NOW()
);

-- Child page 1
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    source_type,
    source_id,
    source_parent_id,  -- Links to parent
    source_url,
    category,
    tags,
    last_synced
) VALUES (
    'Day 1: Getting Started',
    'What to expect on your first day at the company.',
    'document',
    'confluence',
    'page-child-001',
    'page-parent-001',  -- Parent ID
    'https://company.atlassian.net/wiki/spaces/HR/pages/child-001',
    'hr',
    ARRAY['onboarding', 'day-1', 'first-day'],
    NOW()
);

-- Child page 2
INSERT INTO knowledge_base (
    question,
    answer,
    content_type,
    source_type,
    source_id,
    source_parent_id,  -- Links to parent
    source_url,
    category,
    tags,
    last_synced
) VALUES (
    'Week 1: Training Schedule',
    'Your training schedule for the first week.',
    'document',
    'confluence',
    'page-child-002',
    'page-parent-001',  -- Parent ID
    'https://company.atlassian.net/wiki/spaces/HR/pages/child-002',
    'hr',
    ARRAY['onboarding', 'training', 'week-1'],
    NOW()
);

-- ============================================================================
-- Query Examples for Hybrid Data
-- ============================================================================

-- Find all tutorials
-- SELECT * FROM knowledge_base WHERE content_type = 'tutorial';

-- Find all content from Confluence
-- SELECT * FROM knowledge_base WHERE source_type = 'confluence';

-- Find content with multiple media
-- SELECT * FROM knowledge_base WHERE media_urls IS NOT NULL;

-- Find high priority items
-- SELECT * FROM knowledge_base WHERE priority >= 8 ORDER BY priority DESC;

-- Find child pages of a parent
-- SELECT * FROM knowledge_base WHERE source_parent_id = 'page-parent-001';

-- Find code examples in Python
-- SELECT * FROM knowledge_base 
-- WHERE content_type = 'code' 
-- AND content->>'language' = 'python';

-- Find HR policies
-- SELECT * FROM knowledge_base 
-- WHERE department = 'HR' 
-- AND content_type = 'policy';

-- Find content expiring soon
-- SELECT * FROM knowledge_base 
-- WHERE expiry_date < NOW() + INTERVAL '30 days'
-- AND status = 'active';
