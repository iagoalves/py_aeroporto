import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from models.cliente import Cliente
from models.database import get_db
from schemas.auth import LoginTokenResponse, MessageResponse, SessionResponse
from schemas.cliente import ClienteCreate, ClienteLogin
from utils.auth.jwt_auth import (
    create_session,
    create_access_token,
    get_current_access_payload,
    get_client_ip,
    revoke_session,
)

router = APIRouter(tags=["Login"])


@router.post("/register", response_model=LoginTokenResponse, summary="Register")
def register(
    cliente_data: ClienteCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    if db.query(Cliente).filter(Cliente.email == cliente_data.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    if db.query(Cliente).filter(Cliente.cpf == cliente_data.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    cliente = Cliente(
        nome=cliente_data.nome,
        email=cliente_data.email,
        telefone=cliente_data.telefone,
        cpf=cliente_data.cpf,
        senha_hash=bcrypt.hashpw(
            cliente_data.senha.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8"),
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    client_ip = get_client_ip(request)
    session_id = create_session(str(cliente.id), client_ip)
    access_token = create_access_token(
        {
            "sub": str(cliente.id),
            "email": cliente.email,
            "sid": session_id,
            "ip": client_ip,
        }
    )
    return LoginTokenResponse(access_token=access_token)


@router.post("/login", response_model=LoginTokenResponse, summary="Login")
def login(
    cliente_login: ClienteLogin,
    request: Request,
    db: Session = Depends(get_db),
):
    cliente = db.query(Cliente).filter(Cliente.email == cliente_login.email).first()

    if not cliente or not bcrypt.checkpw(
        cliente_login.senha.encode("utf-8"),
        cliente.senha_hash.encode("utf-8"),
    ):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    client_ip = get_client_ip(request)
    session_id = create_session(str(cliente.id), client_ip)
    access_token = create_access_token(
        {
            "sub": str(cliente.id),
            "email": cliente.email,
            "sid": session_id,
            "ip": client_ip,
        }
    )
    return LoginTokenResponse(access_token=access_token)


@router.get("/verificar_sessao", response_model=SessionResponse, summary="Verificar sessao")
def verify_session(payload: dict = Depends(get_current_access_payload)):
    return SessionResponse(user=payload)


@router.post("/logout", response_model=MessageResponse, summary="Logout")
def logout(payload: dict = Depends(get_current_access_payload)):
    session_id = payload.get("sid")
    if not session_id:
        raise HTTPException(status_code=401, detail="Sessão inválida")

    revoke_session(session_id)
    return MessageResponse(message="Logout efetuado com sucesso")
