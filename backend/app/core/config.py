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

    # LLM backend: "vllm" (high concurrency) or "ollama"
    LLM_BACKEND: str = os.getenv("LLM_BACKEND", "vllm")

    # vLLM (primary text engine — handles parallel load)
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://127.0.0.1:8001/v1")
    VLLM_MODEL: str = os.getenv("VLLM_MODEL", "Qwen/Qwen3-4B")
    VLLM_MAX_TOKENS: int = int(os.getenv("VLLM_MAX_TOKENS", "1536"))
    VLLM_MAX_CONTEXT: int = int(os.getenv("VLLM_MAX_CONTEXT", "4096"))
    VLLM_TIMEOUT: float = float(os.getenv("VLLM_TIMEOUT", "300"))

    # RAG retrieval limits (keep prompt within vLLM context window)
    RAG_N_RESULTS: int = int(os.getenv("RAG_N_RESULTS", "6"))
    RAG_MAX_CONTEXT_CHARS: int = int(os.getenv("RAG_MAX_CONTEXT_CHARS", "8000"))

    # Ollama (vision/image queries; fallback text engine)
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    OLLAMA_TEXT_MODEL: str = os.getenv("OLLAMA_TEXT_MODEL", "qwen3:4b")
    OLLAMA_VISION_MODEL: str = os.getenv("OLLAMA_VISION_MODEL", "qwen2.5vl:7b")

    # Embeddings & secondary OpenAI panel
    EMBED_MODEL_NAME: str = "text-embedding-3-small"
    OPENAI_SIDE_MODEL: str = os.getenv("OPENAI_SIDE_MODEL", "gpt-4o-mini")
    OPENAI_SIDE_TIMEOUT: int = int(os.getenv("OPENAI_SIDE_TIMEOUT", "90"))
    OPENAI_POOL_SIZE: int = int(os.getenv("OPENAI_POOL_SIZE", "200"))

    # Embeddings
    EMBEDDINGS_DIRECTORY: str = "."


settings = Settings()
