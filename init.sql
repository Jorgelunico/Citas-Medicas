CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    tipo_usuario VARCHAR(20) CHECK (tipo_usuario IN ('admin', 'medico', 'recepcionista', 'paciente')),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE perfiles (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    genero VARCHAR(20),
    telefono VARCHAR(20),
    direccion TEXT,
    foto_url TEXT,
    especialidad VARCHAR(100), -- Solo para médicos
    numero_licencia VARCHAR(100), -- Solo para médicos
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de pacientes
CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    perfil_id INTEGER REFERENCES perfiles(id) ON DELETE CASCADE,
    tipo_sangre VARCHAR(5),
    alergias TEXT,
    condiciones_cronicas TEXT,
    contacto_emergencia_nombre VARCHAR(100),
    contacto_emergencia_telefono VARCHAR(20),
    aseguradora VARCHAR(100),
    numero_poliza_seguro VARCHAR(100),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de médicos
CREATE TABLE medicos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    perfil_id INTEGER REFERENCES perfiles(id) ON DELETE CASCADE,
    especialidad_principal VARCHAR(100) NOT NULL,
    subespecialidades TEXT,
    años_experiencia INTEGER,
    horario_trabajo TEXT, -- JSON con horario de trabajo
    estado VARCHAR(20) DEFAULT 'activo',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de citas
CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
    medico_id INTEGER REFERENCES medicos(id) ON DELETE CASCADE,
    fecha_hora TIMESTAMP NOT NULL,
    duracion INTEGER DEFAULT 30, -- Duración en minutos
    tipo_consulta VARCHAR(50),
    estado VARCHAR(20) CHECK (estado IN ('programada', 'confirmada', 'completada', 'cancelada', 'no_asistio')) DEFAULT 'programada',
    motivo_consulta TEXT,
    notas_antes_consulta TEXT,
    recordatorio_enviado BOOLEAN DEFAULT FALSE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creado_por INTEGER REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Tabla de historial médico
CREATE TABLE historiales_medicos (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER REFERENCES pacientes(id) ON DELETE CASCADE,
    medico_id INTEGER REFERENCES medicos(id) ON DELETE CASCADE,
    cita_id INTEGER REFERENCES citas(id) ON DELETE SET NULL,
    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sintomas TEXT,
    diagnostico TEXT,
    tratamiento TEXT,
    prescripciones TEXT, -- JSON con medicamentos recetados
    notas_medicas TEXT,
    archivos_adjuntos TEXT, -- JSON con rutas de archivos
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de signos vitales
CREATE TABLE signos_vitales (
    id SERIAL PRIMARY KEY,
    historial_id INTEGER REFERENCES historiales_medicos(id) ON DELETE CASCADE,
    presion_arterial VARCHAR(10),
    frecuencia_cardiaca INTEGER,
    temperatura DECIMAL(4,1),
    saturacion_oxigeno INTEGER,
    peso DECIMAL(5,2),
    altura DECIMAL(3,2),
    imc DECIMAL(4,1),
    glucosa DECIMAL(5,2),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Procedimiento para crear un nuevo usuario con perfil
CREATE OR REPLACE PROCEDURE crear_usuario_completo(
    p_username VARCHAR, 
    p_password_hash VARCHAR, 
    p_email VARCHAR, 
    p_tipo_usuario VARCHAR,
    p_nombre VARCHAR,
    p_apellido VARCHAR,
    p_fecha_nacimiento DATE,
    p_genero VARCHAR,
    p_telefono VARCHAR,
    p_direccion TEXT,
    INOUT p_usuario_id INTEGER DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Insertar en la tabla usuarios
    INSERT INTO usuarios (username, password_hash, email, tipo_usuario)
    VALUES (p_username, p_password_hash, p_email, p_tipo_usuario)
    RETURNING id INTO p_usuario_id;
    
    -- Insertar en la tabla perfiles
    INSERT INTO perfiles (usuario_id, nombre, apellido, fecha_nacimiento, genero, telefono, direccion)
    VALUES (p_usuario_id, p_nombre, p_apellido, p_fecha_nacimiento, p_genero, p_telefono, p_direccion);
    
    -- Si es paciente, crear registro en tabla pacientes
    IF p_tipo_usuario = 'paciente' THEN
        INSERT INTO pacientes (usuario_id, perfil_id)
        VALUES (p_usuario_id, currval('perfiles_id_seq'));
    END IF;
END;
$$;

-- Procedimiento para agendar una cita
CREATE OR REPLACE PROCEDURE agendar_cita(
    p_paciente_id INTEGER,
    p_medico_id INTEGER,
    p_fecha_hora TIMESTAMP,
    p_duracion INTEGER,
    p_tipo_consulta VARCHAR,
    p_motivo_consulta TEXT,
    p_creado_por INTEGER,
    INOUT p_cita_id INTEGER DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar disponibilidad del médico
    IF EXISTS (
        SELECT 1 FROM citas 
        WHERE medico_id = p_medico_id 
        AND fecha_hora = p_fecha_hora 
        AND estado IN ('programada', 'confirmada')
    ) THEN
        RAISE EXCEPTION 'El médico no está disponible en ese horario';
    END IF;
    
    -- Insertar la cita
    INSERT INTO citas (paciente_id, medico_id, fecha_hora, duracion, tipo_consulta, motivo_consulta, creado_por)
    VALUES (p_paciente_id, p_medico_id, p_fecha_hora, p_duracion, p_tipo_consulta, p_motivo_consulta, p_creado_por)
    RETURNING id INTO p_cita_id;
END;
$$;

-- Función para obtener el historial médico de un paciente
CREATE OR REPLACE FUNCTION obtener_historial_paciente(p_paciente_id INTEGER)
RETURNS TABLE (
    fecha_consulta TIMESTAMP,
    medico_nombre VARCHAR,
    medico_apellido VARCHAR,
    sintomas TEXT,
    diagnostico TEXT,
    tratamiento TEXT,
    prescripciones TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        hm.fecha_consulta,
        p.nombre as medico_nombre,
        p.apellido as medico_apellido,
        hm.sintomas,
        hm.diagnostico,
        hm.tratamiento,
        hm.prescripciones
    FROM historiales_medicos hm
    JOIN medicos m ON hm.medico_id = m.id
    JOIN perfiles p ON m.perfil_id = p.id
    WHERE hm.paciente_id = p_paciente_id
    ORDER BY hm.fecha_consulta DESC;
END;
$$;

-- Procedimiento para registrar una consulta médica completa
CREATE OR REPLACE PROCEDURE registrar_consulta_completa(
    p_paciente_id INTEGER,
    p_medico_id INTEGER,
    p_cita_id INTEGER,
    p_sintomas TEXT,
    p_diagnostico TEXT,
    p_tratamiento TEXT,
    p_prescripciones TEXT,
    p_notas_medicas TEXT,
    p_presion_arterial VARCHAR,
    p_frecuencia_cardiaca INTEGER,
    p_temperatura DECIMAL,
    p_saturacion_oxigeno INTEGER,
    p_peso DECIMAL,
    p_altura DECIMAL,
    INOUT p_historial_id INTEGER DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_imc DECIMAL;
BEGIN
    -- Calcular IMC
    IF p_peso IS NOT NULL AND p_altura IS NOT NULL AND p_altura > 0 THEN
        v_imc := p_peso / (p_altura * p_altura);
    END IF;
    
    -- Insertar en historial médico
    INSERT INTO historiales_medicos (paciente_id, medico_id, cita_id, sintomas, diagnostico, tratamiento, prescripciones, notas_medicas)
    VALUES (p_paciente_id, p_medico_id, p_cita_id, p_sintomas, p_diagnostico, p_tratamiento, p_prescripciones, p_notas_medicas)
    RETURNING id INTO p_historial_id;
    
    -- Insertar signos vitales
    INSERT INTO signos_vitales (historial_id, presion_arterial, frecuencia_cardiaca, temperatura, saturacion_oxigeno, peso, altura, imc)
    VALUES (p_historial_id, p_presion_arterial, p_frecuencia_cardiaca, p_temperatura, p_saturacion_oxigeno, p_peso, p_altura, v_imc);
    
    -- Actualizar estado de la cita
    UPDATE citas SET estado = 'completada' WHERE id = p_cita_id;
END;
$$;

