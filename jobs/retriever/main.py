from typing import List
from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma

import chromadb
from chromadb.config import Settings

from vessl.api_client import get_vessl_api_client

api_client = get_vessl_api_client()

def notify_start():
    api_client.notify(f"{api_client.config.organization_name}/{api_client.config.knowledge_name}/{api_client.config.knowledge_retriever_job_number} Retriever Job started", "in_progress")
def notify_end():
    api_client.notify(f"{api_client.config.organization_name}/{api_client.config.knowledge_name}/{api_client.config.knowledge_retriever_job_number} Retriever Job completed", "completed")
def notify_error():
    api_client.notify(
        f"{api_client.config.organization_name}/{api_client.config.knowledge_name}/{api_client.config.knowledge_retriever_job_number} Retriever Job failed",
        "failed")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        notify_start()
        yield
        notify_end()
    except:
        notify_error()

app = FastAPI(lifespan=lifespan)

class VectorDBClient(BaseModel):
    type: str
    host: str
    port: int
    auth_provider: str | None = None
    auth_credentials: str | None = None

class EmbeddingModel(BaseModel):
    type: str
    model: str

class Query(BaseModel):
    vectordb_client: VectorDBClient
    embedding_model: EmbeddingModel
    collection_name: str
    prompt: str
    top_k: int

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/query")
async def retrieve(query: Query):
    if query.vectordb_client.type != "chroma":
        return None
    
    if query.vectordb_client.auth_provider != None and query.vectordb_client.auth_credentials != None:
        client = chromadb.HttpClient(
            host=query.vectordb_client.host,
            port=query.vectordb_client.port,
            settings=Settings(
                chroma_client_auth_provider=query.vectordb_client.auth_provider,
                chroma_client_auth_credentials=query.vectordb_client.auth_credentials),
        )
    else:
        client = chromadb.HttpClient(
            host=query.vectordb_client.host,
            port=query.vectordb_client.port,
        )
    embeddings = None
    if query.embedding_model.type == "openai":
        embeddings = OpenAIEmbeddings(model=query.embedding_model.model)

    vector_store_from_client = Chroma(
        client=client,
        collection_name=query.collection_name,
        embedding_function=embeddings,
    )

    results = vector_store_from_client.similarity_search(
        query.prompt, k=query.top_k
    )
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)