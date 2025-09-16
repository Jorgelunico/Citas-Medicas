# Sistema de Gestión Médica (Citas-Medicas)

## Descripción

Una aplicación web diseñada para facilitar la administración de citas médicas, pacientes, historial médico y reportes. Este sistema está construido con Streamlit para la interfaz de usuario y PostgreSQL como base de datos, todo containerizado con Docker para una fácil implementación y despliegue.

## Características Principales

- **Gestión de Usuarios**: Autenticación con roles diferenciados (Administrador, Médico, Recepcionista, Paciente).
- **Gestión de Pacientes**: Registro y administración de información de pacientes.
- **Gestión de Citas**: Programación, visualización y gestión de citas médicas.
- **Historial Médico**: Registro y consulta del historial médico de pacientes.
- **Dashboard**: Vista general del estado del sistema.
- **Reportes**: Generación de estadísticas y reportes.

## Requisitos Previos

- Docker instalado en tu sistema.
- Docker Compose instalado.
- (Opcional) Python 3.8+ si deseas ejecutar sin Docker.

## Instalación

### Usando Docker (Recomendado)

1. **Clona o descarga el proyecto** en tu directorio local.
2. **Navega al directorio del proyecto**:
   ```bash
   cd citas-medicas
   ```
3. **Construye y ejecuta los contenedores**:
   ```bash
   docker-compose up --build
   ```
4. **Accede a la aplicación** abriendo tu navegador en: `http://localhost:8501`

### Sin Docker

1. Instala las dependencias:
   ```bash
   pip install -r requeriments.txt
   ```
2. Configura la base de datos PostgreSQL (o ajusta config.py para SQLite).
3. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```

## Configuración Inicial

- La base de datos se inicializa automáticamente con las tablas necesarias usando `init.sql` y `populate.sql`.
- Usuario administrador por defecto: `admin` / `admin123` (cambia esto en producción).

## Uso

1. Accede a la aplicación en tu navegador.
2. Inicia sesión con tus credenciales.
3. Navega usando la barra lateral según tu rol.
4. Consulta el [Manual de Usuario](MANUAL_USUARIO.md) para instrucciones detalladas.

## Estructura del Proyecto

- `app.py`: Punto de entrada principal de la aplicación.
- `auth.py`: Manejo de autenticación y registro.
- `config.py`: Configuraciones y utilidades de sesión.
- `pacientes.py`: Módulo de gestión de pacientes.
- `citas.py`: Módulo de gestión de citas.
- `historial.py`: Módulo de historial médico.
- `dashboard.py`: Módulo del dashboard.
- `reportes.py`: Módulo de reportes.
- `init.sql`: Script de inicialización de la base de datos.
- `populate.sql`: Script para poblar la base de datos con datos de ejemplo.
- `Dockerfile`: Configuración para construir la imagen Docker.
- `docker-compose.yml`: Configuración de servicios Docker.
- `requeriments.txt`: Dependencias de Python.

## Contribución

1. Haz un fork del proyecto.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`).
4. Push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas adicionales, consulta el [Manual de Usuario](MANUAL_USUARIO.md) o contacta al equipo de desarrollo.

