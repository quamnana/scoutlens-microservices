from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.config import settings
from endpoints import players
from services.elasticsearch import ElasticsearchService

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    players.router, prefix=f"{settings.API_V1_STR}/players", tags=["players"]
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    es_service = ElasticsearchService()
    if await es_service.health_check():
        return {
            "status": "healthy",
            "elasticsearch": "connected",
            "version": settings.VERSION,
        }
    raise HTTPException(status_code=503, detail="Elasticsearch connection failed")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
