# Manual de Usuario - Sistema de Gestión Médica

## Introducción

Bienvenido al Sistema de Gestión Médica, una aplicación web diseñada para facilitar la administración de citas médicas, pacientes, historial médico y reportes. Este sistema está construido con Streamlit para la interfaz de usuario y PostgreSQL como base de datos, todo containerizado con Docker para una fácil implementación.

### Características Principales
- **Gestión de Usuarios**: Autenticación con roles diferenciados (Administrador, Médico, Recepcionista, Paciente).
- **Gestión de Pacientes**: Registro y administración de información de pacientes.
- **Gestión de Citas**: Programación, visualización y gestión de citas médicas.
- **Historial Médico**: Registro y consulta del historial médico de pacientes.
- **Dashboard**: Vista general del estado del sistema.
- **Reportes**: Generación de estadísticas y reportes.

## Instalación

### Requisitos Previos
- Docker instalado en tu sistema.
- Docker Compose instalado.

### Pasos de Instalación
1. **Descarga o clona el proyecto** en tu directorio local.
2. **Navega al directorio del proyecto**:
   ```bash
   cd citas-medicas
   ```
3. **Construye y ejecuta los contenedores**:
   ```bash
   docker-compose up --build
   ```
4. **Accede a la aplicación** abriendo tu navegador en: `http://localhost:8501`

### Configuración Inicial
- La base de datos se inicializa automáticamente con las tablas necesarias.
- Usuario administrador por defecto: `admin` / `admin123` (cambia esto en producción).

## Inicio de Sesión

1. Al acceder a la aplicación, verás el formulario de inicio de sesión.
2. Ingresa tu nombre de usuario y contraseña.
3. Si no tienes cuenta, selecciona "Registrarse" para crear una nueva cuenta (dependiendo de la configuración del sistema).
4. Una vez autenticado, serás redirigido al dashboard principal.

### Roles de Usuario
- **Administrador**: Acceso completo a todas las funcionalidades.
- **Médico**: Gestión de pacientes, citas, historial médico y reportes.
- **Recepcionista**: Gestión de pacientes y citas.
- **Paciente**: Vista de sus propias citas e historial médico.

## Navegación

La aplicación utiliza una barra lateral para la navegación. Las opciones disponibles dependen de tu rol:

- **Dashboard**: Vista general del sistema.
- **Gestión de Pacientes**: (Disponible para Admin, Médico, Recepcionista)
- **Gestión de Citas**: (Disponible para Admin, Médico, Recepcionista)
- **Historial Médico**: (Disponible para Admin, Médico)
- **Reportes**: (Disponible para Admin, Médico)
- **Mis Citas**: (Disponible para Paciente)
- **Mi Historial**: (Disponible para Paciente)

## Funcionalidades por Rol

### Administrador
- **Dashboard**: Vista completa del estado del sistema.
- **Gestión de Pacientes**: Crear, editar y eliminar pacientes.
- **Gestión de Citas**: Programar, editar y cancelar citas.
- **Historial Médico**: Ver y actualizar historial de todos los pacientes.
- **Reportes**: Generar reportes estadísticos.

### Médico
- **Dashboard**: Vista de sus citas y pacientes.
- **Gestión de Pacientes**: Ver y editar información de pacientes asignados.
- **Gestión de Citas**: Programar y gestionar citas con sus pacientes.
- **Historial Médico**: Ver y actualizar historial médico.
- **Reportes**: Generar reportes de sus pacientes.

### Recepcionista
- **Dashboard**: Vista de citas programadas.
- **Gestión de Pacientes**: Registrar nuevos pacientes y actualizar información básica.
- **Gestión de Citas**: Programar citas y gestionar el calendario.

### Paciente
- **Mis Citas**: Ver citas programadas, cancelar citas futuras.
- **Mi Historial**: Ver su propio historial médico.

## Gestión de Pacientes

### Agregar Paciente
1. Ve a "Gestión de Pacientes".
2. Completa el formulario con la información requerida (nombre, apellido, fecha de nacimiento, etc.).
3. Guarda los cambios.

### Editar Paciente
1. Selecciona un paciente de la lista.
2. Modifica la información necesaria.
3. Guarda los cambios.

## Gestión de Citas

### Programar Cita
1. Ve a "Gestión de Citas" > "Agendar Cita".
2. Selecciona paciente y médico.
3. Elige fecha, hora, duración y tipo de consulta.
4. Ingresa el motivo de la consulta.
5. Confirma la programación.

### Ver Calendario
- En "Gestión de Citas" > "Calendario de Citas", puedes ver todas las citas programadas.

### Gestionar Citas Existentes
- Edita o cancela citas según sea necesario.

## Historial Médico

### Ver Historial
1. Ve a "Historial Médico".
2. Selecciona un paciente.
3. Revisa las entradas del historial.

### Agregar Entrada
1. Selecciona un paciente.
2. Completa el formulario con la información médica.
3. Guarda la entrada.

## Reportes

### Generar Reportes
1. Ve a "Reportes".
2. Selecciona el tipo de reporte deseado.
3. Ajusta los filtros (fechas, pacientes, etc.).
4. Genera y descarga el reporte.

## Solución de Problemas

### No puedo iniciar sesión
- Verifica que tu nombre de usuario y contraseña sean correctos.
- Si olvidaste tu contraseña, contacta al administrador.

### Error de conexión
- Asegúrate de que Docker esté ejecutándose.
- Verifica que los contenedores estén activos: `docker-compose ps`

### Problemas de rendimiento
- Reinicia los contenedores: `docker-compose restart`

## Seguridad

- Siempre cierra sesión al terminar de usar la aplicación.
- No compartas tus credenciales.
- Reporta cualquier actividad sospechosa al administrador.

## Soporte

Para soporte técnico o preguntas adicionales, contacta al administrador del sistema o al equipo de desarrollo.

---

*Este manual está basado en la versión actual del sistema. Las funcionalidades pueden variar en futuras actualizaciones.*
