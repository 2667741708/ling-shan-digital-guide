CREATE TABLE IF NOT EXISTS scenic_spot (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    alias VARCHAR(200),
    description TEXT,
    history_story TEXT,
    guide_text TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    map_x DOUBLE PRECISION,
    map_y DOUBLE PRECISION,
    tags VARCHAR(500),
    recommended_duration INT,
    popularity_score FLOAT DEFAULT 0.5,
    cultural_score FLOAT DEFAULT 0.5,
    photo_score FLOAT DEFAULT 0.5,
    family_score FLOAT DEFAULT 0.5,
    elderly_friendly_score FLOAT DEFAULT 0.5,
    open_time VARCHAR(100),
    close_time VARCHAR(100),
    image_url TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS faq (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(50),
    keywords VARCHAR(500),
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS admin_user (
    id VARCHAR(32) PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(40) DEFAULT 'admin',
    enabled BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS knowledge_document (
    id VARCHAR(32) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    current_version INT DEFAULT 1,
    current_version_id VARCHAR(32),
    storage_path TEXT NOT NULL,
    created_by VARCHAR(80) DEFAULT 'system',
    updated_by VARCHAR(80) DEFAULT 'system',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_knowledge_document_status ON knowledge_document(status);

CREATE TABLE IF NOT EXISTS knowledge_document_version (
    id VARCHAR(32) PRIMARY KEY,
    document_id VARCHAR(32) NOT NULL REFERENCES knowledge_document(id),
    version INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    storage_path TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    change_note TEXT DEFAULT '',
    created_by VARCHAR(80) DEFAULT 'system',
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT uq_knowledge_document_version UNIQUE(document_id, version)
);

CREATE INDEX IF NOT EXISTS ix_knowledge_document_version_document_id ON knowledge_document_version(document_id);

CREATE TABLE IF NOT EXISTS knowledge_operation_log (
    id VARCHAR(32) PRIMARY KEY,
    document_id VARCHAR(32) REFERENCES knowledge_document(id),
    version_id VARCHAR(32),
    action VARCHAR(40) NOT NULL,
    actor VARCHAR(80) DEFAULT 'system',
    detail TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_knowledge_operation_log_document_id ON knowledge_operation_log(document_id);

CREATE TABLE IF NOT EXISTS avatar_config (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(100) DEFAULT '灵灵',
    avatar_style VARCHAR(100) DEFAULT 'ancient',
    clothes VARCHAR(100) DEFAULT 'traditional_blue',
    voice_name VARCHAR(100) DEFAULT 'female_warm',
    voice_speed DOUBLE PRECISION DEFAULT 1.0,
    opening_text TEXT DEFAULT '您好，我是您的 AI 数字人导游灵灵。',
    expressions_json TEXT DEFAULT '["idle","listening","thinking","speaking","happy","concerned"]',
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_avatar_config_enabled ON avatar_config(enabled);
