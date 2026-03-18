from pydantic import BaseModel

class PassagemBase(BaseModel):
    cliente_id: int
    voo_id: int


