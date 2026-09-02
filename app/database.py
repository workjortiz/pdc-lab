"""
database.py — PDC App Framework
==============================
Conexión agnóstica a base de datos. NO MODIFICAR — mantenido por el framework.

DB_MODE=sqlite (default, desarrollo local) → archivo en ./data/app.db
DB_MODE=postgresql (producción) → usa DATABASE_URL del .env / del pipeline

El mismo código y los mismos modelos (app/models.py) funcionan sin cambios
en ambos motores — por eso la regla del framework de "SQLAlchemy ORM
obligatorio, nunca SQL crudo".
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

Base = declarative_base()

DB_MODE = os.getenv("DB_MODE", "sqlite")

if DB_MODE == "sqlite":
    _data_dir = Path(__file__).resolve().parent.parent / "data"
    _data_dir.mkdir(exist_ok=True)
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{_data_dir}/app.db")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    """Nueva sesión por request/acción. El caller es responsable de cerrarla."""
    return SessionLocal()


def init_db():
    """Crea las tablas si no existen. Uso previsto: solo desarrollo local.
    En producción, el schema se gestiona vía Alembic (PDC Deploy)."""
    Base.metadata.create_all(bind=engine)
