from pydantic import BaseModel
from typing import Optional

class AeroportoBase(BaseModel):
    nome: str
    estado: str
    cidade: str
    pais: str
    latitude: float
    longitude: float
    codigo_iata: Optional[str]
    codigo_icao: Optional[str]


