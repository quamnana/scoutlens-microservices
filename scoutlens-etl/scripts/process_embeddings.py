import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct
import uuid
import os

# Define Qdrant client and collection name

QDRANT_COLLECTION = "player_embeddings"
QDRANT_HOST = os.getenv("QDRANT_HOST", "http://localhost:6333")


# Initialize Qdrant client
# client = QdrantClient(QDRANT_HOST)
client = QdrantClient(host="qdrant", port=6333)


def persist_to_qdrant(data: pd.DataFrame, collection_name: str):
    """
    Persist player embeddings to Qdrant.
    :param data: DataFrame containing player embeddings.
    :param collection_name: Name of the Qdrant collection.
    """
    points = []

    for index, row in data.iterrows():
        if row["embedding"] is not None:
            point = PointStruct(
                id=row.get("rank"),
                vector=row["embedding"],
                payload={
                    "rank": row.get("rank"),
                    "fullName": row.get("fullName"),
                    "nation": row.get("nation"),
                    "position": row.get("position"),
                    "team": row.get("team"),
                    "league": row.get("league"),
                    "age": row.get("age"),
                },
            )
            points.append(point)

    try:
        client.upsert(collection_name=collection_name, points=points)
        print(f"Successfully persisted {len(points)} player embeddings to Qdrant.")
    except Exception as e:
        print(f"Error persisting data to Qdrant: {e}")


def read_and_store_embeddings(file_path: str):
    # Load the JSON file
    players_df = pd.read_json(file_path)
    embedding_size = len(players_df["embedding"].dropna().iloc[0])

    client.recreate_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=embedding_size, distance="Cosine"),
    )

    # # Persist embeddings to Qdrant
    persist_to_qdrant(players_df, QDRANT_COLLECTION)
