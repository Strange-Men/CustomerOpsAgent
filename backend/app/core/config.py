"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings.

    Reads from environment variables with COOPS_ prefix.
    All values have safe defaults for local development.
    """

    # Application
    app_env: str = "development"
    debug: bool = True

    # LLM Configuration
    use_mock_llm: bool = True
    llm_provider: str = "mock"
    llm_api_key: str = ""
    llm_model: str = "mock-model"

    # Vector Store (for RAG - future)
    vector_store_type: str = "faiss"
    embedding_provider: str = "mock"

    # External APIs (mock mode)
    erp_api_base: str = ""
    erp_api_key: str = ""
    wms_api_base: str = ""
    wms_api_key: str = ""
    logistics_api_base: str = ""
    logistics_api_key: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
