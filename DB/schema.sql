-- TweeeeeDBT Database Schema
-- PostgreSQL schema for streaming analytics pipeline

-- Create verified_tweets table
CREATE TABLE IF NOT EXISTS verified_tweets (
    id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(255),
    user_name VARCHAR(255),
    user_verified BOOLEAN,
    tweet TEXT,
    hashtags TEXT,
    date TIMESTAMP,
    user_location VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create geo_location table for geographic analytics
CREATE TABLE IF NOT EXISTS geo_location (
    id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(255),
    user_name VARCHAR(255), 
    tweet TEXT,
    user_location VARCHAR(255),
    city VARCHAR(50),
    date TIMESTAMP,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create team_mentions table for team analysis
CREATE TABLE IF NOT EXISTS team_mentions (
    id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(255),
    user_name VARCHAR(255),
    tweet TEXT,
    hashtags TEXT,
    team VARCHAR(50),
    date TIMESTAMP,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create batch_metrics table for performance monitoring
CREATE TABLE IF NOT EXISTS batch_metrics (
    id SERIAL PRIMARY KEY,
    processing_time FLOAT,
    records_processed INTEGER,
    memory_usage FLOAT,
    cpu_usage FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create windowed_user_count table for windowed analytics
CREATE TABLE IF NOT EXISTS windowed_user_count (
    id SERIAL PRIMARY KEY,
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    user_count INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_verified_tweets_date ON verified_tweets(date);
CREATE INDEX IF NOT EXISTS idx_verified_tweets_verified ON verified_tweets(user_verified);
CREATE INDEX IF NOT EXISTS idx_geo_location_city ON geo_location(city);
CREATE INDEX IF NOT EXISTS idx_geo_location_date ON geo_location(date);
CREATE INDEX IF NOT EXISTS idx_team_mentions_team ON team_mentions(team);
CREATE INDEX IF NOT EXISTS idx_team_mentions_date ON team_mentions(date);
CREATE INDEX IF NOT EXISTS idx_batch_metrics_timestamp ON batch_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_windowed_user_count_timestamp ON windowed_user_count(timestamp);

-- Grant permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_username;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_username;