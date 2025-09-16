-- Insertar datos de ejemplo en la tabla usuarios
INSERT INTO usuarios (username, password_hash, email, tipo_usuario) VALUES
('admin1', 'e00cf25ad42683b3df678c61f42c6bda', 'admin@example.com', 'admin'), -- password1: admin1
('medico1', 'a1b2c3d4e5f678901234567890123456', 'medico1@example.com', 'medico'), -- password: medico1
('medico2', 'b2c3d4e5f67890123456789012345678', 'medico2@example.com', 'medico'), -- password: medico2
('paciente1', 'c3d4e5f6789012345678901234567890', 'paciente1@example.com', 'paciente'), -- password: paciente1
('paciente2', 'd4e5f678901234567890123456789012', 'paciente2@example.com', 'paciente'), -- password: paciente2
('recepcionista1', 'e5f67890123456789012345678901234', 'recepcionista@example.com', 'recepcionista'); -- password: recepcionista1

-- Insertar datos de ejemplo en la tabla perfiles
INSERT INTO perfiles (usuario_id, nombre, apellido, fecha_nacimiento, genero, telefono, direccion, especialidad, numero_licencia) VALUES
(1, 'Admin', 'User', '1980-01-01', 'Masculino', '123456789', 'Calle Admin 123', NULL, NULL),
(2, 'Dr. Juan', 'Perez', '1975-05-15', 'Masculino', '987654321', 'Calle Medico 456', 'Cardiologia', 'LIC12345'),
(3, 'Dra. Maria', 'Lopez', '1980-10-20', 'Femenino', '555666777', 'Calle Medico 789', 'Pediatria', 'LIC67890'),
(4, 'Ana', 'Garcia', '1990-03-10', 'Femenino', '111222333', 'Calle Paciente 101', NULL, NULL),
(5, 'Carlos', 'Rodriguez', '1985-07-25', 'Masculino', '444555666', 'Calle Paciente 202', NULL, NULL),
(6, 'Recep', 'User', '1992-12-05', 'Femenino', '777888999', 'Calle Recep 303', NULL, NULL);

-- Insertar datos de ejemplo en la tabla pacientes
INSERT INTO pacientes (usuario_id, perfil_id, tipo_sangre, alergias, condiciones_cronicas, contacto_emergencia_nombre, contacto_emergencia_telefono, aseguradora, numero_poliza_seguro) VALUES
(4, 4, 'O+', 'Penicilina', 'Hipertension', 'Familia Garcia', '999000111', 'Seguro Salud', 'POL123'),
(5, 5, 'A-', 'Ninguna', 'Diabetes', 'Familia Rodriguez', '888777666', 'Seguro Vida', 'POL456');

-- Insertar datos de ejemplo en la tabla medicos
INSERT INTO medicos (usuario_id, perfil_id, especialidad_principal, subespecialidades, años_experiencia, horario_trabajo, estado) VALUES
(2, 2, 'Cardiologia', 'Ecocardiografia', 15, '{"lunes": "09:00-17:00", "martes": "09:00-17:00"}', 'activo'),
(3, 3, 'Pediatria', 'Neonatologia', 10, '{"miercoles": "08:00-16:00", "jueves": "08:00-16:00"}', 'activo');

-- Insertar datos de ejemplo en la tabla citas
INSERT INTO citas (paciente_id, medico_id, fecha_hora, duracion, tipo_consulta, estado, motivo_consulta, creado_por) VALUES
(1, 1, '2023-10-01 10:00:00', 30, 'Consulta General', 'programada', 'Dolor de pecho', 1),
(2, 2, '2023-10-02 14:00:00', 45, 'Control Pediatrico', 'confirmada', 'Revision anual', 6);

-- Insertar datos de ejemplo en la tabla historiales_medicos
INSERT INTO historiales_medicos (paciente_id, medico_id, cita_id, sintomas, diagnostico, tratamiento, prescripciones, notas_medicas) VALUES
(1, 1, 1, 'Dolor en el pecho', 'Angina', 'Medicamentos y descanso', '[{"medicamento": "Aspirina", "dosis": "100mg"}]', 'Paciente estable'),
(2, 2, 2, 'Fiebre', 'Infeccion respiratoria', 'Antibioticos', '[{"medicamento": "Amoxicilina", "dosis": "500mg"}]', 'Mejorando');

-- Insertar datos de ejemplo en la tabla signos_vitales
INSERT INTO signos_vitales (historial_id, presion_arterial, frecuencia_cardiaca, temperatura, saturacion_oxigeno, peso, altura, imc, glucosa) VALUES
(1, '120/80', 72, 36.5, 98, 70.5, 1.75, 23.0, 90.0),
(2, '110/70', 80, 38.0, 96, 25.0, 1.20, 17.4, 100.0);
