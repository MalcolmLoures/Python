import databases
import sqlalchemy as sa

DATABASE_URL = "sqlite:///./contas.db"

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()
engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread":False})

