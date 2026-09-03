"""
main.py — PDC Lab
====================
App pública de intake del PDC App Framework. Sin login — cualquier
futuro PDC App Developer llena este formulario desde su navegador,
sin necesidad de tener nada instalado todavía.

Aquí SÍ puedes modificar libremente. Aquí NO debes tocar auth.py/database.py.
"""

import json
import os
import sys
from pathlib import Path

import requests
import streamlit as st

_ROOT_DIR = Path(__file__).resolve().parent.parent
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from app.auth import require_login, require_it_access
from app.database import get_session
from app.models import Solicitud

NAVY = "#00216F"
NARANJA = "#FF5100"
GRIS = "#606060"

CONFIG = json.loads(Path(__file__).resolve().parent.parent.joinpath("pdc.config.json").read_text())

st.set_page_config(page_title=CONFIG.get("app_name_display", "PDC Lab"), page_icon="💡", layout="centered")

st.markdown(
    f"""
    <style>
    .pdc-header {{ border-bottom: 4px solid {NARANJA}; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }}
    .pdc-header h1 {{ color: {NAVY}; font-weight: 800; margin-bottom: 0; }}
    .badge {{ display:inline-block; padding:2px 10px; border-radius:12px; font-size:12px; font-weight:700; margin-right:6px; }}
    .badge-pendiente {{ background:#FFF3EC; color:{NARANJA}; }}
    .badge-revisada {{ background:#EFEBFB; color:#5B3EBF; }}
    .badge-aprobada {{ background:#E6F4EA; color:#1E7A34; }}
    .badge-rechazada {{ background:#F0F0F0; color:{GRIS}; }}
    </style>
    """,
    unsafe_allow_html=True,
)

require_login()


def construir_registro_json(nombre_app_propuesto, descripcion_problema, division_area, pais, correo_corporativo, codigo_colaborador=""):
    """Mapea los campos de una solicitud al formato que espera el importador de PDC Registry."""
    return {
        "nombre": (nombre_app_propuesto or "").strip().lower().replace(" ", "-"),
        "nombre_display": (nombre_app_propuesto or "").strip().title(),
        "descripcion": descripcion_problema or "",
        "area_pais": f"{division_area or ''} / {pais or ''}".strip(" /"),
        "owner_email": correo_corporativo or "",
        "usuarios_adicionales": "",
        "estado": "En desarrollo",
        "ambiente": "BETA",
        "github_repo_url": "",
        "url_produccion": "",
        "codigo_colaborador": codigo_colaborador or "",
    }


def construir_nombre_archivo(nombre_completo, nombre_app):
    """Registro_{fecha}_{AUTOR}_{APP}.json — ej. Registro_20260902_JUANORTIZ_PDCLAB.json"""
    fecha_str = datetime.utcnow().strftime("%Y%m%d")
    autor = (nombre_completo or "SINAUTOR").upper().replace(" ", "")
    app_slug = (nombre_app or "APP").upper().replace("-", "").replace(" ", "")
    return f"Registro_{fecha_str}_{autor}_{app_slug}.json"

st.markdown('<div class="pdc-header"><h1>PDC Lab</h1></div>', unsafe_allow_html=True)
st.caption("Punto de entrada al PDC App Framework — Grupo PDC · Integraciones Digitales")
st.caption(f"v{CONFIG.get('version', '0.0.0')}")

modo = st.radio("​", ["📝 Registrar una idea", "🔐 Acceso IT"], horizontal=True, label_visibility="collapsed")

# ══════════════════════════════════════════════════════════════════════
# FORMULARIO PÚBLICO
# ══════════════════════════════════════════════════════════════════════
if modo == "📝 Registrar una idea":
    # ── Pantalla 2: cierre del proceso — reemplaza al formulario, no convive con él ──
    if st.session_state.get("formulario_completado"):
        st.markdown("## ✅ Formulario Concluido")
        st.success(
            "¡Listo! Tu solicitud fue enviada. Integraciones Digitales se pondrá en "
            "contacto contigo con los siguientes pasos."
        )
        st.download_button(
            "📤 Descargar JSON para PDC Registry",
            data=st.session_state.ultima_solicitud_json,
            file_name=st.session_state.get("ultima_solicitud_filename", "solicitud-registro.json"),
            mime="application/json",
            key="descarga_solicitud",
        )
        if st.button("📝 Registrar otra idea"):
            st.session_state.formulario_completado = False
            st.session_state.pop("ultima_solicitud_json", None)
            st.session_state.pop("ultima_solicitud_filename", None)
            st.rerun()

    # ── Pantalla 1: el formulario ──
    else:
        st.write(
            "¿Tienes una idea para automatizar algo en tu área con ayuda de Claude? "
            "Cuéntanos y te contactamos con los siguientes pasos."
        )

        with st.form("solicitud_lab", clear_on_submit=True):
            st.markdown("### Sobre ti")
            c1, c2 = st.columns(2)
            nombre_completo = c1.text_input("Nombre completo *")
            correo_corporativo = c2.text_input("Correo corporativo *")
            c3, c4 = st.columns(2)
            empresa = c3.selectbox("Empresa / mundo", ["NEXO", "VIKINGO DISTRIBUIDORA", "PDC BRANDS", "MOSTRO"])
            division_area = c4.text_input("División / Área")
            c_pais, c_codigo = st.columns(2)
            pais = c_pais.selectbox("País", ["GT", "SV", "HN", "NI", "PN", "RD"])
            codigo_colaborador = c_codigo.text_input(
                "¿Ya tienes código colaborador? (RRHH)", placeholder="opcional"
            )

            st.markdown("### Tu equipo")
            c5, c6 = st.columns(2)
            sistema_operativo = c5.selectbox("Sistema operativo de tu laptop *", ["Windows", "macOS", "Linux"])
            laptop_gestionada_it = c6.selectbox("¿Laptop gestionada por IT (corporativa)?", ["Sí", "No"]) == "Sí"
            c7, c8, c9 = st.columns(3)
            tiene_vscode = c7.selectbox("¿Tienes VS Code?", ["Sí", "No", "No sé"])
            tiene_git = c8.selectbox("¿Tienes Git?", ["Sí", "No", "No sé"])
            tiene_python = c9.selectbox("¿Tienes Python 3.11?", ["Sí", "No", "No sé"])

            st.markdown("### Tu idea")
            nombre_app_propuesto = st.text_input(
                "Nombre propuesto para tu app (lowercase-sin-espacios)",
                placeholder="control-rutas-hn",
            )
            descripcion_problema = st.text_area(
                "¿Qué problema quieres resolver? *",
                placeholder="Describe el problema, quiénes lo viven, y qué datos necesitarías capturar.",
                height=140,
            )

            enviado = st.form_submit_button("Solicitar Registro", type="primary", use_container_width=True)

            if enviado:
                nombre_completo = (nombre_completo or "").upper()

                faltantes = []
                if not nombre_completo:
                    faltantes.append("Nombre completo")
                if not correo_corporativo:
                    faltantes.append("Correo corporativo")
                if not descripcion_problema:
                    faltantes.append("Descripción del problema")

                if faltantes:
                    st.error(f"Completa los campos obligatorios: {', '.join(faltantes)}")
                else:
                    session = get_session()
                    try:
                        nueva = Solicitud(
                            nombre_completo=nombre_completo,
                            correo_corporativo=correo_corporativo,
                            empresa=empresa,
                            division_area=division_area,
                            pais=pais,
                            codigo_colaborador=codigo_colaborador,
                            sistema_operativo=sistema_operativo,
                            laptop_gestionada_it=laptop_gestionada_it,
                            tiene_vscode=tiene_vscode,
                            tiene_git=tiene_git,
                            tiene_python=tiene_python,
                            nombre_app_propuesto=nombre_app_propuesto,
                            descripcion_problema=descripcion_problema,
                        )
                        session.add(nueva)
                        session.commit()

                        # Notificación tipo ticket vía Power Automate — mismo patrón
                        # que las notificaciones de Teams en el pipeline PDC Deploy.
                        webhook_url = os.getenv("POWER_AUTOMATE_WEBHOOK_URL", "")
                        if webhook_url:
                            try:
                                requests.post(
                                    webhook_url,
                                    json={
                                        "titulo": f"Nueva solicitud PDC Lab — {nombre_app_propuesto or 'sin nombre'}",
                                        "solicitante": f"{nombre_completo} ({correo_corporativo})",
                                        "empresa_division": f"{empresa} / {division_area}",
                                        "pais": pais,
                                        "sistema_operativo": sistema_operativo,
                                        "herramientas_faltantes": ", ".join(
                                            [
                                                t for t, v in [
                                                    ("VS Code", tiene_vscode),
                                                    ("Git", tiene_git),
                                                    ("Python 3.11", tiene_python),
                                                ] if v != "Sí"
                                            ]
                                        ) or "Ninguna — todo listo",
                                        "descripcion": descripcion_problema,
                                    },
                                    timeout=5,
                                )
                            except requests.RequestException:
                                pass  # el registro en BD ya quedó guardado; el correo es best-effort

                        # JSON listo para importar en PDC Registry — se genera al instante,
                        # sin pasar por ninguna vista de IT.
                        registro_json = construir_registro_json(
                            nombre_app_propuesto, descripcion_problema, division_area, pais, correo_corporativo, codigo_colaborador
                        )
                        st.session_state.ultima_solicitud_json = json.dumps(registro_json, ensure_ascii=False, indent=2)
                        st.session_state.ultima_solicitud_filename = construir_nombre_archivo(
                            nombre_completo, registro_json["nombre"]
                        )
                        st.session_state.formulario_completado = True
                        st.rerun()
                    finally:
                        session.close()

# ══════════════════════════════════════════════════════════════════════
# VISTA DE IT — cola de solicitudes (gate simple, no AD todavía)
# ══════════════════════════════════════════════════════════════════════
else:
    if require_it_access():
        st.markdown("### Cola de solicitudes")

        session = get_session()
        try:
            solicitudes = session.query(Solicitud).order_by(Solicitud.fecha_solicitud.desc()).all()
        finally:
            session.close()

        if not solicitudes:
            st.info("No hay solicitudes todavía.")
        else:
            badge_map = {
                "Pendiente": "badge-pendiente",
                "Revisada": "badge-revisada",
                "Aprobada": "badge-aprobada",
                "Rechazada": "badge-rechazada",
            }
            for s in solicitudes:
                with st.expander(
                    f"{s.fecha_solicitud.strftime('%Y-%m-%d %H:%M')} — {s.nombre_app_propuesto or 'sin nombre'} · {s.nombre_completo}"
                ):
                    st.markdown(
                        f'<span class="badge {badge_map.get(s.estado, "badge-pendiente")}">{s.estado}</span>',
                        unsafe_allow_html=True,
                    )
                    st.write(f"**Correo:** {s.correo_corporativo}")
                    st.write(f"**Empresa / División:** {s.empresa} / {s.division_area} · {s.pais}")
                    st.write(
                        f"**Equipo:** {s.sistema_operativo} · "
                        f"{'Gestionada por IT' if s.laptop_gestionada_it else 'Laptop personal'} · "
                        f"VS Code: {s.tiene_vscode} · Git: {s.tiene_git} · Python: {s.tiene_python}"
                    )
                    st.write(f"**Problema descrito:** {s.descripcion_problema}")

                    export_payload = construir_registro_json(
                        s.nombre_app_propuesto, s.descripcion_problema, s.division_area, s.pais, s.correo_corporativo, s.codigo_colaborador
                    )
                    st.download_button(
                        "📤 Exportar como JSON (para PDC Registry)",
                        data=json.dumps(export_payload, ensure_ascii=False, indent=2),
                        file_name=construir_nombre_archivo(s.nombre_completo, export_payload["nombre"]),
                        mime="application/json",
                        key=f"export_{s.id}",
                    )

                    session = get_session()
                    try:
                        s_edit = session.get(Solicitud, s.id)
                        nuevo_estado = st.selectbox(
                            "Estado",
                            ["Pendiente", "Revisada", "Aprobada", "Rechazada"],
                            index=["Pendiente", "Revisada", "Aprobada", "Rechazada"].index(s_edit.estado),
                            key=f"estado_{s.id}",
                        )
                        notas = st.text_area("Notas de IT", value=s_edit.notas_it or "", key=f"notas_{s.id}")
                        if st.button("Guardar", key=f"guardar_{s.id}"):
                            s_edit.estado = nuevo_estado
                            s_edit.notas_it = notas
                            session.commit()
                            st.success("Actualizado.")
                            st.rerun()
                    finally:
                        session.close()
