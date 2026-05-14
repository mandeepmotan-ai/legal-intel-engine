from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import uuid

class VectorStoreManager():
    def __init__(self):
        #use an in memory client for developement, while in production this will be a url to qdrant server
        self.client = QdrantClient(":memory")
        self.collection_name = "contracts"

        #initialize the collection
        self.client.recreate_collection(
            collection_name = self.collection_name,
            vectors_config= VectorParams(size=384, distance=Distance.COSINE)
        )
    
    def add_contract_to_db(self, text: str, metadata: dict):
        #simple chunking (for now we will split by double new lines)
        chunks = [c.strip() for c in text.split("\n\n") if len(c) > 20]

        #upload to qdrant (it handles embedding automatically with FastEmbed)
        self.client.add(
            collection_name=self.collection_name,
            documents=chunks,
            metadata=[metadata for _ in chunks],
            ids=[str(uuid.uuid4()) for _ in chunks]
        )
        print(f"Added {len(chunks)} chunks to Vector DB")
    
    def search_contract(self, query: str, limit: int=3):
        #search for the most relevant parts of the contract
        results = self.client.query(
            collection_name=self.collection_name,
            query_text=query,
            limit=limit
        )
        return results