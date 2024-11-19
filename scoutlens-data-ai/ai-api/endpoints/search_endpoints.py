from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from services.search_service import SearchService
from qdrant_client import QdrantClient


router = APIRouter(prefix="/search", tags=["search"])


# Dependency to get search service
def get_search_service():
    client = QdrantClient(host="qdrant", port=6333)
    return SearchService(client)


@router.get("/{id}")
async def search_similar(
    id: str,
    limit: Optional[int] = 5,
    search_service: SearchService = Depends(get_search_service),
):
    try:
        similar_items = await search_service.find_similar(int(id), limit)
        return {"results": similar_items}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
