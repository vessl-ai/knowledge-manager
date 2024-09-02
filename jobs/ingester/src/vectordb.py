

from typing import List

import chromadb
import urllib3
import urllib3.util
from config import VectorDBConfig
from models.chunk import Chunk
from models.document import Document


def get_vector_db(config: VectorDBConfig):
    if config.type == "chroma":
        return ChromaVectorDB(config)

    print("Invalid VectorDB type")



class BaseVectorDB():
    def __init__(self, config: VectorDBConfig):
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
    def __init__(self, config: VectorDBConfig):
        super().__init__(config)
        connection_url = urllib3.util.parse_url(config.connection_string)
        self.chroma_client = chromadb.HttpClient(
            host=connection_url.host,
            port=connection_url.port if connection_url.port else "8000",
        )
        # TODO: update embedding function
        self.collection = self.chroma_client.get_or_create_collection(
            name=config.collection_name,
            # embedding_function="something"
        ) 

    def put_one(self, chunk: Chunk):
        self.collection.upsert(
            ids=[chunk.chunk_id],
            documents=[chunk.chunk_data],
            uris=[chunk.chunk_id]
        )

    def put_many(self, chunks: List[Chunk]):
        return self.collection.upsert(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.chunk_data for chunk in chunks],
            uris=[chunk.chunk_id for chunk in chunks],
            )


    def get(self, id: int):
        pass

    def query(self, text: str, size: int) -> List[Chunk]:
        raw_result = self.collection.query(query_texts=[text], n_results=size)

        result = [Chunk(chunk_id=doc.id, chunk_size=0, chunk_data=doc.data, document=Document(doc.id, doc.data)) for doc in raw_result]

        return result

