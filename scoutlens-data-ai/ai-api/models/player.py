from typing import Dict, Any
from pydantic import BaseModel


class SearchResponse(BaseModel):
    id: Any
    score: Any
    payload: Dict[str, Any]
