from elasticsearch import Elasticsearch
import json


class ESDebugger:
    def __init__(
        self, es_host="http://localhost:9300"
    ):  # Changed default host to localhost
        self.es = Elasticsearch(hosts=[es_host])
        self.index = "players"

    def check_index_exists(self):
        """Check if index exists"""
        exists = self.es.indices.exists(index=self.index)
        print(f"Index '{self.index}' exists: {exists}")
        return exists

    def get_index_mapping(self):
        """Get index mapping"""
        try:
            mapping = self.es.indices.get_mapping(index=self.index)
            # Convert mapping to dict if it's not already
            mapping_dict = dict(mapping)
            print("\nCurrent mapping:")
            print(json.dumps(mapping_dict, indent=2))
            return mapping_dict
        except Exception as e:
            print(f"Error getting mapping: {str(e)}")
            return None

    def count_documents(self):
        """Count documents in index"""
        try:
            count = self.es.count(index=self.index)
            print(f"\nTotal documents in index: {count['count']}")
            return count["count"]
        except Exception as e:
            print(f"Error counting documents: {str(e)}")
            return 0

    def get_sample_documents(self, size=5):
        """Get sample documents"""
        try:
            query = {"query": {"match_all": {}}, "size": size}
            response = self.es.search(index=self.index, body=query)
            total = response["hits"]["total"]["value"]
            hits = response["hits"]["hits"]

            print(f"\nSample documents ({min(size, total)} of {total}):")
            for hit in hits:
                print(f"\nDocument ID: {hit['_id']}")
                print(json.dumps(hit["_source"], indent=2))
            return hits
        except Exception as e:
            print(f"Error getting sample documents: {str(e)}")
            return []

    def test_search(self, name):
        """Test different search queries"""
        try:
            # Test 1: Exact match
            exact_query = {"query": {"match": {"fullName": name}}}
            exact_results = self.es.search(index=self.index, body=exact_query)
            print(
                f"\nExact match results for '{name}': {exact_results['hits']['total']['value']}"
            )
            if exact_results["hits"]["hits"]:
                print("Sample exact match:")
                print(json.dumps(exact_results["hits"]["hits"][0]["_source"], indent=2))

            # Test 2: Fuzzy match
            fuzzy_query = {
                "query": {"match": {"fullName": {"query": name, "fuzziness": "AUTO"}}}
            }
            fuzzy_results = self.es.search(index=self.index, body=fuzzy_query)
            print(
                f"\nFuzzy match results for '{name}': {fuzzy_results['hits']['total']['value']}"
            )
            if fuzzy_results["hits"]["hits"]:
                print("Sample fuzzy match:")
                print(json.dumps(fuzzy_results["hits"]["hits"][0]["_source"], indent=2))

            # Test 3: Term query
            term_query = {"query": {"wildcard": {"fullName": f"*{name.lower()}*"}}}
            term_results = self.es.search(index=self.index, body=term_query)
            print(
                f"\nWildcard query results for '{name}': {term_results['hits']['total']['value']}"
            )
            if term_results["hits"]["hits"]:
                print("Sample wildcard match:")
                print(json.dumps(term_results["hits"]["hits"][0]["_source"], indent=2))

            return {
                "exact": exact_results,
                "fuzzy": fuzzy_results,
                "term": term_results,
            }
        except Exception as e:
            print(f"Error testing search: {str(e)}")
            return {}

    def list_all_indices(self):
        """List all indices in Elasticsearch"""
        try:
            indices = self.es.indices.get_alias().keys()
            print("\nAvailable indices:")
            for index in indices:
                print(f"- {index}")
            return list(indices)
        except Exception as e:
            print(f"Error listing indices: {str(e)}")
            return []


def main():
    try:
        debugger = ESDebugger()

        # List all available indices
        print("Checking available indices...")
        indices = debugger.list_all_indices()

        # Basic checks
        if not debugger.check_index_exists():
            print("Index doesn't exist! Data hasn't been indexed properly.")
            return

        # Get mapping
        debugger.get_index_mapping()

        # Count documents
        doc_count = debugger.count_documents()
        if doc_count == 0:
            print("No documents in index! Data hasn't been uploaded.")
            return

        # Get sample documents
        debugger.get_sample_documents()

        # Test search with sample name
        print("\nTesting search functionality...")
        debugger.test_search("Aaronson")

    except Exception as e:
        print(f"Error in main: {str(e)}")


if __name__ == "__main__":
    main()
