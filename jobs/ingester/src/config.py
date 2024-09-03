import os

import dotenv
import yaml
from dotenv import dotenv_values

from api_client import get_vessl_api_client

env = {
    **dotenv_values(".env"),
    **dotenv_values(".env.local"),
    **os.environ,
}


def get_config():
    return IngesterConfig()

class EmbeddingModelConfig:
    def __init__(self, config):
        self.type: str = config["type"]
        self.model_name: str = config["model_name"]
        self.api_key: str = config["api_key"]
        self.model_endpoint: str = config["model_endpoint"]

    def __dict__(self):
        return {
            "type": self.type,
            "model_name": self.model_name,
            "api_key": self.api_key if hasattr(self, "api_key") else env.get("OPENAI_API_KEY") if env.get("OPENAI_API_KEY") != None else None,
            "model_endpoint": self.model_endpoint
        }

    def is_openai(self):
        return self.type == "openai"

class VectorDBConfig:
    
    def __init__(self, config):
        self.type: str = config["type"]
        self.connection_string: str = config["connection_string"]
        self.collection_name: str = config["collection_name"]

    def __dict__(self):
        return {
            "type": self.type,
            "connection_string": self.connection_string,
            "collection_name": self.collection_name
        }

class KnowledgeConfig:
    
    def __init__(self, config):
        self.name: str = config["name"]
        self.id: int = config["id"]
        self.organization_name: str = config["organization_name"]

    def __dict__(self):
        return {
            "name": self.name,
            "id": self.id,
            "organization_name": self.organization_name
        }


class IngestOptionsConfig:
    class IngestOptionParserConfig:
        def __init__(self, config):
            self.type: str = config["type"]
    
    class IngestOptionChunkingConfig:
        class FixedSizeChunkgingConfig:
            def __init__(self, config):
                self.chunk_size: int = config["chunk_size"]
        class CharacterSplittingChunkingConfig:
            def __init__(self, config):
                self.separator: str = config["separator"]
                self.chunk_size: int = config["chunk_size"]
                self.chunk_overlap: int = config["chunk_overlap"]

        def __init__(self, config):
            self.method = config["method"]
            if self.method == "fixed_size":
                self.fixed_size = self.FixedSizeChunkgingConfig(config["fixed_size"])
            elif self.method == "character_splitting":
                self.character_splitting = self.CharacterSplittingChunkingConfig(config["character_splitting"])
            
    def __init__(self, config):
        self.parser = self.IngestOptionParserConfig(config["parser"])
        self.chunking = self.IngestOptionChunkingConfig(config["chunking"])

    def __dict__(self):
        return {
            "parser": {
                "type": self.parser.type
            },
            "chunking": {
                "method": self.chunking.method,
                "fixed_size": {
                    "chunk_size": self.chunking.fixed_size.chunk_size if hasattr(self.chunking, "fixed_size") else None
                },
                "character_splitting": {
                    "separator": self.chunking.character_splitting.separator,
                    "chunk_size": self.chunking.character_splitting.chunk_size,
                    "chunk_overlap": self.chunking.character_splitting.chunk_overlap
                } if hasattr(self.chunking, "character_splitting") else None
            }
        }


class DocumentConfig:
    def __init__(self, config):
        self.id: int = config["id"]
        self.filename: str = config["filename"]

    def __dict__(self):
        return {
            "id": self.id,
            "filename": self.filename
        }


class IngesterConfig:
    def __init__(self):
        self._config = self.get_config()
        self.embedding_model = EmbeddingModelConfig(self._config["embedding_model"])
        self.vector_db = VectorDBConfig(self._config["vectordb"])
        self.knowledge = KnowledgeConfig(self._config["knowledge"])
        self.ingest_options = IngestOptionsConfig(self._config["ingest_options"])
        self.documents = []
        for doc in self._config["documents"]:
            self.documents.append(DocumentConfig(doc))

    def __dict__(self):
        return {
            "embedding_model": self.embedding_model.__dict__(),
            "vectordb": self.vector_db.__dict__(),
            "knowledge": self.knowledge.__dict__(),
            "ingest_options": self.ingest_options.__dict__(),
            "documents": [doc.__dict__() for doc in self.documents]
        }

    def get_config(self):
        vessl_api_client = get_vessl_api_client()
        return yaml.safe_load(vessl_api_client.get_input_config())