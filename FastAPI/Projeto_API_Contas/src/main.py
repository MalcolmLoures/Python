from contextlib import asynccontextmanager
import sqlalchemy as sa
from controllers import conta, auth, movimento
from fastapi import FastAPI
import databases
from database import database, metadata, engine

@asynccontextmanager
async def lifespan(app: FastAPI):

    from models import conta, movimento #noqa
    await database.connect()
    metadata.create_all(engine)

    yield
    await database.disconnect()

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(conta.router)
app.include_router(movimento.router)