import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd


class ESUploader:
    def __init__(self, es_host="http://elasticsearch:9200"):
        self.es = Elasticsearch(hosts=[es_host])
        self.index_name = "players"

    def load_data(self, input_file: str) -> list:
        """Load player data from JSON file"""
        try:
            with open(input_file, "r") as f:
                data = json.load(f)
            print(
                f"Loaded {len(data) if isinstance(data, list) else 1} records from {input_file}"
            )
            return data
        except FileNotFoundError:
            print(f"Error: File {input_file} not found")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {input_file}")
            return []

    def create_index(self):
        """Create the index with appropriate mappings"""
        mappings = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "player_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["lowercase", "asciifolding"],
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "fullName": {
                        "type": "text",
                        "analyzer": "player_analyzer",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                    },
                    "nation": {"type": "keyword"},
                    "position": {"type": "keyword"},
                    "team": {"type": "keyword"},
                    "league": {"type": "keyword"},
                    "age": {"type": "integer"},
                    "yearOfBirth": {"type": "integer"},
                    "matchesPlayed": {"type": "integer"},
                    "matchesStarted": {"type": "integer"},
                    "minutesPlayed": {"type": "float"},
                    "minutesPer90": {"type": "float"},
                    # Attack metrics
                    "goalsScored": {"type": "float"},
                    "totalShots": {"type": "float"},
                    "shotsOnTarget": {"type": "float"},
                    "shotsOnTargetPercentage": {"type": "float"},
                    "goalsPerShot": {"type": "float"},
                    "goalsPerShotOnTarget": {"type": "float"},
                    "averageShotDistance": {"type": "float"},
                    # Passing metrics
                    "totalPassesCompleted": {"type": "float"},
                    "totalPassesAttempted": {"type": "float"},
                    "passCompletionPercentage": {"type": "float"},
                    "assists": {"type": "float"},
                    # Defensive metrics
                    "tackles": {"type": "float"},
                    "tacklesWon": {"type": "float"},
                    "interceptions": {"type": "float"},
                    "blocks": {"type": "float"},
                    # Additional metrics
                    "yellowCards": {"type": "float"},
                    "redCards": {"type": "float"},
                    "foulsCommitted": {"type": "float"},
                    "foulsDrawn": {"type": "float"},
                    # Metadata
                    "updatedAt": {"type": "date"},
                }
            },
            "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        }

        try:
            # Create the index if it doesn't exist
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, body=mappings)
                print(f"Created index: {self.index_name}")
            else:
                print(f"Index {self.index_name} already exists")
        except Exception as e:
            print(f"Error creating index: {str(e)}")

    def prepare_document(self, player_data: dict) -> dict:
        """Prepare the player data document for indexing"""
        doc = player_data.copy()  # Create a copy to avoid modifying original
        doc["updatedAt"] = datetime.now().isoformat()

        # Convert any string numbers to float/int where appropriate
        for key, value in doc.items():
            if isinstance(value, str) and value.replace(".", "").isdigit():
                doc[key] = float(value) if "." in value else int(value)

        return doc

    def generate_bulk_actions(self, players_data: list) -> dict:
        """Generate actions for bulk indexing"""
        # Ensure players_data is a list
        if not isinstance(players_data, list):
            players_data = [players_data]

        for player in players_data:
            yield {
                "_index": self.index_name,
                "_id": f"{player['fullName']}_{player['team']}".lower().replace(
                    " ", "_"
                ),
                "_source": self.prepare_document(player),
            }

    def upload_players(self, players_data: list) -> bool:
        """Upload players data to Elasticsearch"""
        try:
            # Create index if it doesn't exist
            self.create_index()

            # Ensure players_data is a list
            if not isinstance(players_data, list):
                players_data = [players_data]

            # Perform bulk upload
            success, failed = bulk(
                self.es, self.generate_bulk_actions(players_data), refresh=True
            )

            print(f"Successfully uploaded {success} documents")
            if failed:
                print(f"Failed to upload {len(failed)} documents")
                return False

            return True

        except Exception as e:
            print(f"Error uploading data: {str(e)}")
            return False

    def verify_upload(self) -> dict:
        """Verify the upload by counting documents and showing sample"""
        try:
            self.es.indices.refresh(index=self.index_name)
            count = self.es.count(index=self.index_name)
            print(f"Total documents in index: {count['count']}")

            # Get a sample document without sorting by _id
            result = self.es.search(
                index=self.index_name, size=1, body={"query": {"match_all": {}}}
            )

            if result["hits"]["hits"]:
                print("\nSample document:")
                print(json.dumps(result["hits"]["hits"][0]["_source"], indent=2))

            return {
                "total_documents": count["count"],
                "sample_document": (
                    result["hits"]["hits"][0]["_source"]
                    if result["hits"]["hits"]
                    else None
                ),
            }

        except Exception as e:
            print(f"Error verifying upload: {str(e)}")
            return {"total_documents": 0, "sample_document": None}
