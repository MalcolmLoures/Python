import sqlalchemy as sa
from database import metadata

movimentos = sa.Table('movimentos', metadata, 
                sa.Column("id", sa.Integer, primary_key=True ),
                sa.Column('conta_id', sa.Integer, sa.ForeignKey('contas.id')),
                sa.Column("tipo", sa.String(20), nullable=False),
                sa.Column("data", sa.DateTime, nullable=False),
                sa.Column("valor", sa.Float, nullable=False),
                )