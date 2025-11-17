from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from services.vector_store import get_vector_store
from datetime import datetime
import logging
import uuid
import hashlib

logger = logging.getLogger(__name__)

class WebService:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.collection_name = "web_data_collection"
        self.metadata_collection = "web_metadata"  # Track processed URLs
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
    
    def _calculate_url_hash(self, url: str) -> str:
        """Calculate hash of URL."""
        return hashlib.sha256(url.encode('utf-8')).hexdigest()
    
    def _is_already_processed(self, url_hash: str) -> bool:
        """Check if URL hash exists in metadata collection."""
        try:
            results = self.vector_store.similarity_search(
                query=url_hash,
                collection_name=self.metadata_collection,
                k=1
            )
            return len(results) > 0 and url_hash in results[0].page_content
        except:
            return False
    
    def _store_metadata(self, url_hash: str, url: str, chunks_count: int):
        """Store URL metadata to prevent duplicates."""
        from langchain.schema import Document
        
        metadata_doc = Document(
            page_content=url_hash,  # Store hash as content
            metadata={
                "url": url,
                "url_hash": url_hash,
                "chunks_count": chunks_count,
                "processed_at": str(datetime.utcnow())
            }
        )
        self.vector_store.add_documents([metadata_doc], self.metadata_collection)
    
    def process_url(self, url: str, force_reprocess: bool = False) -> int:
        """Scrape, chunk, and store web page."""
        try:
            # Calculate URL hash
            url_hash = self._calculate_url_hash(url)
            
            # Check if already processed
            if not force_reprocess and self._is_already_processed(url_hash):
                logger.warning(f"URL already processed: {url} (hash: {url_hash[:8]}...)")
                raise ValueError(
                    f"URL '{url}' has already been processed. "
                    f"Use force_reprocess=True to override."
                )
            
            # Load web page
            loader = WebBaseLoader(url)
            raw_documents = loader.load()
            
            # Split into chunks
            documents = self.text_splitter.split_documents(raw_documents)
            
            # Add metadata
            for i, doc in enumerate(documents):
                doc.metadata["source_url"] = url
                doc.metadata["chunk_number"] = i + 1
                doc.metadata["chunk_id"] = str(uuid.uuid4())
                doc.metadata["url_hash"] = url_hash  # Track which URL this came from
            
            # Store in vector DB
            num_stored = self.vector_store.add_documents(documents, self.collection_name)
            
            # Store metadata for duplicate detection
            self._store_metadata(url_hash, url, num_stored)
            
            logger.info(f"Processed URL '{url}': {num_stored} chunks stored")
            return num_stored
            
        except Exception as e:
            logger.exception(f"Error processing URL '{url}'")
            raise
    
    def search(self, query: str, k: int = 10) -> list:
        """Search web knowledge base."""
        try:
            results = self.vector_store.similarity_search(query, self.collection_name, k=k)
            
            structured_results = []
            for res in results:
                structured_results.append({
                    "content": res.page_content,
                    "source_url": res.metadata.get("source_url", "unknown"),
                    "chunk_number": res.metadata.get("chunk_number", 0)
                })
            
            return structured_results
            
        except Exception as e:
            logger.exception("Web search failed")
            raise