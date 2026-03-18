import os
from threading import Lock
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


SECRET_KEY = os.getenv("SECRET_KEY", "senhasegura123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
bearer_scheme = HTTPBearer()
ACTIVE_SESSIONS: dict[str, dict] = {}
SESSION_LOCK = Lock()


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def create_session(user_id: str, client_ip: str) -> str:
    session_id = uuid4().hex
    with SESSION_LOCK:
        for current_session_id, session in list(ACTIVE_SESSIONS.items()):
            if session["user_id"] == user_id:
                ACTIVE_SESSIONS.pop(current_session_id, None)
        ACTIVE_SESSIONS[session_id] = {
            "user_id": user_id,
            "ip": client_ip,
            "active": True,
        }
    return session_id


def revoke_session(session_id: str) -> None:
    with SESSION_LOCK:
        ACTIVE_SESSIONS.pop(session_id, None)


def create_access_token(data: dict) -> str:
    payload = data.copy()
    if "sub" in payload:
        payload["sub"] = str(payload["sub"])

    payload["token_type"] = "access"
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = int(expires.timestamp())
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Token expirado") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Token inválido") from exc

    if payload.get("token_type") != "access":
        raise HTTPException(status_code=401, detail="Token inválido para acesso")

    return payload


def get_current_access_payload(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    payload = verify_access_token(credentials.credentials)

    session_id = payload.get("sid")
    if not session_id:
        raise HTTPException(status_code=401, detail="Sessão inválida")

    client_ip = get_client_ip(request)
    with SESSION_LOCK:
        session = ACTIVE_SESSIONS.get(session_id)

    if not session or not session.get("active"):
        raise HTTPException(status_code=401, detail="Sessão encerrada")

    if session.get("ip") != client_ip:
        raise HTTPException(status_code=401, detail="Sessão inválida para este IP")

    return payload
