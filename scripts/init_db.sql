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
