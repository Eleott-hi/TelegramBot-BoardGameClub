from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column, Boolean

class BoardGame(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    gameName: str
    minPlayers: Optional[int]
    maxPlayers: Optional[int]
    minIdealPlayers: Optional[int]
    maxIdealPlayers: Optional[int]
    minPlayTime: Optional[int]
    maxPlayTime: Optional[int]
    ruleTime: Optional[int]
    gameComplexity: Optional[str]
    minAge: Optional[int]
    year: Optional[int]
    gameShortDescription: Optional[str]
    gameFullDescription: Optional[str]
    coverImageLink: Optional[str]
    videoRulesLink: Optional[str]
    genre: Optional[str]
    status: Optional[bool] = Field(default=False)