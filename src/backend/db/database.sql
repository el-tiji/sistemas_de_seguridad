CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    rol VARCHAR(50),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- ORGANIZACION
-- =========================
CREATE TABLE organizacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200),
    descripcion TEXT,
    alcance_sgsi TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- CONTROLES ISO
-- =========================
CREATE TABLE control (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20),
    nombre VARCHAR(255),
    descripcion TEXT,
    estado VARCHAR(50),
    version_norma VARCHAR(50)
);

-- =========================
-- SOA (Cabecera)
-- =========================
CREATE TABLE soa (
    id INT AUTO_INCREMENT PRIMARY KEY,

    organizacion_id INT,

    version INT NOT NULL,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    responsable VARCHAR(100),

    descripcion TEXT,

    estado VARCHAR(50),

    FOREIGN KEY (organizacion_id)
    REFERENCES organizacion(id)
    ON DELETE CASCADE
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

    justificacion_inclusion TEXT,

    justificacion_exclusion TEXT,

    estado_implementacion VARCHAR(50),

    FOREIGN KEY (soa_id)
    REFERENCES soa(id)
    ON DELETE CASCADE,

    FOREIGN KEY (control_id)
    REFERENCES control(id)
    ON DELETE CASCADE
);

-- =========================
-- RIESGOS
-- =========================
CREATE TABLE riesgo (
    id INT AUTO_INCREMENT PRIMARY KEY,

    organizacion_id INT,

    descripcion TEXT,

    impacto VARCHAR(50),

    probabilidad VARCHAR(50),

    nivel_riesgo VARCHAR(50),

    tratamiento VARCHAR(50),

    fecha_identificacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (organizacion_id)
    REFERENCES organizacion(id)
    ON DELETE CASCADE
);

-- =========================
-- RELACION RIESGO-CONTROL
-- =========================
CREATE TABLE riesgo_control (
    id INT AUTO_INCREMENT PRIMARY KEY,

    riesgo_id INT,

    control_id INT,

    FOREIGN KEY (riesgo_id)
    REFERENCES riesgo(id)
    ON DELETE CASCADE,

    FOREIGN KEY (control_id)
    REFERENCES control(id)
    ON DELETE CASCADE
);

-- =========================
-- AUDITORIAS
-- =========================
CREATE TABLE auditoria (
    id INT AUTO_INCREMENT PRIMARY KEY,

    organizacion_id INT,

    tipo VARCHAR(50),

    fecha_inicio DATE,

    fecha_fin DATE,

    auditor VARCHAR(100),

    resultado TEXT,

    FOREIGN KEY (organizacion_id)
    REFERENCES organizacion(id)
    ON DELETE CASCADE
);

-- =========================
-- HALLAZGOS
-- =========================
CREATE TABLE hallazgo (
    id INT AUTO_INCREMENT PRIMARY KEY,

    auditoria_id INT,

    control_id INT,

    tipo VARCHAR(50),

    descripcion TEXT,

    estado VARCHAR(50),

    FOREIGN KEY (auditoria_id)
    REFERENCES auditoria(id)
    ON DELETE CASCADE,

    FOREIGN KEY (control_id)
    REFERENCES control(id)
    ON DELETE SET NULL
);