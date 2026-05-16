CREATE TABLE news_sources (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    fetch_method TEXT NOT NULL
);