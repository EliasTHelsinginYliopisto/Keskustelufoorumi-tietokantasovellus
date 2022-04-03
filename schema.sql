CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    poster_id INTEGER REFERENCES users,
    poster_name TEXT, --Temporary column, remove after implementing users
    title TEXT,
    body TEXT
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    commenter_id INTEGER REFERENCES users,
    post_id INTEGER REFERENCES posts,
    comment TEXT
);