

from config import IngestOptionsConfig


def get_chunking_function(config: IngestOptionsConfig):
    if config.chunking.method == "ragflow":
        return NaiveSplittingChunkingFunction()
    else:
        return BaseChunkingFunction()


class BaseChunkingFunction():
    def __init__(self):
        pass

    def chunk(self, input):
        pass


class NaiveSplittingChunkingFunction(BaseChunkingFunction):
    def __init__(self):
        pass

    def chunk(self, input):
        pass