CREATE TABLE news_sources (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    portal_url TEXT NOT NULL UNIQUE,
    method_url TEXT NOT NULL UNIQUE,
    fetch_method TEXT NOT NULL
);