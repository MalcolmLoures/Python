from datetime import datetime
from databases.interfaces import Record
from database import database
from models.conta import contas
from models.movimento import movimentos
from schemas.conta import ContaIn
from schemas.movimento import MovimentoIn
import exceptions as ex

class ContaService:
    async def read_all (self) -> list[Record]:
        query = contas.select()
        return await database.fetch_all(query)

    async def create(self, conta: ContaIn) -> int:
        command = contas.insert().values(
                titular=conta.titular, 
                numero=conta.numero, 
                saldo=conta.saldo)
        
        return await database.execute(command)

    async def read(self, id:int) -> Record:
        return await self.__getByID(id)

    async def update (self, id:int, conta:ContaIn) -> Record:
        total = await self.count(id)
        if not total:
            raise Exception("errro!!!")

        data = conta.model_dump(exclude_unset=True)
        command = contas.update().where(contas.c.id==id).values(**data)
        await database.execute(command)
        return await self.__getByID(id)

    async def delete (self, id:int) ->None:
        command = contas.delete().where(contas.c.id == id)        
        await database.execute(command)

    async def count(self, id:int) -> int:
        query = "select count(id) as total from contas where id = :id"
        result = await database.fetch_one(query, {"id": id})
        return result.total

    async def __getByID(self, id:int) -> Record:
        query = contas.select().where(contas.c.id == id)
        conta = await database.fetch_one(query)

        if not conta:
            raise ex.ContaInvalidaError(numero_conta=id)

        return conta

    async def GetID(self, numero:str) -> int:
        query = "select id from contas where numero = :numero"
        result = await database.fetch_one(query, {"numero": numero})
        if not result.id:             
            raise ex.ContaInvalidaError(numero_conta=numero)
            
        return result.id
    
    async def GetFieldValue(self, id:int, fieldName:str):
        query = f"select {fieldName} as valor from contas where id = :id"
        result = await database.fetch_one(query, {"id": id})

        if not result.valor:             
            raise ex.ContaInvalidaError(numero_conta=id)
        
        return result.valor

class MovimentoService:
    def __init__(self, service:ContaService):
        self.__conta_service = service

    async def count(self, id:int) -> int:
        query = "select count(id) as total from movimentos where id = :id"
        result = await database.fetch_one(query, {"id": id})
        return result.total
    
    async def GetFieldValue(self, id:int, fieldName:str):
        query = f"select {fieldName} as valor from movimentos where id = :id"
        result = await database.fetch_one(query, {"id": id})

        if not result.valor:             
            raise ex.ContaInvalidaError(numero_conta=id)
        return result.valor
        
    async def read_all (self, conta_numero:str) -> list[Record]:
        conta_id = await self.__conta_service.GetID(numero=conta_numero)
        query = movimentos.select().where( movimentos.c.conta_id == conta_id)
        return await database.fetch_all(query)

    async def create(self, movimento: MovimentoIn, tipo:str) -> int:

        if tipo.upper() not in ("SAQUE", "DEPOSITO"):
            raise ex.TipoMovimentoInvalidoError(tipo_movimento=tipo)
        
        SINAL = 1
        movimento.data = datetime.now()
        conta_id = await self.__conta_service.GetID(numero=movimento.conta_numero)
        command = movimentos.insert().values(
                conta_id=conta_id, 
                data=movimento.data, 
                valor=movimento.valor,
                tipo=tipo)

        if tipo.upper() == "SAQUE":
            SINAL = -1

        conta = ContaIn()
        saldo:float = await self.__conta_service.GetFieldValue(conta_id, "saldo")
        conta.saldo = saldo + (movimento.valor * SINAL)
        await self.__conta_service.update(conta_id, conta)
        
        return await database.execute(command)

    async def delete (self, id:int) ->None:

        if self.count(id) == 0:
            raise ex.MovimentoInvalidoError(id=id)
        
        SINAL:int = -1
        movimento_valor:float = await self.GetFieldValue(id,"valor") 
        movimento_tipo:str = await self.GetFieldValue(id,"tipo") 
        conta_id:int = await self.GetFieldValue(id,"conta_id") 

        if movimento_tipo.upper() == "SAQUE":
            SINAL = 1

        command = movimentos.delete().where(movimentos.c.id == id) 

        conta = ContaIn()
        saldo = await self.__conta_service.GetFieldValue(conta_id, "saldo")
        conta.saldo = saldo + (movimento_valor * SINAL)

        await self.__conta_service.update(conta_id, conta)               
        await database.execute(command)