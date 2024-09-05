from langchain_community.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma

import chromadb
from chromadb.config import Settings


client = chromadb.HttpClient(
    host="https://model-service-gateway-3ewj2oiym34t.seoul.aws-cluster.vessl.ai",
    port=8000,
    settings=Settings(chroma_client_auth_provider="chromadb.auth.basic_authn.BasicAuthClientProvider",chroma_client_auth_credentials="user:password"),
)
collection_name = "knowledge-name-sungbin-test" # Change it to existing collection
collection = client.get_collection(collection_name)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store_from_client = Chroma(
    client=client,
    collection_name=collection_name,
    embedding_function=embeddings,
)

results = vector_store_from_client.similarity_search(
    "What is the docuement about?", k=1
)
print(results)
