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
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st

_ROOT_DIR = Path(__file__).resolve().parent.parent
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

from app.auth import require_login
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


def construir_registro_json(nombre_completo, nombre_app_propuesto, descripcion_problema, division_area, pais, correo_corporativo, codigo_colaborador=""):
    """Mapea los campos de una solicitud al formato que espera el importador de PDC Registry."""
    return {
        "nombre": (nombre_app_propuesto or "").strip().lower().replace(" ", "-"),
        "nombre_display": (nombre_app_propuesto or "").strip().title(),
        "descripcion": descripcion_problema or "",
        "area_pais": f"{division_area or ''} / {pais or ''}".strip(" /"),
        "owner_email": correo_corporativo or "",
        "estado": "En desarrollo",
        "ambiente": "BETA",
        "codigo_colaborador": codigo_colaborador or "",
        "nombre_colaborador": nombre_completo or "",
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

# ══════════════════════════════════════════════════════════════════════
# FORMULARIO PÚBLICO
# ══════════════════════════════════════════════════════════════════════
# ── Pantalla 2: cierre del proceso — reemplaza al formulario, no convive con él ──
if st.session_state.get("formulario_completado"):
    st.markdown("## ✅ Formulario Concluido")
    st.success(
        "¡Listo! Tu solicitud fue enviada. Integraciones Digitales se pondrá en "
        "contacto contigo con los siguientes pasos."
    )
    if st.session_state.get("ultima_solicitud_json"):
        st.download_button(
            "📤 Descargar JSON para PDC Registry",
            data=st.session_state.ultima_solicitud_json,
            file_name=st.session_state.get("ultima_solicitud_filename", "solicitud-registro.json"),
            mime="application/json",
            key="descarga_solicitud",
        )
    else:
        st.warning(
            "Tu solicitud quedó guardada correctamente, pero no se pudo generar el "
            "JSON de descarga. Avisa a Integraciones Digitales para que lo generen manualmente."
        )
    if st.button("📝 Registrar otra idea"):
        st.session_state.formulario_completado = False
        st.session_state.pop("ultima_solicitud_json", None)
        st.session_state.pop("ultima_solicitud_filename", None)
        st.session_state.pop("nombre_completo_input", None)
        st.session_state.pop("correo_corporativo_input", None)
        st.session_state.pop("division_area_input", None)
        st.rerun()

# ── Pantalla 1: el formulario ──
else:
    st.write(
        "¿Tienes una idea para automatizar algo en tu área con ayuda de Claude? "
        "Cuéntanos y te contactamos con los siguientes pasos."
    )

    # Estos 3 campos van FUERA del st.form: Streamlit no reacciona en vivo a
    # cambios dentro de un form (solo al enviar) — para que la mayúscula se
    # vea al tabular, el widget necesita un on_change fuera del form.
    def _forzar_mayusculas(key):
        if key in st.session_state and st.session_state[key]:
            st.session_state[key] = st.session_state[key].upper()

    st.markdown("### Sobre ti")
    c1, c2 = st.columns(2)
    c1.text_input(
        "Nombre completo *", key="nombre_completo_input",
        on_change=_forzar_mayusculas, args=("nombre_completo_input",),
    )
    c2.text_input(
        "Correo corporativo *", key="correo_corporativo_input",
        on_change=_forzar_mayusculas, args=("correo_corporativo_input",),
    )
    c3, c4 = st.columns(2)
    c3.selectbox("Empresa / mundo", ["NEXO", "VIKINGO DISTRIBUIDORA", "PDC BRANDS", "MOSTRO"], key="empresa_input")
    c4.text_input(
        "División / Área", key="division_area_input",
        on_change=_forzar_mayusculas, args=("division_area_input",),
    )

    with st.form("solicitud_lab", clear_on_submit=True):
        c_pais, c_codigo = st.columns(2)
        pais = c_pais.selectbox("País", ["GT", "SV", "HN", "NI", "PN", "RD"])
        codigo_colaborador_num = c_codigo.number_input(
            "Código colaborador (RRHH) *", min_value=0, step=1, value=None, format="%d"
        )

        st.markdown("### Tu equipo")
        c5, c6 = st.columns(2)
        sistema_operativo = c5.selectbox("Sistema operativo de tu laptop *", ["Windows", "macOS", "Linux"])
        laptop_gestionada_it = c6.selectbox("¿Laptop gestionada por IT (corporativa)?", ["Sí", "No"]) == "Sí"
        c7, c8, c9 = st.columns(3)
        tiene_vscode = c7.selectbox("¿Tienes VS Code?", ["Sí", "No", "No sé"])
        tiene_git = c8.selectbox("¿Tienes un Gestor Git?", ["Sí", "No", "No sé"])
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
            nombre_completo = st.session_state.get("nombre_completo_input", "") or ""
            correo_corporativo = st.session_state.get("correo_corporativo_input", "") or ""
            division_area = st.session_state.get("division_area_input", "") or ""
            empresa = st.session_state.get("empresa_input", "")
            codigo_colaborador = str(int(codigo_colaborador_num)) if codigo_colaborador_num is not None else ""

            faltantes = []
            if not nombre_completo:
                faltantes.append("Nombre completo")
            if not correo_corporativo:
                faltantes.append("Correo corporativo")
            if not descripcion_problema:
                faltantes.append("Descripción del problema")
            if not codigo_colaborador:
                faltantes.append("Código colaborador")

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
                    # sin pasar por ninguna vista de IT. Si algo aquí falla, el registro
                    # en BD ya quedó guardado arriba — no debe tumbar toda la pantalla.
                    try:
                        registro_json = construir_registro_json(
                            nombre_completo, nombre_app_propuesto, descripcion_problema, division_area, pais, correo_corporativo, codigo_colaborador
                        )
                        st.session_state.ultima_solicitud_json = json.dumps(registro_json, ensure_ascii=False, indent=2)
                        st.session_state.ultima_solicitud_filename = construir_nombre_archivo(
                            nombre_completo, registro_json["nombre"]
                        )
                    except Exception:
                        st.session_state.ultima_solicitud_json = None
                        st.session_state.ultima_solicitud_filename = None

                    st.session_state.formulario_completado = True
                    st.rerun()
                finally:
                    session.close()

