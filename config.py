import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import hashlib
import os
from datetime import datetime, timedelta
import json

# Configuración de la base de datos con fallback a variables de entorno
@st.cache_resource
def init_connection():
    # Intentar obtener configuración de secrets, con fallback a variables de entorno
    try:
        db_config = {
            "host": st.secrets["DB_HOST"],
            "database": st.secrets["DB_NAME"],
            "user": st.secrets["DB_USER"],
            "password": st.secrets["DB_PASSWORD"],
            "port": st.secrets["DB_PORT"]
        }
    except KeyError:
        # Fallback a variables de entorno para Docker
        db_config = {
            "host": os.getenv("DB_HOST", "db"),
            "database": os.getenv("DB_NAME", "citas_medicas"),
            "user": os.getenv("DB_USER", "admin"),
            "password": os.getenv("DB_PASSWORD", "admin123"),
            "port": int(os.getenv("DB_PORT", "5432"))
        }

    return psycopg2.connect(
        host=db_config["host"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"],
        port=db_config["port"],
        cursor_factory=RealDictCursor
    )

# Conexión lazy para evitar problemas con Streamlit
_conn = None

def get_conn():
    global _conn
    if _conn is None:
        _conn = init_connection()
    return _conn

# Funciones de utilidad
def hash_password(password):
    return password

def get_user_role():
    return st.session_state.get('user_role', None)

def is_logged_in():
    return 'user_id' in st.session_state

def redirect_to_login():
    st.session_state.clear()
    st.rerun()
