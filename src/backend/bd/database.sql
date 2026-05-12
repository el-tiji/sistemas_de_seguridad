CREATE DATABASE IF NOT EXISTS sgsi;
USE sgsi;

CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    rol VARCHAR(50)
);

CREATE TABLE control (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20),
    descripcion TEXT,
    estado VARCHAR(50)
);