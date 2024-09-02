

from jobs.ingester.src.config import IngestOptionsConfig


def get_chunking_function(config: IngestOptionsConfig):
    if config.chunking_function == "ragflow":
        return NaiveSplittingCHunkginFunction()
    else:
        return BaseChunkingFunction()


class BaseChunkingFunction():
    def __init__(self):
        pass

    def chunk(self, input):
        pass


class NaiveSplittingCHunkginFunction(BaseChunkingFunction):
    def __init__(self):
        pass

    def chunk(self, input):
        pass