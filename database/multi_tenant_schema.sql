-- Multi-Tenant Database Schema for Cypher Widget Platform
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Products Table (Represents different applications/websites using the widget)
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    domain VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    active BOOLEAN DEFAULT true
);

-- Widgets Table (Individual widget instances per product)
CREATE TABLE IF NOT EXISTS widgets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    widget_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    active BOOLEAN DEFAULT true
);

-- API Keys Table (Authentication for widgets)
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    widget_id UUID REFERENCES widgets(id) ON DELETE CASCADE,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    permissions JSONB DEFAULT '{}',
    rate_limit INTEGER DEFAULT 1000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    last_used_at TIMESTAMP WITH TIME ZONE,
    active BOOLEAN DEFAULT true
);

-- Knowledge Base Table (Q&A data per widget)
CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    widget_id UUID REFERENCES widgets(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(100),
    tags TEXT[],
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Analytics Table (Usage tracking)
CREATE TABLE IF NOT EXISTS analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    widget_id UUID REFERENCES widgets(id) ON DELETE CASCADE,
    session_id VARCHAR(255),
    message_count INTEGER DEFAULT 0,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_widgets_product_id ON widgets(product_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_widget_id ON api_keys(widget_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_key ON api_keys(api_key);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_widget_id ON knowledge_base(widget_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_base_status ON knowledge_base(status);
CREATE INDEX IF NOT EXISTS idx_analytics_widget_id ON analytics(widget_id);
CREATE INDEX IF NOT EXISTS idx_analytics_created_at ON analytics(created_at);

-- Insert demo data
INSERT INTO products (name, description, domain, active) VALUES
('InSync', 'Carelon employee attendance management portal', 'insync.carelon.com', true)
ON CONFLICT DO NOTHING;

-- Get the product ID for demo
DO $$
DECLARE
    product_id UUID;
    widget_uuid UUID;
BEGIN
    SELECT id INTO product_id FROM products WHERE name = 'InSync' LIMIT 1;

    IF product_id IS NOT NULL THEN
        -- Insert demo widget
        INSERT INTO widgets (product_id, widget_id, name, config, active) VALUES
        (product_id, 'insync-widget', 'InSync Chatbot',
         '{"theme": {"primaryColor": "#5009B5", "accentColor": "#00D9FF"}}', true)
        ON CONFLICT (widget_id) DO NOTHING;

        -- Insert demo API key
        SELECT id INTO widget_uuid FROM widgets WHERE widget_id = 'insync-widget' LIMIT 1;
        INSERT INTO api_keys (widget_id, api_key, name, rate_limit, active)
        VALUES (widget_uuid, 'demo-key', 'Demo API Key', 1000, true)
        ON CONFLICT (api_key) DO NOTHING;
    END IF;
END $$;

-- Insert demo knowledge base
DO $$
DECLARE
    widget_uuid UUID;
BEGIN
    SELECT id INTO widget_uuid FROM widgets WHERE widget_id = 'insync-widget' LIMIT 1;

    IF widget_uuid IS NOT NULL THEN
        INSERT INTO knowledge_base (widget_id, question, answer, category, status) VALUES
        (widget_uuid, 'What is HyWo?', 'HyWo stands for Hybrid Work. It is Carelon''s attendance tracking system where employees log their daily work location.', 'insync', 'active'),
        (widget_uuid, 'How do I track my HyWo attendance?', 'To track HyWo attendance: 1) Log in to InSync portal, 2) Navigate to HyWo section, 3) Select your work location, 4) Submit your attendance.', 'insync', 'active'),
        (widget_uuid, 'What is a HyWo Exception?', 'A HyWo Exception is a request to correct or update your attendance for dates where you couldn''t mark HyWo on time.', 'insync', 'active'),
        (widget_uuid, 'How do I submit a HyWo Exception?', 'Go to InSync portal, navigate to HyWo Exception section, select the date, provide reason, and submit for approval.', 'insync', 'active'),
        (widget_uuid, 'What is a relocation request?', 'A relocation request is a formal request to change your primary work location or office.', 'insync', 'active'),
        (widget_uuid, 'What is a SEZ card?', 'SEZ card is your official identification for accessing SEZ-designated office premises.', 'insync', 'active')
        ON CONFLICT DO NOTHING;
    END IF;
END $$;
