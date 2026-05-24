CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- ORGANIZACION
-- =========================
CREATE TABLE organizacion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    alcance_sgsi TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- CONTROLES ISO
-- =========================
CREATE TABLE control (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(255),
    descripcion TEXT,
    estado VARCHAR(50),
    version_norma VARCHAR(50)
);

-- =========================
-- SOA
-- =========================
CREATE TABLE soa (
    id SERIAL PRIMARY KEY,

    organizacion_id INTEGER NOT NULL,

    version INTEGER NOT NULL,

    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    responsable VARCHAR(100),

    descripcion TEXT,

    estado VARCHAR(50),

    CONSTRAINT fk_soa_organizacion
        FOREIGN KEY (organizacion_id)
        REFERENCES organizacion(id)
        ON DELETE CASCADE
);

-- =========================
-- RELACION SOA-CONTROL
-- =========================
CREATE TABLE soa_control (

    id SERIAL PRIMARY KEY,

    soa_id INTEGER NOT NULL,

    control_id INTEGER NOT NULL,

    aplica BOOLEAN NOT NULL DEFAULT TRUE,

    justificacion_inclusion TEXT,

    justificacion_exclusion TEXT,

    estado_implementacion VARCHAR(50),

    CONSTRAINT fk_soa_control_soa
        FOREIGN KEY (soa_id)
        REFERENCES soa(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_soa_control_control
        FOREIGN KEY (control_id)
        REFERENCES control(id)
        ON DELETE CASCADE
);

-- =========================
-- RIESGOS
-- =========================
CREATE TABLE riesgo (

    id SERIAL PRIMARY KEY,

    organizacion_id INTEGER NOT NULL,

    descripcion TEXT NOT NULL,

    impacto VARCHAR(50),

    probabilidad VARCHAR(50),

    nivel_riesgo VARCHAR(50),

    tratamiento VARCHAR(50),

    fecha_identificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_riesgo_organizacion
        FOREIGN KEY (organizacion_id)
        REFERENCES organizacion(id)
        ON DELETE CASCADE
);

-- =========================
-- RELACION RIESGO-CONTROL
-- =========================
CREATE TABLE riesgo_control (

    id SERIAL PRIMARY KEY,

    riesgo_id INTEGER NOT NULL,

    control_id INTEGER NOT NULL,

    CONSTRAINT fk_riesgo_control_riesgo
        FOREIGN KEY (riesgo_id)
        REFERENCES riesgo(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_riesgo_control_control
        FOREIGN KEY (control_id)
        REFERENCES control(id)
        ON DELETE CASCADE
);

-- =========================
-- AUDITORIAS
-- =========================
CREATE TABLE auditoria (

    id SERIAL PRIMARY KEY,

    organizacion_id INTEGER NOT NULL,

    tipo VARCHAR(50),

    fecha_inicio DATE,

    fecha_fin DATE,

    auditor VARCHAR(100),

    resultado TEXT,

    CONSTRAINT fk_auditoria_organizacion
        FOREIGN KEY (organizacion_id)
        REFERENCES organizacion(id)
        ON DELETE CASCADE
);

-- =========================
-- HALLAZGOS
-- =========================
CREATE TABLE hallazgo (

    id SERIAL PRIMARY KEY,

    auditoria_id INTEGER NOT NULL,

    control_id INTEGER,

    tipo VARCHAR(50),

    descripcion TEXT,

    estado VARCHAR(50),

    CONSTRAINT fk_hallazgo_auditoria
        FOREIGN KEY (auditoria_id)
        REFERENCES auditoria(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_hallazgo_control
        FOREIGN KEY (control_id)
        REFERENCES control(id)
        ON DELETE SET NULL
);