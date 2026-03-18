from pydantic import BaseModel

class AeronaveBase(BaseModel):
    modelo: str
    capacidade: int
    companhia_id: int