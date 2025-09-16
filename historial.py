import streamlit as st
from config import get_conn
import json
conn = get_conn()

def show_medical_history():
    st.title("Historial Médico")
    
    # Buscar paciente primero
    search_term = st.text_input("Buscar paciente para ver historial")
    
    if search_term:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.id, pr.nombre, pr.apellido 
                FROM pacientes p 
                JOIN perfiles pr ON p.perfil_id = pr.id 
                WHERE pr.nombre ILIKE %s OR pr.apellido ILIKE %s
            """, (f"%{search_term}%", f"%{search_term}%"))
            
            pacientes = cur.fetchall()
            
            if pacientes:
                selected_patient = st.selectbox(
                    "Seleccionar paciente",
                    options=[f"{p['nombre']} {p['apellido']}" for p in pacientes],
                    key="patient_select"
                )
                
                patient_id = next(p['id'] for p in pacientes if f"{p['nombre']} {p['apellido']}" == selected_patient)
                
                # Mostrar historial del paciente seleccionado
                show_patient_medical_history(patient_id, is_doctor=True)
            else:
                st.info("No se encontraron pacientes con ese nombre")

def show_patient_medical_history(patient_id=None, is_doctor=False):
    if not patient_id:
        # Obtener el ID del paciente actual
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM pacientes WHERE usuario_id = %s", (st.session_state.user_id,))
            paciente = cur.fetchone()
            if paciente:
                patient_id = paciente['id']
            else:
                st.error("No se encontró información de paciente")
                return
    
    # Mostrar historial médico
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM obtener_historial_paciente(%s)", (patient_id,))
        historial = cur.fetchall()
        
        if historial:
            for consulta in historial:
                with st.expander(f"Consulta del {consulta['fecha_consulta'].strftime('%d/%m/%Y')} con Dr. {consulta['medico_nombre']} {consulta['medico_apellido']}"):
                    st.subheader("Síntomas")
                    st.write(consulta['sintomas'] or "No registrado")
                    
                    st.subheader("Diagnóstico")
                    st.write(consulta['diagnostico'] or "No registrado")
                    
                    st.subheader("Tratamiento")
                    st.write(consulta['tratamiento'] or "No registrado")
                    
                    if consulta['prescripciones']:
                        try:
                            prescripciones = json.loads(consulta['prescripciones'])
                            st.subheader("Medicamentos Recetados")
                            for med in prescripciones:
                                st.write(f"- {med['nombre']}: {med['dosis']} cada {med['frecuencia']} durante {med['duracion']}")
                        except:
                            st.write("Prescripciones:", consulta['prescripciones'])
        else:
            st.info("No hay historial médico registrado")

def record_medical_consultation():
    st.title("Registrar Nueva Consulta")
    
    # Formulario para registrar una nueva consulta médica
    # Similar al formulario de agendar cita pero con campos médicos completos
