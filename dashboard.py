import streamlit as st
from config import get_conn
import pandas as pd
import plotly.express as px
conn = get_conn()

def show_dashboard():
    st.title("Dashboard de Gestión Médica")
    
    # Obtener estadísticas según el rol del usuario
    user_role = st.session_state.user_role
    
    if user_role in ['admin', 'medico', 'recepcionista']:
        show_admin_dashboard()
    else:
        show_patient_dashboard()

def show_admin_dashboard():
    col1, col2, col3 = st.columns(3)
    
    with conn.cursor() as cur:
        # Total de pacientes
        cur.execute("SELECT COUNT(*) as total FROM pacientes")
        total_pacientes = cur.fetchone()['total']
        
        # Citas hoy
        cur.execute("SELECT COUNT(*) as total FROM citas WHERE DATE(fecha_hora) = CURRENT_DATE")
        citas_hoy = cur.fetchone()['total']
        
        # Citas esta semana
        cur.execute("""
            SELECT COUNT(*) as total 
            FROM citas 
            WHERE fecha_hora BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
        """)
        citas_semana = cur.fetchone()['total']
        
        # Ingresos del mes (ejemplo simplificado)
        cur.execute("""
            SELECT COUNT(*) * 50 as estimado  -- Valor假设 de consulta
            FROM citas 
            WHERE estado = 'completada' 
            AND fecha_hora >= DATE_TRUNC('month', CURRENT_DATE)
        """)
        ingresos_mes = cur.fetchone()['estimado']
    
    with col1:
        st.metric("Total Pacientes", total_pacientes)
    with col2:
        st.metric("Citas Hoy", citas_hoy)
    with col3:
        st.metric("Citas Esta Semana", citas_semana)
    # with col4:
    #     st.metric("Ingresos del Mes", f"${ingresos_mes:,.2f}")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with conn.cursor() as cur:  # Crear un cursor regular temporal
        cur.execute("""
            SELECT estado, COUNT(*) as cantidad 
            FROM citas 
            GROUP BY estado
        """)
        data_estados = cur.fetchall()
        df_estados = pd.DataFrame(data_estados, columns=['estado', 'cantidad'])
        
        if not df_estados.empty:
            fig = px.pie(df_estados, values='cantidad', names='estado', 
                         title="Distribución de Citas por Estado")
            st.plotly_chart(fig)
    
    with conn.cursor() as cur:  # Crear otro cursor regular
        cur.execute("""
            SELECT DATE_TRUNC('month', fecha_hora) as mes, COUNT(*) as cantidad
            FROM citas 
            GROUP BY mes 
            ORDER BY mes
        """)
        data_mensual = cur.fetchall()
        df_mensual = pd.DataFrame(data_mensual, columns=['mes', 'cantidad'])
        
        if not df_mensual.empty:
            df_mensual['mes'] = pd.to_datetime(df_mensual['mes'])
            fig = px.line(df_mensual, x='mes', y='cantidad', 
                          title="Evolución de Citas por Mes")
            st.plotly_chart(fig)

def show_patient_dashboard():
    with conn.cursor() as cur:
        # Obtener información del paciente
        cur.execute("""
            SELECT p.*, pr.*,u.* FROM pacientes p 
            JOIN perfiles pr ON p.perfil_id = pr.id  
            JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.usuario_id = %s
        """, (st.session_state.user_id,))
        paciente = cur.fetchone()
        
        if paciente:
            st.header(f"Bienvenido/a, {paciente['nombre']} {paciente['apellido']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Tu Información")
                print(paciente)
                st.write(f"**Email:** {paciente['email']}")
                st.write(f"**Teléfono:** {paciente['telefono']}")
                st.write(f"**Fecha de Nacimiento:** {paciente['fecha_nacimiento']}")
                st.write(f"**Tipo de Sangre:** {paciente['tipo_sangre'] or 'No especificado'}")
            
            with col2:
                st.subheader("Próximas Citas")
                cur.execute("""
                    SELECT c.*, pr.nombre as medico_nombre, pr.apellido as medico_apellido
                    FROM citas c
                    JOIN medicos m ON c.medico_id = m.id
                    JOIN perfiles pr ON m.perfil_id = pr.id
                    WHERE c.paciente_id = %s AND c.fecha_hora > NOW() AND c.estado IN ('programada', 'confirmada')
                    ORDER BY c.fecha_hora ASC
                    LIMIT 3
                """, (paciente['id'],))
                
                proximas_citas = cur.fetchall()
                
                if proximas_citas:
                    for cita in proximas_citas:
                        st.write(f"**{cita['fecha_hora'].strftime('%d/%m/%Y %H:%M')}**")
                        st.write(f"Dr. {cita['medico_nombre']} {cita['medico_apellido']}")
                        st.write(f"Estado: {cita['estado'].capitalize()}")
                        st.divider()
                else:
                    st.info("No tienes citas programadas")
            
            # Mostrar recordatorios de salud según condiciones crónicas
            if paciente['condiciones_cronicas']:
                st.subheader("Recordatorios de Salud")
                st.warning(f"Recuerda seguir tu tratamiento para: {paciente['condiciones_cronicas']}")
