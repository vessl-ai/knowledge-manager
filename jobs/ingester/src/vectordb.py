

from jobs.ingester.src.config import VectorDBConfig


def get_vector_db(config: VectorDBConfig):
    if config.type == "chroma":
        return ChromaVectorDB(config)

    print("Invalid VectorDB type")



class BaseVectorDB():
    def __init__(self, config: VectorDBConfig):
        pass

    def save(self, input):
        pass

    def get(self, input):
        pass


class ChromaVectorDB(BaseVectorDB):
    def __init__(self, config: VectorDBConfig):
        super().__init__(config)
        pass

    def save(self, input):
        pass

    def get(self, input):
        pass