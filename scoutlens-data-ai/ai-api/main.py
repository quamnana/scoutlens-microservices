from fastapi import FastAPI
import uvicorn
from qdrant_client import QdrantClient
from services.search_service import SearchService
from endpoints.search_endpoints import router as search_router

app = FastAPI(title="Similar Data Search API")

# Initialize Qdrant client
qdrant_client = QdrantClient(host="qdrant", port=6333)

# Initialize services
search_service = SearchService(qdrant_client)

# Include routers
app.include_router(search_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
