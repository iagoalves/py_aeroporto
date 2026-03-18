from pydantic import BaseModel
from typing import Optional

class ReservaBase(BaseModel):
    id: int
    voo_id: int
    localizador: Optional[str]
    numero_eticket: Optional[str]
    cliente_id: int
    status_pagamento: str

    class Config:
        from_attributes = True


class ReservaCreate(BaseModel):
    voo_id: int
