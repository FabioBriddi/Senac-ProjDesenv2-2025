from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SourceBase(BaseModel):
    name: str
    type: str
    active: bool = True


class SourceCreate(SourceBase):
    pass


class Source(SourceBase):
    id: int


class IngestionBase(BaseModel):
    source_id: int
    file_name: Optional[str] = None
    ingested_at: Optional[str] = None
    total_rows: Optional[int] = None


class IngestionCreate(IngestionBase):
    pass


class Ingestion(IngestionBase):
    id: int


class PlaySummary(BaseModel):
    artist: str
    platform: str
    plays: int
    revenue: float
