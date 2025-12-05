from fastapi import APIRouter, HTTPException
from ..db import get_connection
from ..models import LoginRequest, LoginResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (payload.username, payload.password),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Token fake só para a demo
    token = f"fake-token-for-{payload.username}"
    return LoginResponse(access_token=token)
