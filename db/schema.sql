CREATE TABLE IF NOT EXISTS states (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    population INT,
    category VARCHAR(20)
);