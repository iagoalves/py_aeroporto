from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import date, datetime

from models.database import get_db
from models.voo import Voo
from models.aeroporto import Aeroporto
from schemas.voo import VooBase
from schemas.aeroporto import AeroportoBase

router = APIRouter(tags=["Voo"])

# 1) Listar voos de uma companhia — retornando nomes de origem, destino e companhia
@router.get(
    "/companhia/{companhia_id}/voos",
    response_model=List[VooBase],
    summary="Listar voos",
)
def listar_voos(companhia_id: int, db: Session = Depends(get_db)):
    voos = (
        db.query(Voo)
          .options(
              joinedload(Voo.origem),  # Carregar dados da origem
              joinedload(Voo.destino),  # Carregar dados do destino
              joinedload(Voo.companhia),  # Carregar dados da companhia
              joinedload(Voo.aeronave)  # Carregar dados da aeronave
          )
          .filter(Voo.companhia_id == companhia_id)
          .all()
    )
    
    if not voos:
        raise HTTPException(status_code=404, detail="Nenhum voo encontrado para essa companhia.")
    
    resultado: List[VooBase] = []
    for v in voos:
        resultado.append(
            VooBase(
                voo_id=v.id,
                partida_prevista=v.partida_prevista,
                origem_nome=v.origem.nome,  # Nome da origem
                destino_nome=v.destino.nome,  # Nome do destino
                companhia_nome=v.companhia.nome,  # Nome da companhia
                custo_km=v.custo,  # Passa diretamente o valor de custo
                capacidade=v.aeronave.capacidade  # Capacidade da aeronave
            )
        )
    
    return resultado

# 2) Listar aeroportos de destino a partir de uma origem
@router.get(
    "/aeroporto/{origem_id}/destinos",
    response_model=List[AeroportoBase],
    summary="Listar destinos",
)
def listar_destinos(origem_id: int, db: Session = Depends(get_db)):
    destinos = (
        db.query(Aeroporto)
          .join(Voo, Aeroporto.id == Voo.destino_id)
          .filter(Voo.origem_id == origem_id)
          .distinct()
          .all()
    )
    if not destinos:
        raise HTTPException(status_code=404, detail="Nenhum destino encontrado para esse aeroporto de origem.")
    return destinos

# 3) Listar voos por data — sem IDs, apenas nomes e custo
@router.get(
    "/voos/{data}",
    response_model=List[VooBase],
    summary="Listar voos por data",
)
def listar_voos_por_data(data: date, db: Session = Depends(get_db)):
    inicio = datetime.combine(data, datetime.min.time())
    fim    = datetime.combine(data, datetime.max.time())

    voos = (
        db.query(Voo)
          .options(
              joinedload(Voo.origem),
              joinedload(Voo.destino),
              joinedload(Voo.companhia),
              joinedload(Voo.aeronave)
          )
          .filter(Voo.partida_prevista.between(inicio, fim))
          .all()
    )
    if not voos:
        raise HTTPException(status_code=404, detail="Nenhum voo encontrado para essa data.")

    resultado: List[VooBase] = []
    for v in voos:
        resultado.append(
            VooBase(
                voo_id=v.id,
                companhia_id=v.companhia_id,
                origem_id=v.origem_id,
                destino_id=v.destino_id,
                partida_prevista=v.partida_prevista,
                chegada_prevista=v.chegada_prevista,
                origem_nome=v.origem.nome,
                destino_nome=v.destino.nome,
                companhia_nome=v.companhia.nome,
                capacidade=v.aeronave.capacidade,  # Capacidade da aeronave
                custo_km=float(v.custo)
            )
        )
    return resultado


@router.get("/voo/{voo_id}/custo", summary="Obter custo do voo")
def obter_custo_voo(voo_id: int, db: Session = Depends(get_db)):
    custo = db.query(Voo.custo).filter(Voo.id == voo_id).scalar()
    if custo is None:
        raise HTTPException(status_code=404, detail="Voo não encontrado.")
    return {"custo": float(custo)}
