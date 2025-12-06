from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..db import get_db

router = APIRouter(tags=["connectors"])


# =============================================================================
# SCHEMAS
# =============================================================================

class ConnectorCreate(BaseModel):
    name: str
    description: Optional[str] = None
    base_url: Optional[str] = None
    auth_type: str = "api_key"  # api_key, oauth2, basic_auth, bearer_token
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    token_url: Optional[str] = None
    additional_headers: Optional[str] = None  # JSON string
    is_active: bool = True
    notes: Optional[str] = None


class ConnectorUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_url: Optional[str] = None
    auth_type: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    token_url: Optional[str] = None
    additional_headers: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get("/")
def list_connectors():
    """
    Lista todos os conectores cadastrados.
    """
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 
                id, name, description, base_url, auth_type,
                api_key, api_secret, client_id, client_secret, token_url,
                additional_headers, is_active, last_sync_at, 
                created_at, updated_at, notes
            FROM api_connectors
            ORDER BY name ASC
            """
        )
        rows = []
        for r in cur.fetchall():
            rows.append({
                "id": r["id"],
                "name": r["name"],
                "description": r["description"],
                "base_url": r["base_url"],
                "auth_type": r["auth_type"],
                "api_key": r["api_key"],
                "api_secret": r["api_secret"],
                "client_id": r["client_id"],
                "client_secret": r["client_secret"],
                "token_url": r["token_url"],
                "additional_headers": r["additional_headers"],
                "is_active": bool(r["is_active"]),
                "last_sync_at": r["last_sync_at"],
                "created_at": r["created_at"],
                "updated_at": r["updated_at"],
                "notes": r["notes"],
            })
    return rows


@router.get("/{connector_id}")
def get_connector(connector_id: int):
    """
    Retorna um conector específico pelo ID.
    """
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT 
                id, name, description, base_url, auth_type,
                api_key, api_secret, client_id, client_secret, token_url,
                additional_headers, is_active, last_sync_at, 
                created_at, updated_at, notes
            FROM api_connectors
            WHERE id = ?
            """,
            (connector_id,)
        )
        r = cur.fetchone()
        
        if not r:
            raise HTTPException(status_code=404, detail="Conector não encontrado")
        
        return {
            "id": r["id"],
            "name": r["name"],
            "description": r["description"],
            "base_url": r["base_url"],
            "auth_type": r["auth_type"],
            "api_key": r["api_key"],
            "api_secret": r["api_secret"],
            "client_id": r["client_id"],
            "client_secret": r["client_secret"],
            "token_url": r["token_url"],
            "additional_headers": r["additional_headers"],
            "is_active": bool(r["is_active"]),
            "last_sync_at": r["last_sync_at"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "notes": r["notes"],
        }


@router.post("/")
def create_connector(connector: ConnectorCreate):
    """
    Cria um novo conector de API.
    """
    now = datetime.now().isoformat()
    
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO api_connectors (
                name, description, base_url, auth_type,
                api_key, api_secret, client_id, client_secret, token_url,
                additional_headers, is_active, created_at, updated_at, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                connector.name,
                connector.description,
                connector.base_url,
                connector.auth_type,
                connector.api_key,
                connector.api_secret,
                connector.client_id,
                connector.client_secret,
                connector.token_url,
                connector.additional_headers,
                1 if connector.is_active else 0,
                now,
                now,
                connector.notes,
            )
        )
        new_id = cur.lastrowid
    
    return {
        "status": "ok",
        "message": "Conector criado com sucesso",
        "id": new_id
    }


@router.put("/{connector_id}")
def update_connector(connector_id: int, connector: ConnectorUpdate):
    """
    Atualiza um conector existente.
    """
    with get_db() as conn:
        cur = conn.cursor()
        
        # Verificar se existe
        cur.execute("SELECT id FROM api_connectors WHERE id = ?", (connector_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Conector não encontrado")
        
        # Montar update dinâmico
        updates = []
        params = []
        
        if connector.name is not None:
            updates.append("name = ?")
            params.append(connector.name)
        if connector.description is not None:
            updates.append("description = ?")
            params.append(connector.description)
        if connector.base_url is not None:
            updates.append("base_url = ?")
            params.append(connector.base_url)
        if connector.auth_type is not None:
            updates.append("auth_type = ?")
            params.append(connector.auth_type)
        if connector.api_key is not None:
            updates.append("api_key = ?")
            params.append(connector.api_key)
        if connector.api_secret is not None:
            updates.append("api_secret = ?")
            params.append(connector.api_secret)
        if connector.client_id is not None:
            updates.append("client_id = ?")
            params.append(connector.client_id)
        if connector.client_secret is not None:
            updates.append("client_secret = ?")
            params.append(connector.client_secret)
        if connector.token_url is not None:
            updates.append("token_url = ?")
            params.append(connector.token_url)
        if connector.additional_headers is not None:
            updates.append("additional_headers = ?")
            params.append(connector.additional_headers)
        if connector.is_active is not None:
            updates.append("is_active = ?")
            params.append(1 if connector.is_active else 0)
        if connector.notes is not None:
            updates.append("notes = ?")
            params.append(connector.notes)
        
        if not updates:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        # Sempre atualizar updated_at
        updates.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        
        params.append(connector_id)
        
        query = f"UPDATE api_connectors SET {', '.join(updates)} WHERE id = ?"
        cur.execute(query, params)
    
    return {"status": "ok", "message": "Conector atualizado com sucesso"}


@router.delete("/{connector_id}")
def delete_connector(connector_id: int):
    """
    Remove um conector.
    """
    with get_db() as conn:
        cur = conn.cursor()
        
        # Verificar se existe
        cur.execute("SELECT id, name FROM api_connectors WHERE id = ?", (connector_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Conector não encontrado")
        
        connector_name = row["name"]
        
        cur.execute("DELETE FROM api_connectors WHERE id = ?", (connector_id,))
    
    return {
        "status": "ok",
        "message": f"Conector '{connector_name}' removido com sucesso"
    }


@router.post("/{connector_id}/toggle")
def toggle_connector(connector_id: int):
    """
    Alterna o status ativo/inativo do conector.
    """
    with get_db() as conn:
        cur = conn.cursor()
        
        cur.execute("SELECT id, is_active, name FROM api_connectors WHERE id = ?", (connector_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Conector não encontrado")
        
        new_status = 0 if row["is_active"] else 1
        cur.execute(
            "UPDATE api_connectors SET is_active = ?, updated_at = ? WHERE id = ?",
            (new_status, datetime.now().isoformat(), connector_id)
        )
    
    return {
        "status": "ok",
        "is_active": bool(new_status),
        "message": f"Conector {'ativado' if new_status else 'desativado'}"
    }


@router.get("/auth-types/options")
def list_auth_types():
    """
    Retorna os tipos de autenticação disponíveis.
    """
    return [
        {"value": "api_key", "label": "API Key", "description": "Autenticação via chave de API no header ou query param"},
        {"value": "bearer_token", "label": "Bearer Token", "description": "Token no header Authorization: Bearer {token}"},
        {"value": "basic_auth", "label": "Basic Auth", "description": "Autenticação básica com usuário e senha"},
        {"value": "oauth2", "label": "OAuth 2.0", "description": "Fluxo OAuth 2.0 com client_id e client_secret"},
        {"value": "custom", "label": "Custom", "description": "Headers personalizados definidos manualmente"},
    ]
