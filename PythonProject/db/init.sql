CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
INSERT INTO items (name) VALUES ('item1'), ('item2');
