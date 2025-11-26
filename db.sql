CREATE DATABASE IF NOT EXISTS portfolio_db;
USE portfolio_db;

-- Tabla para información personal
CREATE TABLE IF NOT EXISTS informacion_personal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla para experiencia laboral
CREATE TABLE IF NOT EXISTS experiencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    puesto VARCHAR(100) NOT NULL,
    empresa VARCHAR(100) NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    descripcion TEXT
);

-- Tabla para educación
CREATE TABLE IF NOT EXISTS educacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    institucion VARCHAR(100) NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE
);

-- Tabla para habilidades (duras y blandas)
CREATE TABLE IF NOT EXISTS habilidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nivel INT,
    tipo ENUM('dura', 'blanda') NOT NULL
);

-- Tabla para proyectos
CREATE TABLE IF NOT EXISTS proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha DATE,
    enlace VARCHAR(255)
);

ALTER TABLE habilidades ADD COLUMN tipo ENUM('dura', 'blanda');


-- Insertar datos de ejemplo
INSERT INTO informacion_personal (nombre, apellido, titulo, descripcion)
VALUES ('Santino', 'Macchiarola', 'Desarrollador Full Stack Jr.', 'Soy un apasionado por la robotica y por aprender cosas nuevas.');

INSERT INTO experiencia (puesto, empresa, fecha_inicio, fecha_fin, descripcion)
VALUES ('Desarrollador Jr.', 'Empresa Ejemplo', '2020-01-01', '2022-12-05', 'Desarrollé aplicaciones web utilizando Python y Flask.');

INSERT INTO educacion (titulo, institucion, fecha_inicio, fecha_fin)
VALUES ('Técnico en Programación', 'Instituto Tecnico Renault', '2020-01-01', '2026-12-05');

INSERT INTO habilidades (nombre, nivel, tipo)
VALUES ('Python', 3, 'dura'), ('HTML/CSS', 4, 'dura'), ('C++', 3, 'dura'), ('JavaScript', 4, 'dura'), ('React', 3, 'dura'),
       ('Trabajo en equipo', 4, 'blanda'), ('Comunicación', 5, 'blanda'), ('Liderazgo', 3, 'blanda'),
       ('Resolución de problemas', 5, 'blanda'), ('Gestión del tiempo', 4, 'blanda');

INSERT INTO proyectos (nombre, descripcion, fecha, enlace)
VALUES ('Portfolio Web', 'Desarrollo de mi portfolio.', '2025-11-26', 'https://ejemplo.com');
