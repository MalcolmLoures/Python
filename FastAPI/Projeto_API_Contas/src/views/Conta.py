from pydantic import BaseModel

class ContaOut(BaseModel):
    id:int
    numero:str
    titular:str
    saldo:float   
 