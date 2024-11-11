from fastapi import APIRouter, HTTPException, Depends

from models.player import PlayerResponse, SearchResponse, PlayerSearchQuery
from services.elasticsearch import ElasticsearchService


router = APIRouter()


@router.get("/search/", response_model=SearchResponse)
async def search_players(
    query: PlayerSearchQuery = Depends(), es_service: ElasticsearchService = Depends()
):
    """
    Search for players by name with optional fuzzy matching.
    """
    try:
        result = await es_service.search_players(
            name=query.name, fuzzy=query.fuzzy, size=query.size
        )
        return SearchResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error searching players: {str(e)}"
        )
