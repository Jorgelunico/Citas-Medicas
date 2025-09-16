import streamlit as st
from config import get_conn
from datetime import datetime, timedelta
import calendar
conn = get_conn()


def show_appointment_management():
    st.title("Gestión de Citas")
    
    tab1, tab2, tab3 = st.tabs(["Agendar Cita", "Calendario de Citas", "Gestionar Citas"])
    
    with tab1:
        st.subheader("Agendar Nueva Cita")
        
        with conn.cursor() as cur:
            # Obtener lista de pacientes
            cur.execute("""
                SELECT p.id, pr.nombre, pr.apellido 
                FROM pacientes p 
                JOIN perfiles pr ON p.perfil_id = pr.id 
                ORDER BY pr.nombre, pr.apellido
            """)
            pacientes = cur.fetchall()
            paciente_options = {f"{p['nombre']} {p['apellido']}": p['id'] for p in pacientes}
            
            # Obtener lista de médicos
            cur.execute("""
                SELECT m.id, pr.nombre, pr.apellido, m.especialidad_principal
                FROM medicos m 
                JOIN perfiles pr ON m.perfil_id = pr.id 
                WHERE m.estado = 'activo'
                ORDER BY pr.nombre, pr.apellido
            """)
            medicos = cur.fetchall()
            medico_options = {f"Dr. {m['nombre']} {m['apellido']} ({m['especialidad_principal']})": m['id'] for m in medicos}
        
        col1, col2 = st.columns(2)
        with col1:
            selected_paciente = st.selectbox("Paciente", options=list(paciente_options.keys()))
            paciente_id = paciente_options[selected_paciente]
            
            fecha = st.date_input("Fecha de la cita", min_value=datetime.today())
            hora = st.time_input("Hora de la cita")
            
        with col2:
            selected_medico = st.selectbox("Médico", options=list(medico_options.keys()))
            medico_id = medico_options[selected_medico]
            
            duracion = st.number_input("Duración (minutos)", min_value=15, max_value=120, value=30, step=15)
            tipo_consulta = st.selectbox("Tipo de Consulta", 
                                       ["Consulta General", "Control", "Urgencia", "Examen", "Otro"])
        
        motivo = st.text_area("Motivo de la consulta")
        
        if st.button("Agendar Cita"):
            fecha_hora = datetime.combine(fecha, hora)
            try:
                with conn.cursor() as cur:
                    cur.execute("CALL agendar_cita(%s, %s, %s, %s, %s, %s, %s, NULL)",
                               (paciente_id, medico_id, fecha_hora, duracion, tipo_consulta, motivo, st.session_state.user_id))
                    conn.commit()
                    st.success("Cita agendada exitosamente")
            except Exception as e:
                st.error(f"Error al agendar la cita: {e}")
    
    with tab2:
        st.subheader("Calendario de Citas")

        # Selección de mes y año para mostrar
        today = datetime.today()
        year = st.selectbox("Año", options=[today.year + i for i in range(-1, 2)], index=1)
        month_name = st.selectbox("Mes", options=list(calendar.month_name)[1:], index=today.month - 1)
        month = list(calendar.month_name).index(month_name)

        # Obtener citas para el mes seleccionado
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.fecha_hora, c.duracion, c.tipo_consulta, c.estado,
                       pr.nombre as paciente_nombre, pr.apellido as paciente_apellido,
                       m.id as medico_id, mp.nombre as medico_nombre, mp.apellido as medico_apellido
                FROM citas c
                JOIN pacientes p ON c.paciente_id = p.id
                JOIN perfiles pr ON p.perfil_id = pr.id
                JOIN medicos m ON c.medico_id = m.id
                JOIN perfiles mp ON m.perfil_id = mp.id
                WHERE c.fecha_hora >= %s AND c.fecha_hora < %s
                ORDER BY c.fecha_hora
            """, (start_date, end_date))
            citas_mes = cur.fetchall()

        if not citas_mes:
            st.info("No hay citas programadas para este mes.")
        else:
            # Agrupar citas por día
            citas_por_dia = {}
            for cita in citas_mes:
                dia = cita['fecha_hora'].date()
                citas_por_dia.setdefault(dia, []).append(cita)

            for dia in sorted(citas_por_dia.keys()):
                st.markdown(f"### {dia.strftime('%A, %d de %B de %Y')}")
                for cita in citas_por_dia[dia]:
                    hora_fin = cita['fecha_hora'] + timedelta(minutes=cita['duracion'])
                    st.write(f"- {cita['fecha_hora'].strftime('%H:%M')} - {hora_fin.strftime('%H:%M')}: "
                             f"Cita con Dr. {cita['medico_nombre']} {cita['medico_apellido']} "
                             f"({cita['tipo_consulta']}) - Estado: {cita['estado'].capitalize()}")

    
    with tab3:
        st.subheader("Gestionar Citas Existentes")

        with conn.cursor() as cur:
            # Obtener todas las citas
            cur.execute("""
                SELECT c.id, c.fecha_hora, c.duracion, c.tipo_consulta, c.estado, c.motivo_consulta,
                       p.id as paciente_id, pr.nombre as paciente_nombre, pr.apellido as paciente_apellido,
                       m.id as medico_id, mp.nombre as medico_nombre, mp.apellido as medico_apellido
                FROM citas c
                JOIN pacientes p ON c.paciente_id = p.id
                JOIN perfiles pr ON p.perfil_id = pr.id
                JOIN medicos m ON c.medico_id = m.id
                JOIN perfiles mp ON m.perfil_id = mp.id
                ORDER BY c.fecha_hora DESC
            """)
            citas = cur.fetchall()

        if not citas:
            st.info("No hay citas registradas.")
        else:
            for cita in citas:
                with st.expander(f"Cita #{cita['id']} - {cita['fecha_hora'].strftime('%d/%m/%Y %H:%M')} - "
                                 f"Paciente: {cita['paciente_nombre']} {cita['paciente_apellido']} - "
                                 f"Dr. {cita['medico_nombre']} {cita['medico_apellido']}"):
                    st.write(f"Estado: {cita['estado'].capitalize()}")
                    st.write(f"Duración: {cita['duracion']} minutos")
                    st.write(f"Tipo de Consulta: {cita['tipo_consulta']}")
                    st.write(f"Motivo: {cita['motivo_consulta']}")

                    # Formulario para editar cita
                    with st.form(key=f"edit_form_{cita['id']}"):
                        new_fecha = st.date_input("Fecha", value=cita['fecha_hora'].date(), key=f"fecha_{cita['id']}")
                        new_hora = st.time_input("Hora", value=cita['fecha_hora'].time(), key=f"hora_{cita['id']}")
                        new_duracion = st.number_input("Duración (minutos)", min_value=15, max_value=120,
                                                      value=cita['duracion'], step=15, key=f"duracion_{cita['id']}")
                        new_tipo = st.selectbox("Tipo de Consulta",
                                               ["Consulta General", "Control", "Urgencia", "Examen", "Otro"],
                                               index=["Consulta General", "Control", "Urgencia", "Examen", "Otro"].index(cita['tipo_consulta']) if cita['tipo_consulta'] in ["Consulta General", "Control", "Urgencia", "Examen", "Otro"] else 0,
                                               key=f"tipo_{cita['id']}")
                        new_motivo = st.text_area("Motivo", value=cita['motivo_consulta'], key=f"motivo_{cita['id']}")

                        # Selección de médico
                        with conn.cursor() as cur:
                            cur.execute("""
                                SELECT m.id, pr.nombre, pr.apellido, m.especialidad_principal
                                FROM medicos m
                                JOIN perfiles pr ON m.perfil_id = pr.id
                                WHERE m.estado = 'activo'
                                ORDER BY pr.nombre, pr.apellido
                            """)
                            medicos = cur.fetchall()
                            medico_options = {f"Dr. {m['nombre']} {m['apellido']} ({m['especialidad_principal']})": m['id'] for m in medicos}
                        selected_medico_name = f"Dr. {cita['medico_nombre']} {cita['medico_apellido']} ({next((m['especialidad_principal'] for m in medicos if m['id'] == cita['medico_id']), '')})"
                        try:
                            index = list(medico_options.keys()).index(selected_medico_name)
                        except ValueError:
                            index = 0
                        new_medico = st.selectbox("Médico", options=list(medico_options.keys()), index=index, key=f"medico_{cita['id']}")

                        submitted = st.form_submit_button("Guardar Cambios")
                        if submitted:
                            new_fecha_hora = datetime.combine(new_fecha, new_hora)
                            new_medico_id = medico_options[new_medico]
                            # Verificar disponibilidad
                            with conn.cursor() as cur:
                                cur.execute("""
                                    SELECT 1 FROM citas
                                    WHERE medico_id = %s
                                    AND fecha_hora = %s
                                    AND estado IN ('programada', 'confirmada')
                                    AND id != %s
                                """, (new_medico_id, new_fecha_hora, cita['id']))
                                if cur.fetchone():
                                    st.error("El médico no está disponible en ese horario")
                                    return
                            try:
                                with conn.cursor() as cur:
                                    cur.execute("""
                                        UPDATE citas
                                        SET fecha_hora = %s,
                                            duracion = %s,
                                            tipo_consulta = %s,
                                            motivo_consulta = %s,
                                            medico_id = %s
                                        WHERE id = %s
                                    """, (new_fecha_hora, new_duracion, new_tipo, new_motivo, new_medico_id, cita['id']))
                                    conn.commit()
                                    st.success("Cita actualizada exitosamente")
                                    #st.rerun()
                            except Exception as e:
                                st.error(f"Error al actualizar la cita: {e}")

                    # Botón para cancelar cita si está programada
                    if cita['estado'] == 'programada':
                        if st.button("Cancelar Cita", key=f"cancel_{cita['id']}"):
                            cancel_appointment(cita['id'])

def show_patient_appointments():
    st.title("Mis Citas")
    
    with conn.cursor() as cur:
        # Obtener el ID del paciente actual
        cur.execute("SELECT id FROM pacientes WHERE usuario_id = %s", (st.session_state.user_id,))
        paciente = cur.fetchone()
        
        if paciente:
            paciente_id = paciente['id']
            
            # Obtener citas del paciente
            cur.execute("""
                SELECT c.*, m.id as medico_id, pr.nombre as medico_nombre, pr.apellido as medico_apellido
                FROM citas c
                JOIN medicos m ON c.medico_id = m.id
                JOIN perfiles pr ON m.perfil_id = pr.id
                WHERE c.paciente_id = %s
                ORDER BY c.fecha_hora DESC
            """, (paciente_id,))
            
            citas = cur.fetchall()
            
            if citas:
                for cita in citas:
                    with st.expander(f"Cita con Dr. {cita['medico_nombre']} {cita['medico_apellido']} - {cita['fecha_hora'].strftime('%d/%m/%Y %H:%M')}"):
                        st.write(f"Estado: {cita['estado'].capitalize()}")
                        st.write(f"Duración: {cita['duracion']} minutos")
                        st.write(f"Tipo: {cita['tipo_consulta']}")
                        st.write(f"Motivo: {cita['motivo_consulta']}")
                        
                        # Mostrar acciones según el estado
                        if cita['estado'] == 'programada' and cita['fecha_hora'] > datetime.now():
                            if st.button("Cancelar Cita", key=f"cancel_{cita['id']}"):
                                cancel_appointment(cita['id'])
            else:
                st.info("No tienes citas programadas")
        else:
            st.error("No se encontró información de paciente para tu usuario")

def cancel_appointment(appointment_id):
    with conn.cursor() as cur:
        cur.execute("UPDATE citas SET estado = 'cancelada' WHERE id = %s", (appointment_id,))
        conn.commit()
        st.success("Cita cancelada exitosamente")
        st.rerun()
