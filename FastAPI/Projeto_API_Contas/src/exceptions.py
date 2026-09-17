from http import HTTPStatus

class MovimentoInvalidoError(Exception):
    def __init__(self, id:int, message:str = f"Movimento não encontrado", status_code: int = HTTPStatus.NOT_FOUND) -> None:
        self.message =  f"{message} - id movimento: {id}"
        self.status_code = status_code

class ContaInvalidaError(Exception):
    def __init__(self, numero_conta:str, message:str = f"Conta inválida", status_code: int = HTTPStatus.NOT_FOUND) -> None:
        self.message = f"{message} - conta: {numero_conta}"
        self.status_code = status_code

class TipoMovimentoInvalidoError(Exception):
    def __init__(self, tipo_movimento:str, message:str = f"Tipo de movimento inválido", status_code:int = HTTPStatus.INTERNAL_SERVER_ERROR) -> None:
        self.message = f"{message} - tipo: {tipo_movimento}"
        self.status_code = status_code

class ValorMovimentoInvalidoError(Exception):
    def __init__(self, valor:float, tipo_movimento:str, message:str = f"Tipo de movimento inválido", status_code:int = HTTPStatus.INTERNAL_SERVER_ERROR) -> None:
        self.message = f"{message} - tipo: {tipo_movimento} - valor informado: {valor}"
        self.status_code = status_code