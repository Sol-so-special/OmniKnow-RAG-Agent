from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache
from core.config import get_settings

@lru_cache()
def get_embeddings():
    """Singleton embedding model."""
    settings = get_settings()
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )