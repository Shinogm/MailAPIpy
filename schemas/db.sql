-- Active: 1696921476499@@127.0.0.1@3306@mail_db
DROP DATABASE IF EXISTS mail_db;

CREATE DATABASE mail_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE mail_db;

CREATE TABLE permissions (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY name (name)
);

CREATE TABLE contacts (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
);

CREATE TABLE users (
    id BINARY(16) NOT NULL DEFAULT (UUID_TO_BIN(UUID())),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
);

CREATE TABLE user_perms (
    id INT NOT NULL AUTO_INCREMENT,
    user_id BINARY(16) NOT NULL,
    perm_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY user_perm (user_id, perm_id),
    CONSTRAINT fk_user_perm_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_perm_perm FOREIGN KEY (perm_id) REFERENCES permissions (id) ON DELETE CASCADE
);