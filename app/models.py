"""
models.py — PDC Lab
======================
Modelo de datos de la app pública de intake del PDC App Framework.

Una sola tabla: cada fila es una solicitud de un futuro PDC App Developer,
capturada ANTES de que tenga cualquier herramienta instalada — por eso
esta app vive públicamente accesible por navegador, sin login.

Vive en su propio schema aislado (pdc_app_pdc_lab) — pdc-lab NO es una
excepción como PDC Registry, sigue la regla estándar del framework
(SPEC §4.4). El puente hacia PDC Registry es el correo (ticket), no
una lectura cruzada de schema — ver notas de sesión.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime

from app.database import Base


class Solicitud(Base):
    __tablename__ = "solicitud"

    id = Column(Integer, primary_key=True)

    # Identidad — también pre-llena los tags de AWS que usará IT después
    nombre_completo = Column(String(255), nullable=False)
    correo_corporativo = Column(String(255), nullable=False)
    empresa = Column(String(100))          # Grupo PDC / PDC Brands / Vikingo / Nexo
    division_area = Column(String(255))
    pais = Column(String(100))

    # Diagnóstico técnico — determina qué instructivo recibe y si falta algo
    sistema_operativo = Column(String(50))     # Windows / macOS / Linux
    laptop_gestionada_it = Column(Boolean, default=True)
    tiene_vscode = Column(String(10))          # Sí / No / No sé
    tiene_git = Column(String(10))
    tiene_python = Column(String(10))

    # Canvas de PDC Lab (SPEC §3)
    nombre_app_propuesto = Column(String(255))     # lowercase-sin-espacios
    descripcion_problema = Column(Text)

    # Workflow — seguimiento interno simple de pdc-lab (no reemplaza PDC Registry)
    estado = Column(String(50), default="Pendiente")  # Pendiente/Revisada/Aprobada/Rechazada
    fecha_solicitud = Column(DateTime, default=datetime.utcnow, nullable=False)
    notas_it = Column(Text)
