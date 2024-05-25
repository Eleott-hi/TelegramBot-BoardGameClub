from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum as PyEnum


class AuthMethod(str, PyEnum):
    NATIVE = "native"
    GOOGLE = "google"
    GITLAB = "gitlab"
    TELEGRAM = "telegram"


class User(BaseModel):
    id: UUID
    telegram_id: int
    nickname: str
    email: EmailStr
    auth_method: AuthMethod


class BookingFilters(BaseModel):
    game_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    booking_date: Optional[date] = None


class BookingRequest(BaseModel):
    game_id: UUID
    user_id: UUID
    booking_date: date


class BookingResponse(BookingRequest):
    id: UUID


class FastapiError(BaseModel):
    detail: str
