from fastapi import APIRouter, Depends, HTTPException
import random
import string
from sqlalchemy.orm import Session

from models.database import get_db
from models.reserva import Reserva
from models.voo import Voo
from schemas.reserva import ReservaBase, ReservaCreate
from utils.auth.jwt_auth import get_current_access_payload

router = APIRouter(tags=["Reserva"])


def gerar_localizador():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


def gerar_eticket():
    return "".join(random.choices(string.digits, k=13))


def _get_reserva_do_cliente(db: Session, reserva_id: int, cliente_id: int) -> Reserva:
    reserva = (
        db.query(Reserva)
        .filter(Reserva.id == reserva_id, Reserva.cliente_id == cliente_id)
        .first()
    )
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva


@router.get("/reservas", response_model=list[ReservaBase], summary="Listar reservas")
async def listar_reservas(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_access_payload),
):
    cliente_id = payload.get("sub")
    if not cliente_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    return (
        db.query(Reserva)
        .filter(Reserva.cliente_id == int(cliente_id))
        .order_by(Reserva.id.desc())
        .all()
    )


@router.post("/reservas", response_model=ReservaBase, summary="Efetuar reserva")
async def criar_reserva(
    reserva_data: ReservaCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_access_payload),
):
    cliente_id = payload.get("sub")
    if not cliente_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    # Buscar o voo para garantir que ele existe
    voo = db.query(Voo).filter(Voo.id == reserva_data.voo_id).first()
    
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado")

    nova_reserva = Reserva(
        cliente_id=int(cliente_id),
        voo_id=reserva_data.voo_id,
        status_pagamento="pendente",
        localizador=None,
        numero_eticket=None,
    )

    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)

    return nova_reserva


@router.post(
    "/reservas/{reserva_id}/pagamento",
    response_model=ReservaBase,
    summary="Efetuar pagamento",
)
async def processar_pagamento(
    reserva_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_access_payload),
):
    cliente_id = payload.get("sub")
    if not cliente_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    reserva = _get_reserva_do_cliente(db, reserva_id, int(cliente_id))
    if reserva.status_pagamento == "pago":
        raise HTTPException(status_code=400, detail="Reserva já paga")

    reserva.status_pagamento = "pago"
    reserva.localizador = reserva.localizador or gerar_localizador()
    reserva.numero_eticket = reserva.numero_eticket or gerar_eticket()

    db.commit()
    db.refresh(reserva)

    return reserva
