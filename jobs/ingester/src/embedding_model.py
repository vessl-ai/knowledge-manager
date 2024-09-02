import chromadb.utils.embedding_functions as embedding_functions
from chromadb import Documents, EmbeddingFunction, Embeddings

from jobs.ingester.src.config import EmbeddingModelConfig


class CustomEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # embed the documents somehow
        ## TODO: Call the embedding model on remote server
        ## embeddings =  openai_client.embed_documents(input)

        return embeddings

def get_embedding_function(config: EmbeddingModelConfig):

    if config.IsOpenAI():
        return embedding_functions.OpenAIEmbeddingFunction({
            "model": config.model,
            "api_key": config.api_key
        })
    else:
        custom_embedding_function = CustomEmbeddingFunction()
        return custom_embedding_function
    