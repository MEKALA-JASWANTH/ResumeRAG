# RAG Pipeline - Orchestrates document processing, embeddings, and vector search
from .document_processor import DocumentProcessor
from .embeddings import EmbeddingService
from .vector_store import VectorStore
from typing import List, Dict
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, collection_name: str = "resumerag"):
        logger.info("Initializing RAG Pipeline...")
        self.doc_processor = DocumentProcessor()
        self.embeddings = EmbeddingService()
        self.vector_store = VectorStore()
        self.collection_name = collection_name
        self.vector_store.create_collection(name=collection_name)
        logger.info("RAG Pipeline initialized successfully")
    
    def index_documents(self, file_paths: List[str]) -> Dict:
        logger.info(f"Starting to index {len(file_paths)} documents")
        
        # Process documents
        chunks = self.doc_processor.process_multiple_documents(file_paths)
        
        if not chunks:
            logger.warning("No chunks created from documents")
            return {"status": "error", "message": "No content extracted", "chunks": 0}
        
        # Extract texts and metadata
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings_list = self.embeddings.embed_documents(texts)
        
        # Generate unique IDs
        ids = [str(uuid.uuid4()) for _ in texts]
        
        # Store in vector database
        logger.info("Storing in vector database...")
        self.vector_store.add_documents(texts, embeddings_list, metadatas, ids)
        
        result = {
            "status": "success",
            "chunks": len(chunks),
            "files_processed": len(file_paths),
            "collection": self.collection_name
        }
        
        logger.info(f"Indexing complete: {result}")
        return result
    
    def search(self, query: str, k: int = 5, filter_dict: Dict = None) -> Dict:
        logger.info(f"Searching for: {query}")
        
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Search vector store
        results = self.vector_store.similarity_search(
            query_embedding, 
            k=k, 
            filter_dict=filter_dict
        )
        
        # Format results
        formatted_results = {
            "query": query,
            "results": [],
            "num_results": len(results.get('documents', [[]])[0])
        }
        
        if results and 'documents' in results:
            for i in range(len(results['documents'][0])):
                formatted_results["results"].append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i] if 'metadatas' in results else {},
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        
        logger.info(f"Found {formatted_results['num_results']} results")
        return formatted_results
    
    def get_stats(self) -> Dict:
        count = self.vector_store.get_collection_count()
        model_info = self.embeddings.get_model_info()
        
        return {
            "total_chunks": count,
            "collection_name": self.collection_name,
            "embedding_model": model_info['model_name'],
            "embedding_dimension": model_info['embedding_dimension']
        }

if __name__ == "__main__":
    # Example usage
    pipeline = RAGPipeline()
    
    # Test indexing
    result = pipeline.index_documents(["sample.pdf"])
    print(f"Indexing result: {result}")
    
    # Test search
    search_result = pipeline.search("What is machine learning?")
    print(f"Search results: {search_result['num_results']} found")
    
    # Get stats
    stats = pipeline.get_stats()
    print(f"Pipeline stats: {stats}")
