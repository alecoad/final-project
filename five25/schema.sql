CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

CREATE TABLE goalss (
    id SERIAL PRIMARY KEY,
    pursuit VARCHAR NOT NULL,
    distraction BOOLEAN NOT NULL DEFAULT TRUE,
    user_id INTEGER REFERENCES users
);
