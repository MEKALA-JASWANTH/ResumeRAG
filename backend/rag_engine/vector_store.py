# Vector Store - ChromaDB integration for similarity search
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = None
        logger.info(f"ChromaDB initialized at {persist_directory}")
    
    def create_collection(self, name: str = "resumerag", reset: bool = False):
        if reset:
            try:
                self.client.delete_collection(name=name)
                logger.info(f"Deleted existing collection: {name}")
            except:
                pass
        
        self.collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Collection created/loaded: {name}")
        return self.collection
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]], metadatas: List[Dict], ids: Optional[List[str]] = None):
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Added {len(documents)} documents to vector store")
        return ids
    
    def similarity_search(self, query_embedding: List[float], k: int = 5, filter_dict: Optional[Dict] = None) -> Dict:
        query_args = {
            "query_embeddings": [query_embedding],
            "n_results": k
        }
        
        if filter_dict:
            query_args["where"] = filter_dict
        
        results = self.collection.query(**query_args)
        logger.info(f"Found {len(results['documents'][0])} results")
        return results
    
    def get_collection_count(self) -> int:
        if self.collection:
            return self.collection.count()
        return 0
    
    def delete_collection(self, name: str):
        self.client.delete_collection(name=name)
        logger.info(f"Deleted collection: {name}")

if __name__ == "__main__":
    store = VectorStore()
    store.create_collection()
    print(f"Collection count: {store.get_collection_count()}")
