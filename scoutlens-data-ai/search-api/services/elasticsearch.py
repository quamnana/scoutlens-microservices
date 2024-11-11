from elasticsearch import Elasticsearch
from datetime import datetime

from core.config import settings
from models.player import PlayerResponse


class ElasticsearchService:
    def __init__(self):
        self.client = Elasticsearch(hosts=[settings.ELASTICSEARCH_HOST])
        self.index = settings.ELASTICSEARCH_INDEX

    async def search_players(self, name: str, fuzzy: bool = True, size: int = 10):
        query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "fullName": {
                                    "query": name,
                                    "operator": "and",
                                    "fuzziness": "AUTO" if fuzzy else "0",
                                }
                            }
                        },
                        {
                            "match_phrase_prefix": {
                                "fullName": {
                                    "query": name,
                                    "slop": 2,
                                    "max_expansions": 50,
                                }
                            }
                        },
                        {"wildcard": {"fullName": f"*{name.lower()}*"}},
                    ],
                    "minimum_should_match": 1,
                }
            },
            "size": size,
        }

        start_time = datetime.now()
        response = self.client.search(index=self.index, body=query)
        took_ms = (datetime.now() - start_time).total_seconds() * 1000

        hits = response["hits"]["hits"]
        total_hits = response["hits"]["total"]["value"]

        players = []
        for hit in hits:
            try:
                player = hit["_source"]
                # Add score for debugging
                player["_score"] = hit["_score"]
                players.append(player)
            except Exception as e:
                print(f"Error processing player data: {e}")
                continue

        return {"total": total_hits, "players": players, "took_ms": round(took_ms, 2)}

    async def health_check(self) -> bool:
        try:
            return self.client.ping()
        except Exception:
            return False
