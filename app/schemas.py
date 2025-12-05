
from typing import Optional, Literal
from datetime import date
from pydantic import BaseModel, Field

Role = Literal["ADMIN", "OPERATOR", "VIEWER"]

class UserCreate(BaseModel):
    email: str
    password: str
    role: Role = "VIEWER"

class UserLogin(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SourceIn(BaseModel):
    name: str
    type: Literal["API", "CSV"]

class CSVRow(BaseModel):
    distributor: str
    artist: str
    work_title: str
    isrc: Optional[str] = None
    upc: Optional[str] = None
    platform: Optional[str] = None
    territory: Optional[str] = None
    stream_date: date
    streams: int = Field(ge=0)
    ad_supported: Optional[bool] = None
    subscription: Optional[bool] = None
