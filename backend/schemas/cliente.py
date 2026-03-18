from pydantic import BaseModel
from typing import Optional


class ClienteBase(BaseModel):
    id: int
    nome: str
    email: str
    telefone: Optional[str]
    cpf: Optional[str]


class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    cpf: str
    senha: str


class ClienteLogin(BaseModel):
    email: str
    senha: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: Optional[str]
    cpf: Optional[str]
