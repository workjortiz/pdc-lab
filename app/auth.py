"""
auth.py — PDC App Framework (pdc-lab)
========================================
pdc-lab es PÚBLICA — no requiere login para el formulario de solicitud.
NO MODIFICAR el patrón general del framework, pero aquí require_login()
es intencionalmente un no-op: cualquier persona con el link puede
llenar el formulario, ese es el punto de esta app.

La vista de IT (cola de solicitudes) usa un gate simple por clave
compartida (ADMIN_ACCESS_CODE en .env) — mock temporal hasta integrar AD.
"""

import os

import streamlit as st

_MOCK_USER = {"name": "Visitante", "email": "publico@grupopdc.com"}


def require_login():
    """No-op intencional — pdc-lab es de acceso público."""
    if "user" not in st.session_state:
        st.session_state.user = _MOCK_USER


def current_user():
    return st.session_state.user


def logout():
    st.session_state.pop("user", None)
    st.session_state.pop("it_autenticado", None)
    st.rerun()


def require_it_access():
    """Gate simple para la vista de IT — clave compartida, no AD todavía."""
    if st.session_state.get("it_autenticado"):
        return True

    clave = st.text_input("Clave de acceso IT", type="password")
    if clave and clave == os.getenv("ADMIN_ACCESS_CODE", ""):
        st.session_state.it_autenticado = True
        st.rerun()
    elif clave:
        st.error("Clave incorrecta.")
    return False
