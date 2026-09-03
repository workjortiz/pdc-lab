"""add codigo_colaborador

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-02

"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("solicitud") as batch_op:
        batch_op.add_column(sa.Column("codigo_colaborador", sa.String(length=50)))


def downgrade():
    with op.batch_alter_table("solicitud") as batch_op:
        batch_op.drop_column("codigo_colaborador")
