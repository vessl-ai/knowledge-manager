import yaml

from jobs.ingester.src import embedding_model


class IngesterConfig:
    def __init__(self):
        self._config = get_config()
        self.embedding_model = EmbeddingModelConfig(self._config["embedding_model"])
        self.vector_db = VectorDBConfig(self._config["vector_db"])
        self.knowledge = KnowledgeConfig(self._config["knowledge"])
        self.ingest_options = IngestOptionsConfig(self._config["ingest_options"])
        self.documents = DocumentsConfig(self._config["documents"])

    def get_config(self):
        return self._config

class EmbeddingModelConfig:
    def __init__(self, config):
        self.embedding_model
        pass

    # TODO

class VectorDBConfig:
    
    def __init__(self, config):
        pass
    # todo


class KnowledgeConfig:
    
    def __init__(self, config):
        pass
    # todo


class IngestOptionsConfig:
    
    def __init__(self, config):
        pass
    # todo

class DocumentsConfig:
    
    def __init__(self, config):
        pass
    # todo



def get_config():
    with open("../config/config.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    return cfg
