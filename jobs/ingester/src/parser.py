

from config import IngestOptionsConfig


def get_parser(config: IngestOptionsConfig):
    if config.parser == "ragflow":
        return RagflowParser()
    else:
        return BaseParser()

class BaseParser():
    def __init__(self):
        pass

    def parse(self, input):
        pass

class RagflowParser(BaseParser):
    def __init__(self):
        pass

    def parse(self, input):
        pass

    