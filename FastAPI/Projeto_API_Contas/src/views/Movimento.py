from pydantic import BaseModel
from datetime import datetime

class MovimentoOut(BaseModel):
    id:int|None=None
    conta_numero:str|None=None
    valor:float|None=None
    data:datetime|None=None   

class MovimentoExtrato(BaseModel):
    id:int|None=None
    tipo:str|None=None
    valor:float|None=None
    data:datetime|None=None   
 