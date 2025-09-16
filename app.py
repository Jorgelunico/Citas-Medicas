import streamlit as st
from config import is_logged_in, redirect_to_login, get_user_role
from auth import show_login_form, show_register_form
import pacientes
import citas
import historial
import dashboard
import reportes

def main():
    # Mover set_page_config al inicio para evitar error
    st.set_page_config(
        page_title="Sistema de Gestión Médica",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Verificar si el usuario está logueado
    if not is_logged_in():
        if st.session_state.get('show_register', False):
            show_register_form()
        else:
            show_login_form()
        return
    
    # Sidebar con navegación
    with st.sidebar:
        st.title(f"👋 Hola, {st.session_state.user_name}")
        st.write(f"Rol: {st.session_state.user_role.capitalize()}")
        st.divider()
        
        # Menú de navegación según el rol
        menu_options = ["Dashboard"]
        
        if st.session_state.user_role in ['admin', 'medico', 'recepcionista']:
            menu_options.extend(["Gestión de Pacientes", "Gestión de Citas"])
        
        if st.session_state.user_role in ['admin', 'medico']:
            menu_options.extend(["Historial Médico", "Reportes"])
        
        if st.session_state.user_role == 'paciente':
            menu_options.extend(["Mis Citas", "Mi Historial"])
        
        selected_option = st.radio("Navegación", menu_options)
        
        st.divider()
        if st.button("Cerrar Sesión"):
            redirect_to_login()
    
    # Contenido principal según la selección
    if selected_option == "Dashboard":
        dashboard.show_dashboard()
    elif selected_option == "Gestión de Pacientes":
        pacientes.show_patient_management()
    elif selected_option == "Gestión de Citas":
        citas.show_appointment_management()
    elif selected_option == "Historial Médico":
        historial.show_medical_history()
    elif selected_option == "Reportes":
        reportes.show_reports()
    elif selected_option == "Mis Citas":
        citas.show_patient_appointments()
    elif selected_option == "Mi Historial":
        historial.show_patient_medical_history()

if __name__ == "__main__":
    main()
