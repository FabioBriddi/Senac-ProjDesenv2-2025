import time
import hashlib
import jwt

# Segredos simples para ambiente de desenvolvimento (pode trocar se quiser)
JWT_SECRET = "supersegredo-dev-mudar-depois"
JWT_ALG = "HS256"
JWT_EXPIRE_MIN = 60  # minutos


def hash_password(password: str) -> str:
    """
    Gera um hash simples usando SHA-256.
    Não usa bcrypt para evitar problemas de dependência.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """
    Compara a senha informada com o hash armazenado.
    """
    return hash_password(password) == hashed


def create_token(sub: str, role: str) -> str:
    """
    Cria um JWT com id do usuário (sub) e papel (role).
    """
    payload = {
        "sub": sub,
        "role": role,
        "exp": int(time.time()) + JWT_EXPIRE_MIN * 60,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
