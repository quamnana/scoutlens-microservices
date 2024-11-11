from pydantic import BaseModel, Field
from typing import Optional, List


class PlayerBase(BaseModel):
    fullName: str
    nation: str
    position: str
    team: str
    league: str
    age: int


class PlayerResponse(PlayerBase):
    class Config:
        from_attributes = True


class PlayerSearchQuery(BaseModel):
    name: str = Field(..., description="Player name to search for")
    fuzzy: bool = Field(True, description="Enable fuzzy matching")
    size: int = Field(10, ge=1, le=100, description="Number of results to return")


class SearchResponse(BaseModel):
    total: int
    players: List[PlayerResponse]
    took_ms: float
    page: Optional[int] = None
    total_pages: Optional[int] = None
