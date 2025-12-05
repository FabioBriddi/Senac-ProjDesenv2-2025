from fastapi import APIRouter, HTTPException
from typing import List
from ..db import get_connection
from ..models import Source, SourceCreate

router = APIRouter()


@router.get("/", response_model=List[Source])
def list_sources():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, active FROM sources")
    rows = cur.fetchall()
    conn.close()

    return [
        Source(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            active=bool(row["active"]),
        )
        for row in rows
    ]


@router.post("/", response_model=Source)
def create_source(payload: SourceCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sources (name, type, active) VALUES (?, ?, ?)",
        (payload.name, payload.type, int(payload.active)),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return Source(id=new_id, **payload.dict())


@router.get("/{source_id}", response_model=Source)
def get_source(source_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, type, active FROM sources WHERE id = ?", (source_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Fonte não encontrada")

    return Source(
        id=row["id"],
        name=row["name"],
        type=row["type"],
        active=bool(row["active"]),
    )
