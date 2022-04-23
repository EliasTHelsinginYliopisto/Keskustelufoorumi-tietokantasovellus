CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    poster_id INTEGER REFERENCES users,
    title TEXT,
    body TEXT
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    commenter_id INTEGER REFERENCES users,
    post_id INTEGER REFERENCES posts,
    comment TEXT
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    comment_id INTEGER REFERENCES comments,
    rater_id INTEGER REFERENCES users,
    post_id INTEGER REFERENCES posts
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users,
    reciever_id INTEGER REFERENCES users
);