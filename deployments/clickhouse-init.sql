CREATE TABLE IF NOT EXISTS events(
    event_id UUID,
    user_id String,
    event_name String,
    timestamp DateTime64(2, 'UTC'),
    properties String, -- stores JSON DATA like browser, os ip etc
    site_url String,
)ENGINE = MergeTree()
ORDER BY (timestamp, event_id,  user_id)