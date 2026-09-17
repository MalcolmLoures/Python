from datetime import datetime, UTC
from pydantic import BaseModel

class ContaIn(BaseModel):
    numero:str|None=None
    titular:str|None=None
    saldo:float|None=None