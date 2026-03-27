import os
import logging
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb

logger = logging.getLogger("msoko.ai_usage")

# 1. Setup Local Embedding Model (Free, fast, runs locally)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

class RAGEngine:
    def __init__(self):
        self.db_path = str(Path(__file__).resolve().parent.parent.parent.parent / 'media' / 'chroma_db')
        self.collection_name = "msoko_knowledge"
        
        # Ensure directory exists
        os.makedirs(self.db_path, exist_ok=True)
        
        try:
            # Initialize ChromaDB client
            self.db = chromadb.PersistentClient(path=self.db_path)
            self.chroma_collection = self.db.get_or_create_collection(self.collection_name)
            
            # Assign chroma as vector store
            self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
            self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
            
            self.index = None
            self._load_or_create_index()
        except Exception as e:
            logger.error(f"RAG Initialization failed: {e}")
            self.index = None

    def _load_or_create_index(self):
        if self.chroma_collection.count() > 0:
            # Load existing
            self.index = VectorStoreIndex.from_vector_store(
                self.vector_store,
                embed_model=Settings.embed_model,
            )
            logger.info("RAG Engine loaded from existing ChromaDB.")
        else:
            # Needs initialization for empty store
            self.index = VectorStoreIndex.from_documents(
                [], storage_context=self.storage_context, embed_model=Settings.embed_model
            )
            logger.info("RAG Engine initialized empty ChromaDB.")

    def add_documents_from_directory(self, dir_path: str):
        if not os.path.exists(dir_path):
            logger.warning(f"RAG: Directory {dir_path} not found.")
            return
            
        if self.chroma_collection.count() > 0:
            logger.info("RAG: Collection already has items. Skipping seed to prevent duplicates.")
            return
        
        logger.info(f"RAG: Indexing directory {dir_path}...")
        documents = SimpleDirectoryReader(dir_path).load_data()
        for doc in documents:
            self.index.insert(doc)
        logger.info(f"RAG: Indexed {len(documents)} new document chunks.")

    def query(self, text: str, top_k: int = 3) -> str:
        if not self.index:
            return ""
        
        try:
            if self.chroma_collection.count() == 0:
                return ""
                
            retriever = self.index.as_retriever(similarity_top_k=top_k)
            nodes = retriever.retrieve(text)
            
            if not nodes:
                return ""
                
            context_str = "\n\n".join([n.node.get_content() for n in nodes])
            return context_str
        except Exception as e:
            logger.error(f"RAG Query failed: {e}")
            return ""

# Initialize singleton for the app
rag_engine = RAGEngine()
