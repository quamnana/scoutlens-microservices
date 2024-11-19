class Settings:
    API_V1_STR = "/api/v1"
    PROJECT_NAME = "Player Search API"
    VERSION = "1.0.0"
    DESCRIPTION = "API for searching soccer player statistics"

    # Elasticsearch settings
    ELASTICSEARCH_HOST = "http://elasticsearch:9200"
    ELASTICSEARCH_INDEX = "players"

    # API settings
    MAX_SEARCH_RESULTS = 100
    DEFAULT_SEARCH_SIZE = 10
    ENABLE_FUZZY_SEARCH = True


settings = Settings()
