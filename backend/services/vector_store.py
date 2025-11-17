from abc import ABC, abstractmethod
from langchain_chroma import Chroma
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from core.config import get_settings
from services.embeddings import get_embeddings
import logging

logger = logging.getLogger(__name__)

class VectorStore(ABC):
    """Abstract base class for vector stores."""
    
    @abstractmethod
    def add_documents(self, documents: list, collection_name: str) -> int:
        """Add documents to the store."""
        pass
    
    @abstractmethod
    def similarity_search(self, query: str, collection_name: str, k: int = 5) -> list:
        """Search for similar documents."""
        pass

class ChromaVectorStore(VectorStore):
    """ChromaDB implementation (local development)."""
    
    def __init__(self):
        self.settings = get_settings()
        self.embeddings = get_embeddings()
        self.stores = {}  # Cache stores by collection name
        logger.info("Initialized ChromaDB vector store")
    
    def _get_store(self, collection_name: str):
        if collection_name not in self.stores:
            self.stores[collection_name] = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=f"{self.settings.chroma_persist_directory}/{collection_name}"
            )
        return self.stores[collection_name]
    
    def add_documents(self, documents: list, collection_name: str) -> int:
        store = self._get_store(collection_name)
        store.add_documents(documents)
        logger.info(f"Added {len(documents)} documents to ChromaDB collection '{collection_name}'")
        return len(documents)
    
    def similarity_search(self, query: str, collection_name: str, k: int = 5) -> list:
        store = self._get_store(collection_name)
        results = store.similarity_search(query, k=k)
        logger.info(f"ChromaDB search returned {len(results)} results for collection '{collection_name}'")
        return results

class PineconeVectorStore(VectorStore):
    """Pinecone implementation (cloud production)."""
    
    def __init__(self):
        self.settings = get_settings()
        self.embeddings = get_embeddings()
        
        # Initialize Pinecone client
        self.pc = Pinecone(api_key=self.settings.pinecone_api_key)
        
        # Dynamically get embedding dimension
        try:
            test_embedding = self.embeddings.embed_query("test")
            EMBEDDING_DIM = len(test_embedding)
            logger.info(f"Detected embedding dimension: {EMBEDDING_DIM}")
        except Exception as e:
            EMBEDDING_DIM = 768  # Fallback
            logger.warning(f"Could not detect embedding dim, falling back to {EMBEDDING_DIM}: {e}")

        # Create index if it doesn't exist
        index_name = self.settings.pinecone_index_name
        if index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=index_name,
                dimension=EMBEDDING_DIM,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=self.settings.pinecone_cloud,
                    region=self.settings.pinecone_region
                )
            )
            logger.info(f"Created Pinecone index '{index_name}' on {self.settings.pinecone_cloud}/{self.settings.pinecone_region}")
        
        self.index = self.pc.Index(index_name)
        self.stores = {}
        logger.info(f"Initialized Pinecone vector store on {self.settings.pinecone_cloud}")
    
    def _get_store(self, collection_name: str):
        if collection_name not in self.stores:
            self.stores[collection_name] = PineconeVectorStore(
                index=self.index,
                embedding=self.embeddings,
                namespace=collection_name  # Use namespace for collections
            )
        return self.stores[collection_name]
    
    def add_documents(self, documents: list, collection_name: str) -> int:
        store = self._get_store(collection_name)
        store.add_documents(documents)
        logger.info(f"Added {len(documents)} documents to Pinecone namespace '{collection_name}'")
        return len(documents)
    
    def similarity_search(self, query: str, collection_name: str, k: int = 5) -> list:
        store = self._get_store(collection_name)
        results = store.similarity_search(query, k=k)
        logger.info(f"Pinecone search returned {len(results)} results for namespace '{collection_name}'")
        return results

def get_vector_store() -> VectorStore:
    """Factory function - returns ChromaDB locally, Pinecone in production."""
    settings = get_settings()
    
    if settings.environment == "production" and settings.vector_store_type == "pinecone":
        if not settings.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY required for production environment")
        return PineconeVectorStore()
    else:
        return ChromaVectorStore()