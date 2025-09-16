import streamlit as st
from config import get_conn
from datetime import datetime
conn = get_conn()

def login_user(username, password):
    hashed_password = password
    with conn.cursor() as cur:
        cur.execute("""
            SELECT u.id, u.username, u.tipo_usuario, u.email, p.nombre, p.apellido
            FROM usuarios u
            JOIN perfiles p ON u.id = p.usuario_id
            WHERE u.username = %s AND u.password_hash = %s AND u.activo = TRUE
        """, (username, hashed_password))
        user = cur.fetchone()
        
        if user:
            # Actualizar último login
            cur.execute("UPDATE usuarios SET ultimo_login = NOW() WHERE id = %s", (user['id'],))
            conn.commit()
            
            return user
    return None

def register_user(user_data):
    try:
        with conn.cursor() as cur:
            # Llamar al procedimiento almacenado
            cur.execute("CALL crear_usuario_completo(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)",
                       (user_data['username'], 
                        user_data['password'],
                        user_data['email'],
                        user_data['tipo_usuario'],
                        user_data['nombre'],
                        user_data['apellido'],
                        user_data['fecha_nacimiento'],
                        user_data['genero'],
                        user_data['telefono'],
                        user_data['direccion']))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Error al registrar usuario: {e}")
        return False

def show_login_form():
    st.title("Inicio de Sesión - Sistema de Gestión Médica")
    
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión")
        
        if submitted:
            user = login_user(username, password)
            if user:
                st.session_state.user_id = user['id']
                st.session_state.user_role = user['tipo_usuario']
                st.session_state.user_name = f"{user['nombre']} {user['apellido']}"
                st.success(f"Bienvenido, {st.session_state.user_name}!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
    
    # Opción para registrarse
    if st.button("¿No tienes cuenta? Regístrate aquí"):
        st.session_state.show_register = True
        st.rerun()

def show_register_form():
    st.title("Registro de Nuevo Usuario")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre")
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            fecha_nacimiento = st.date_input("Fecha de Nacimiento", 
                                           min_value=datetime(1900, 1, 1),
                                           max_value=datetime.today())
        with col2:
            apellido = st.text_input("Apellido")
            email = st.text_input("Email")
            confirm_password = st.text_input("Confirmar Contraseña", type="password")
            genero = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])
        
        telefono = st.text_input("Teléfono")
        direccion = st.text_area("Dirección")
        tipo_usuario = st.selectbox("Tipo de Usuario", ['paciente'])
        
        submitted = st.form_submit_button("Registrarse")
        
        if submitted:
            if password != confirm_password:
                st.error("Las contraseñas no coinciden")
            else:
                user_data = {
                    'username': username,
                    'password': password,
                    'email': email,
                    'tipo_usuario': tipo_usuario,
                    'nombre': nombre,
                    'apellido': apellido,
                    'fecha_nacimiento': fecha_nacimiento,
                    'genero': genero,
                    'telefono': telefono,
                    'direccion': direccion
                }
                
                if register_user(user_data):
                    st.success("Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
                    st.session_state.show_register = False
                    st.rerun()
    
    if st.button("Volver al Login"):
        st.session_state.show_register = False
        st.rerun()
