DROP DATABASE IF EXISTS scoin;
CREATE DATABASE scoin;
\c scoin

CREATE TABLE transactions(
  id SERIAL PRIMARY KEY,
  hash VARCHAR(100) NOT NULL UNIQUE,
  sender VARCHAR(100) NOT NULL,
  receiver VARCHAR(100) NOT NULL,
  description TEXT,
  timestamp INT
);
