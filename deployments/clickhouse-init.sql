-- Create database
CREATE DATABASE IF NOT EXISTS xsw;

-- Create events table
CREATE TABLE IF NOT EXISTS xsw.events (
    event_id UUID,
    user_id String,
    event_name String,
    timestamp DateTime64(3, 'UTC'),
    properties String,  -- stores JSON data like browser, os, ip etc
    site_url String
) ENGINE = MergeTree()
ORDER BY (timestamp, event_id, user_id);