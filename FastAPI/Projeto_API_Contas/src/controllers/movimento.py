from fastapi import APIRouter, Depends, Response, status
from schemas.movimento import MovimentoIn
from views.Movimento import MovimentoOut, MovimentoExtrato
import exceptions as ex 
from services.service import ContaService, MovimentoService
from security import login_required

#router = APIRouter(prefix="/conta", dependencies=[Depends(login_required)] )
router = APIRouter(prefix="/conta" )
contaserv:ContaService = ContaService()
service = MovimentoService(contaserv)

@router.get("/extrato", response_model=list[MovimentoExtrato])
async def ler_movimentos(conta_numero:str):
    return await service.read_all(conta_numero)

@router.post("/saque", status_code=status.HTTP_201_CREATED, response_model=MovimentoOut)
async def registrar_saque (movimento: MovimentoIn):

    print ("movimento info.", movimento)
    tipo = "SAQUE"    
    if movimento.valor > 0:
        last_id = await service.create(movimento, tipo)
        return {**movimento.model_dump(), "id":last_id}
    else:
        raise ex.ValorMovimentoInvalidoError(tipo_movimento=tipo,
                                             valor=movimento.valor)
    
@router.post("/deposito", status_code=status.HTTP_201_CREATED, response_model=MovimentoOut)
async def registrar_deposito (movimento: MovimentoIn):
    tipo = "DEPOSITO"
    if movimento.valor > 0:
        last_id = await service.create(movimento, tipo)
        return {**movimento.model_dump(), "id":last_id}
    else:
        raise ex.ValorMovimentoInvalidoError(tipo_movimento=tipo,
                                             valor=movimento.valor)

@router.delete("/estorno/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_movimento (id:int):
    return await service.delete(id)
