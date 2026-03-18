from pydantic import BaseModel
from datetime import datetime

class VooBase(BaseModel):
    voo_id: int
    partida_prevista: datetime
    origem_nome: str 
    destino_nome: str  
    companhia_nome: str  
    custo_km: float 
    capacidade: int  