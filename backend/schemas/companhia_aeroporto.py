from pydantic import BaseModel

class CompanhiaAeroportoBase(BaseModel):
    companhia_id: int
    aeroporto_id: int