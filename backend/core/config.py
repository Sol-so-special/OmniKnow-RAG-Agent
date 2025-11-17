from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal

class Settings(BaseSettings):
    # Environment
    environment: Literal["local", "production"] = "local"
    cloud_provider: Literal["aws", "gcp", "local"] | None = None
    
    # API Keys
    gemini_api_key: str | None = None
    pinecone_api_key: str | None = None
    google_search_api_key: str | None = None
    google_cse_id: str | None = None
    
    # Vector Store
    vector_store_type: Literal["chroma", "pinecone"] = "chroma"
    pinecone_index_name: str = "omniknow"
    pinecone_cloud: str | None = "aws"
    pinecone_region: str | None = "us-east-1"
    chroma_persist_directory: str = "./chroma_db"
    
    # Embeddings
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2"
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["*"]
    
    # Upload Settings
    upload_directory: str = "uploads"
    max_upload_size: int = 200_000_000  # 200MB
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "api.log"
    
    # Storage
    s3_bucket_name: str | None = None
    s3_region: str | None = None
    gcs_bucket_name: str | None = None
    gcs_project_id: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()