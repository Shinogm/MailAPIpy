-- Active: 1695837029838@@127.0.0.1@3306@mail_db
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
    name VARCHAR(255),
    birthday DATE,
    email VARCHAR(255),
    phone VARCHAR(255),
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
);

CREATE TABLE plans(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY name (name)
);

INSERT INTO plans (name, price) VALUES
('Basic', 4.99),
('Pro', 9.99),
('Ultimate', 14.99);

CREATE TABLE users (
    id BINARY(16) NOT NULL DEFAULT (UUID_TO_BIN(UUID())),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    plan_id INT NOT NULL,
    paid_plan_stamp TIMESTAMP NULL DEFAULT NOW(),
    is_paid TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    UNIQUE KEY email (email),
    CONSTRAINT fk_user_plan FOREIGN KEY (plan_id) REFERENCES plans (id)
);

CREATE TABLE user_email_smtp(
    id INT NOT NULL AUTO_INCREMENT,
    user_id BINARY(16) NOT NULL,
    smtp_server VARCHAR(255) NOT NULL,
    port INT NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY user_email_smtp (smtp_server(191), port, user_name(191), user_password(191)),
    CONSTRAINT fk_user_email_smtp_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
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

CREATE TABLE folders(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE user_folders (
    id INT NOT NULL AUTO_INCREMENT,
    user_id BINARY(16) NOT NULL,
    folder_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY user_folder (user_id, folder_id),
    CONSTRAINT fk_user_folder_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_folder_folder FOREIGN KEY (folder_id) REFERENCES folders (id) ON DELETE CASCADE
);

CREATE TABLE contacts_in_user_folder(
    id INT NOT NULL AUTO_INCREMENT,
    user_id BINARY(16) NOT NULL,
    contact_id INT NOT NULL,
    folder_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY user_contact_folder (user_id, contact_id, folder_id),
    CONSTRAINT fk_user_contact_folder_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_contact_folder_contact FOREIGN KEY (contact_id) REFERENCES contacts (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_contact_folder_folder FOREIGN KEY (folder_id) REFERENCES folders (id) ON DELETE CASCADE
);



