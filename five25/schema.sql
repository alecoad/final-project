CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL,
  password VARCHAR NOT NULL
);

CREATE TABLE lists (
  id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER REFERENCES users
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL,
  distraction BOOLEAN NOT NULL DEFAULT TRUE,
  completed BOOLEAN NOT NULL DEFAULT FALSE,
  list_id INTEGER REFERENCES lists
);
