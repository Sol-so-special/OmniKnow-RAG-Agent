from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from services.vector_store import get_vector_store
from datetime import datetime
import logging
import uuid
import hashlib

logger = logging.getLogger(__name__)

class PDFService:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.collection_name = "pdf_data_collection"
        self.metadata_collection = "pdf_metadata"  # Track processed PDFs
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def _calculate_pdf_hash(self, pdf_path: Path) -> str:
        """Calculate hash of PDF file."""
        with open(pdf_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def _is_already_processed(self, pdf_hash: str) -> bool:
        """Check if PDF hash exists in metadata collection."""
        try:
            results = self.vector_store.similarity_search(
                query=pdf_hash,
                collection_name=self.metadata_collection,
                k=1
            )
            return len(results) > 0 and pdf_hash in results[0].page_content
        except:
            return False
    
    def _store_metadata(self, pdf_hash: str, filename: str, chunks_count: int):
        """Store PDF metadata to prevent duplicates."""
        from langchain.schema import Document
        
        metadata_doc = Document(
            page_content=pdf_hash,  # Store hash as content for exact matching
            metadata={
                "filename": filename,
                "pdf_hash": pdf_hash,
                "chunks_count": chunks_count,
                "processed_at": str(datetime.utcnow())
            }
        )
        self.vector_store.add_documents([metadata_doc], self.metadata_collection)
    
    def process_pdf(self, pdf_path: Path, force_reprocess: bool = False) -> int:
        """Load, chunk, and store PDF."""
        try:
            # Calculate PDF hash
            pdf_hash = self._calculate_pdf_hash(pdf_path)
            
            # Check if already processed
            if not force_reprocess and self._is_already_processed(pdf_hash):
                logger.warning(f"PDF already processed: {pdf_path.name} (hash: {pdf_hash[:8]}...)")
                raise ValueError(
                    f"PDF '{pdf_path.name}' has already been processed. "
                    f"Use force_reprocess=True to override."
                )
            
            # Load PDF
            loader = PyPDFLoader(str(pdf_path), extract_images=False)
            raw_documents = loader.load()
            
            # Split into chunks
            documents = self.text_splitter.split_documents(raw_documents)
            
            # Add metadata
            for i, doc in enumerate(documents):
                doc.metadata["source"] = pdf_path.name
                doc.metadata["page_number"] = doc.metadata.get("page", 0) + 1  # Default value for safety
                doc.metadata["chunk_id"] = str(uuid.uuid4())
                doc.metadata["pdf_hash"] = pdf_hash  # Track which PDF this came from
            
            # Store in vector DB
            num_stored = self.vector_store.add_documents(documents, self.collection_name)
            
            # Store metadata for duplicate detection
            self._store_metadata(pdf_hash, pdf_path.name, num_stored)
            
            logger.info(f"Processed PDF '{pdf_path.name}': {num_stored} chunks stored")
            return num_stored
            
        except Exception as e:
            logger.exception(f"Error processing PDF '{pdf_path}'")
            raise
    
    def search(self, query: str, k: int = 5) -> list:
        """Search PDF knowledge base."""
        try:
            results = self.vector_store.similarity_search(query, self.collection_name, k=k)
            
            structured_results = []
            for res in results:
                structured_results.append({
                    "content": res.page_content,
                    "source": res.metadata.get("source", "unknown"),
                    "page_number": res.metadata.get("page_number", 0)
                })
            
            return structured_results
            
        except Exception as e:
            logger.exception("PDF search failed")
            raise