import sqlalchemy as sa
from database import metadata

contas = sa.Table('contas', metadata, 
                sa.Column("id", sa.Integer, primary_key=True ),
                sa.Column("numero", sa.String(30), nullable=False, unique=True ),
                sa.Column("titular", sa.String, nullable=False),
                sa.Column("saldo", sa.Float, nullable=False),
                )
