from typing import TYPE_CHECKING

from pydantic import BaseModel

from schemas.cliente import ClienteResponse

if TYPE_CHECKING:
    from models.cliente import Cliente


class LoginResponse(ClienteResponse):
    access_token: str
    token_type: str = "bearer"

    @classmethod
    def from_cliente(cls, cliente: "Cliente", access_token: str) -> "LoginResponse":
        cliente_data = ClienteResponse.model_validate(cliente, from_attributes=True).model_dump()
        return cls(**cliente_data, access_token=access_token)


class LoginTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str


class SessionResponse(BaseModel):
    user: dict
