import chromadb

from config import get_config, VectorDBConfig
from models.chunk import Chunk
from models.document import Document
from vectordb import get_vector_db


def _set_up():
    ingester_config = get_config()
    config = ingester_config.get_config()
    return VectorDBConfig(config["vectordb"])

def test_put_one_vectordb():
    vector_config = _set_up()
    chroma_vector_db = get_vector_db(vector_config)

    # Create a dummy Document instance
    dummy_document = Document(
        id="1",
        filename="dummy.txt",
        content="This is some dummy content.",
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-02T00:00:00Z"
    )

    # Create a dummy Chunk instance
    dummy_chunk = Chunk(
        chunk_id="1",
        chunk_size=1024,
        chunk_data="This is some chunk data.",
        document_id=dummy_document.id
    )

    chroma_vector_db.put_one(dummy_chunk)
    result_chunks = chroma_vector_db.query("This is some chunk data.", 1)

    # retrieve the chunk from the collection
    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    collection = chroma_client.get_or_create_collection(vector_config.collection_name)
    result = collection.get(dummy_chunk.chunk_id)

    # assertion
    assert result['documents'][0] == dummy_chunk.chunk_data, "Chunk data does not match"
    assert result_chunks[0].chunk_data == dummy_chunk.chunk_data, "Chunk data does not match"

def test_put_many_vectordb():
    vector_config = _set_up()
    chroma_vector_db = get_vector_db(vector_config)

    # Create dummy Document instances
    dummy_documents = [
        Document(
            id="1",
            filename="dummy1.txt",
            content="This is some dummy content 1.",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-02T00:00:00Z"
        ),
        Document(
            id="2",
            filename="dummy2.txt",
            content="This is some dummy content 2.",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-02T00:00:00Z"
        )
    ]

    # Create dummy Chunk instances
    dummy_chunks = [
        Chunk(
            chunk_id="1",
            chunk_size=1024,
            chunk_data="This is some chunk data 1.",
            document_id=dummy_documents[0].id
        ),
        Chunk(
            chunk_id="2",
            chunk_size=1024,
            chunk_data="This is some chunk data 2.",
            document_id=dummy_documents[1].id
        )
    ]

    chroma_vector_db.put_many(dummy_chunks)
    result_chunks = chroma_vector_db.query("This is some chunk data 2.", 2)

    # Retrieve the inserted chunks
    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    collection = chroma_client.get_or_create_collection(vector_config.collection_name)
    result1 = collection.get(dummy_chunks[0].chunk_id)
    result2 = collection.get(dummy_chunks[1].chunk_id)

    # Assertions
    assert result1['documents'][0] == dummy_chunks[0].chunk_data, "Chunk data 1 does not match"
    assert result2['documents'][0] == dummy_chunks[1].chunk_data, "Chunk data 2 does not match"
    assert result_chunks[0].chunk_data == dummy_chunks[1].chunk_data, "Chunk data does not match"


test_put_one_vectordb()
test_put_many_vectordb()