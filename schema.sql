CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    poster_id INTEGER REFERENCES users,
    title TEXT,
    body TEXT,
    visible INTEGER
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    commenter_id INTEGER REFERENCES users,
    post_id INTEGER REFERENCES posts,
    comment TEXT,
    visible INTEGER
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
    group_id INTEGER REFERENCES groups,
    content TEXT
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    member_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups,
    post_id INTEGER REFERENCES posts,
    role INTEGER  -- 0 = member, 1 = admin
);