from datetime import datetime, UTC
from pydantic import BaseModel

class MovimentoIn(BaseModel):
    conta_numero:str|None=None
    valor:float|None=None
    data:datetime|None=None
