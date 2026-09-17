from fastapi import APIRouter, Depends, Response, status
from schemas.conta import ContaIn
from views.Conta import ContaOut
from services.service import ContaService
from security import login_required

#router = APIRouter(prefix="/contas", dependencies=[Depends(login_required)] )
router = APIRouter(prefix="/contas" )

service = ContaService()

@router.get("/", response_model=list[ContaOut])
async def read_contas ():
    return await service.read_all()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ContaOut)
async def create_conta (conta: ContaIn):
    
    last_id = await service.create(conta)
    return {**conta.model_dump(), "id":last_id}
          
@router.patch("/{id}", response_model=ContaOut)
async def update_conta (id:int, conta: ContaIn):
    
    return await service.update(id, conta)
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_conta (id:int):

    return await service.delete(id)
