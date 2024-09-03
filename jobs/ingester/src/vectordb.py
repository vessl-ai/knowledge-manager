

from typing import List

import chromadb
import urllib3
import urllib3.util
from chromadb import EmbeddingFunction

from config import VectorDBConfig
from models.chunk import Chunk


def get_vector_db(config: VectorDBConfig, embedding_function: EmbeddingFunction):
    if config.type == "chroma":
        return ChromaVectorDB(config, embedding_function)

    print("Invalid VectorDB type")



class BaseVectorDB:
    def __init__(self, config: VectorDBConfig, embedding_function: EmbeddingFunction):
        pass

    def put_one(self, chunk: Chunk):
        pass

    def put_many(self, chunks: List[Chunk]):
        pass


    def get(self, id: int):
        pass

    def query(self, text: str, size: int):
        pass


class ChromaVectorDB(BaseVectorDB):
    def __init__(self, config: VectorDBConfig, embedding_function: EmbeddingFunction):
        super().__init__(config, embedding_function)
        connection_url = urllib3.util.parse_url(config.connection_string)
        self.chroma_client = chromadb.HttpClient(
            host=connection_url.host,
            port=connection_url.port if connection_url.port else "8000",
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name=config.collection_name,
            metadata={"hnsw:space": "cosine"}, # Use cosine similarity instead of Squared L2
            embedding_function=embedding_function
        )

    def put_one(self, chunk: Chunk):
        self.collection.upsert(
            ids=[chunk.chunk_id],
            documents=[chunk.chunk_data],
            metadatas=[{"document_id": chunk.document_id}],
            uris=[chunk.chunk_id]
        )

    def put_many(self, chunks: List[Chunk]):
        return self.collection.upsert(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.chunk_data for chunk in chunks],
            metadatas=[{"document_id": chunk.document_id} for chunk in chunks],
            uris=[chunk.chunk_id for chunk in chunks],
            )


    def get(self, id: int):
        pass

    def query(self, text: str, size: int) -> List[Chunk]:
        raw_result = self.collection.query(query_texts=[text], n_results=size)
        result = [
            Chunk(
                chunk_id=raw_result.get("ids")[0][i],
                chunk_size=0,
                chunk_data=raw_result.get("documents")[0][i],
                document_id=raw_result.get("metadatas")[0][i]["document_id"]
            )
            for i in range(len(raw_result.get("ids")))
        ]

        return result

