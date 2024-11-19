from qdrant_client import QdrantClient


COLLECTION_NAME = "player_embeddings"


class SearchService:
    def __init__(self, client: QdrantClient):
        self.client = client
        self.collection_name = COLLECTION_NAME

    async def find_similar(self, id: int, limit: int = 5):
        try:
            results = self.client.query_points(
                collection_name=COLLECTION_NAME, query=id, limit=limit
            )
            print(results.points)

            payloads = []
            for result in results.points:
                payload = result.payload
                payloads.append(payload)

            print(payloads)
            return payloads

        except Exception as e:
            raise Exception(f"Error searching for similar items: {str(e)}")
