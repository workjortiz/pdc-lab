"""initial

Revision ID: 0001
Revises:
Create Date: 2026-09-02

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "solicitud",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre_completo", sa.String(length=255), nullable=False),
        sa.Column("correo_corporativo", sa.String(length=255), nullable=False),
        sa.Column("empresa", sa.String(length=100)),
        sa.Column("division_area", sa.String(length=255)),
        sa.Column("pais", sa.String(length=100)),
        sa.Column("sistema_operativo", sa.String(length=50)),
        sa.Column("laptop_gestionada_it", sa.Boolean()),
        sa.Column("tiene_vscode", sa.String(length=10)),
        sa.Column("tiene_git", sa.String(length=10)),
        sa.Column("tiene_python", sa.String(length=10)),
        sa.Column("nombre_app_propuesto", sa.String(length=255)),
        sa.Column("descripcion_problema", sa.Text()),
        sa.Column("estado", sa.String(length=50)),
        sa.Column("fecha_solicitud", sa.DateTime(), nullable=False),
        sa.Column("notas_it", sa.Text()),
    )


def downgrade():
    op.drop_table("solicitud")
