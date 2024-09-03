import chromadb.utils.embedding_functions as embedding_functions
from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction

from config import EmbeddingModelConfig


class CustomEmbeddingFunction(EmbeddingFunction):
    def __init__(self, input: Documents) -> Embeddings:
        # embed the documents somehow
        ## TODO: Call the embedding model on remote server
        ## embeddings =  openai_client.embed_documents(input)

        pass

def get_embedding_function(config: EmbeddingModelConfig):
    if config.is_openai():
        return OpenAIEmbeddingFunction(api_key=config.api_key, model_name=config.model_name)
    else:
        custom_embedding_function = CustomEmbeddingFunction()
        return custom_embedding_function
    