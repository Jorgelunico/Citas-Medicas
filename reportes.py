import streamlit as st
from config import get_conn
import pandas as pd
import plotly.express as px

conn = get_conn()

def show_reports():
    st.title("Reportes y Análisis")
    
    tab1, tab2 = st.tabs(["Reportes Básicos", "Exportar Datos"])
    
    with tab1:
        st.subheader("Reportes Básicos")
        
        # Selector de rango de fechas
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Fecha de inicio")
        with col2:
            fecha_fin = st.date_input("Fecha de fin")
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                st.error("La fecha de inicio debe ser anterior a la fecha de fin")
            else:
                # Reporte de citas por médico
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT m.id, pr.nombre, pr.apellido, COUNT(c.id) as cantidad_citas
                        FROM medicos m
                        JOIN perfiles pr ON m.perfil_id = pr.id
                        LEFT JOIN citas c ON m.id = c.medico_id 
                        AND c.fecha_hora BETWEEN %s AND %s
                        GROUP BY m.id, pr.nombre, pr.apellido
                        ORDER BY cantidad_citas DESC
                    """, (fecha_inicio, fecha_fin))
                    
                    citas_medico = cur.fetchall()
                    df_citas_medico = pd.DataFrame(citas_medico)
                    
                    if not df_citas_medico.empty:
                        fig = px.bar(df_citas_medico, x='nombre', y='cantidad_citas', 
                                    title="Citas por Médico", labels={'nombre': 'Médico', 'cantidad_citas': 'Número de Citas'})
                        st.plotly_chart(fig)
    
    # with tab2:
    #     st.subheader("Análisis Avanzados con Google Colab")
    #     st.info("""
    #     Para análisis avanzados con machine learning, puedes utilizar nuestro notebook de Google Colab
    #     que se conecta directamente a la base de datos para realizar análisis predictivos.
    #     """)
        
    #     st.write("""
    #     **Análisis disponibles:**
    #     - Predicción de demanda de citas por temporada
    #     - Detección de patrones en enfermedades comunes
    #     - Optimización de horarios médicos
    #     - Análisis de eficiencia del consultorio
    #     """)
        
    #     if st.button("Abrir Notebook de Análisis en Google Colab"):
    #         # Aquí iría la URL del notebook de Colab
    #         st.write("https://colab.research.google.com/drive/1kkQGnjOV4O_syzcdYNkU9zlnRP1eepKp?authuser=0")
    
    with tab2:
        st.subheader("Exportar Datos para Análisis")
        
        export_options = st.multiselect("Selecciona los datos a exportar",
                                      ["Pacientes", "Citas", "Historial Médico", "Signos Vitales"])
        
        if st.button("Generar Archivo CSV"):
            if export_options:
                dfs = {}
                
                with conn.cursor() as cur:
                    if "Pacientes" in export_options:
                        cur.execute("""
                            SELECT p.*, pr.*, u.email
                            FROM pacientes p
                            JOIN perfiles pr ON p.perfil_id = pr.id
                            JOIN usuarios u ON p.usuario_id = u.id
                        """)
                        pacientes = cur.fetchall()
                        dfs['pacientes'] = pd.DataFrame(pacientes)
                    
                    if "Citas" in export_options:
                        cur.execute("""
                            SELECT c.*, 
                                   pp.nombre as paciente_nombre, pp.apellido as paciente_apellido,
                                   pm.nombre as medico_nombre, pm.apellido as medico_apellido
                            FROM citas c
                            JOIN pacientes p ON c.paciente_id = p.id
                            JOIN perfiles pp ON p.perfil_id = pp.id
                            JOIN medicos m ON c.medico_id = m.id
                            JOIN perfiles pm ON m.perfil_id = pm.id
                        """)
                        citas = cur.fetchall()
                        dfs['citas'] = pd.DataFrame(citas)
                
                # Crear archivo ZIP con los DataFrames
                import zipfile
                from io import BytesIO
                
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for name, df in dfs.items():
                        csv_buffer = BytesIO()
                        df.to_csv(csv_buffer, index=False, encoding='utf-8')
                        zip_file.writestr(f"{name}.csv", csv_buffer.getvalue())
                
                zip_buffer.seek(0)
                st.download_button("Descargar Datos", zip_buffer.getvalue(), 
                                  file_name="datos_consultorio.zip", 
                                  mime="application/zip")
            else:
                st.warning("Selecciona al menos un tipo de dato para exportar")
