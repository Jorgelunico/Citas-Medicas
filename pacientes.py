import streamlit as st
from config import get_conn
conn = get_conn()

def show_patient_management():
    st.title("Gestión de Pacientes")
    
    tab1, tab2, tab3 = st.tabs(["Buscar Pacientes", "Registrar Nuevo Paciente", "Historial Completo"])
    
    with tab1:
        st.subheader("Buscar Pacientes")
        search_term = st.text_input("Buscar por nombre, apellido o documento")
        
        if search_term:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT p.id, pr.nombre, pr.apellido, pr.telefono, p.tipo_sangre, p.aseguradora
                    FROM pacientes p
                    JOIN perfiles pr ON p.perfil_id = pr.id
                    WHERE pr.nombre ILIKE %s OR pr.apellido ILIKE %s
                """, (f"%{search_term}%", f"%{search_term}%"))
                
                pacientes = cur.fetchall()
                
                if pacientes:
                    for paciente in pacientes:
                        with st.expander(f"{paciente['nombre']} {paciente['apellido']}"):
                            st.write(f"Teléfono: {paciente['telefono']}")
                            st.write(f"Tipo de sangre: {paciente['tipo_sangre'] or 'No especificado'}")
                            st.write(f"Aseguradora: {paciente['aseguradora'] or 'No especificada'}")
                            # if st.button("Ver detalles completos", key=f"det_{paciente['id']}"):
                            #     st.session_state.selected_patient = paciente['id']
                            #     st.rerun()
                else:
                    st.info("No se encontraron pacientes con ese criterio de búsqueda")
    
    with tab2:
        st.subheader("Registrar Nuevo Paciente")
        # Formulario de registro de paciente (similar al de registro de usuario pero con campos médicos adicionales)
    
    with tab3:
        if 'selected_patient' in st.session_state:
            show_patient_details(st.session_state.selected_patient)

def show_patient_details(patient_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.*, pr.*, u.email
            FROM pacientes p
            JOIN perfiles pr ON p.perfil_id = pr.id
            JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.id = %s
        """, (patient_id,))
        
        paciente = cur.fetchone()
        
        if paciente:
            st.title(f"Historial de {paciente['nombre']} {paciente['apellido']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Información Personal")
                st.write(f"Email: {paciente['email']}")
                st.write(f"Teléfono: {paciente['telefono']}")
                st.write(f"Fecha de Nacimiento: {paciente['fecha_nacimiento']}")
                st.write(f"Género: {paciente['genero']}")
                st.write(f"Dirección: {paciente['direccion']}")
            
            with col2:
                st.subheader("Información Médica")
                st.write(f"Tipo de Sangre: {paciente['tipo_sangre'] or 'No especificado'}")
                st.write(f"Aseguradora: {paciente['aseguradora'] or 'No especificada'}")
                st.write(f"Número de Póliza: {paciente['numero_poliza_seguro'] or 'No especificado'}")
                st.write(f"Alergias: {paciente['alergias'] or 'Ninguna registrada'}")
                st.write(f"Condiciones Crónicas: {paciente['condiciones_cronicas'] or 'Ninguna registrada'}")
            
            # Mostrar historial médico del paciente
            st.subheader("Historial de Consultas")
            cur.execute("SELECT * FROM obtener_historial_paciente(%s)", (patient_id,))
            historial = cur.fetchall()
            
            if historial:
                for consulta in historial:
                    with st.expander(f"Consulta del {consulta['fecha_consulta'].strftime('%d/%m/%Y')} con Dr. {consulta['medico_nombre']} {consulta['medico_apellido']}"):
                        st.write(f"Síntomas: {consulta['sintomas']}")
                        st.write(f"Diagnóstico: {consulta['diagnostico']}")
                        st.write(f"Tratamiento: {consulta['tratamiento']}")
                        if consulta['prescripciones']:
                            st.write("Prescripciones:")
                            st.json(consulta['prescripciones'])
            else:
                st.info("No hay historial médico registrado para este paciente")
