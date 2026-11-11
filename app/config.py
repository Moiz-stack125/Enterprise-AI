from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Gemini (LLM + embeddings)
    gemini_api_key: str = ""
    gemini_chat_model: str = "gemini-2.5-flash"
    gemini_embed_model: str = "gemini-embedding-001"
    embed_dim: int = 768

    # Render PostgreSQL
    database_url: str = ""

    # Pinecone
    pinecone_api_key: str = ""
    pinecone_index_name: str = "atlas-rag-index"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"
    pinecone_ready_timeout: int = 180

    # Rius observability (optional)
    rius_api_key: str = ""
    rius_service_name: str = "atlas-ai-enterprise"
    rius_disabled: bool = False
    rius_capture_content: bool = False

    # App behaviour
    max_upload_bytes: int = 10485760
    min_relevance: float = 0.25
    hitl_enabled: bool = True
    memory_turns: int = 6

@lru_cache
def settings():
    return Settings()