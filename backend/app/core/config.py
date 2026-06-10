import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Centralized application settings loaded from environment variables."""

    # Database
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    @property
    def DATABASE_URL(self) -> str:
        # Encode password to handle special characters like '@'
        encoded_password = quote_plus(self.DB_PASSWORD)
        return f"mysql+pymysql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Google AI
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # JWT Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # LLM Models
    EMBED_MODEL_NAME: str = "text-embedding-3-small"
    OLLAMA_TEXT_MODEL: str = "qwen3:4b"          # kept as fallback for text
    OLLAMA_VISION_MODEL: str = "qwen2.5vl:7b"    # vision (rare) stays on Ollama

    # vLLM (primary text engine — OpenAI-compatible, local, continuous batching)
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://127.0.0.1:8001/v1")
    VLLM_TEXT_MODEL: str = os.getenv("VLLM_TEXT_MODEL", "qwen3-4b")
    VLLM_MAX_TOKENS: int = int(os.getenv("VLLM_MAX_TOKENS", "1200"))

    # Embeddings
    EMBEDDINGS_DIRECTORY: str = "."


settings = Settings()
