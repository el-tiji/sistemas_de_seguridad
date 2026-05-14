-- =========================
-- USUARIOS
-- =========================
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    rol VARCHAR(50)
);

-- =========================
-- CONTROLES ISO
-- =========================
CREATE TABLE control (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20),
    descripcion TEXT,
    estado VARCHAR(50)
);

-- =========================
-- SOA (Cabecera)
-- =========================
CREATE TABLE soa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    version INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    responsable VARCHAR(100),
    descripcion TEXT
);

-- =========================
-- SOA DETALLE
-- Relación entre SOA y Controles
-- =========================
CREATE TABLE soa_detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    soa_id INT,
    control_id INT,
    incluido BOOLEAN NOT NULL,
    justificacion TEXT,

    FOREIGN KEY (soa_id) REFERENCES soa(id) ON DELETE CASCADE,
    FOREIGN KEY (control_id) REFERENCES control(id) ON DELETE CASCADE
);