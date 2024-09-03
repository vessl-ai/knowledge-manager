

from config import IngestOptionsConfig
import openparse
import openparse.schemas


def get_parser(config: IngestOptionsConfig):
    if config.parser.type == "openparse":
        return OpenparseParser()
    else:
        return BaseParser()

class BaseParser():
    def __init__(self):
        pass

    def parse(self, input):
        pass

class OpenparseParser(BaseParser):
    def __init__(self):
        self.parser = openparse.DocumentParser()

    def parse(self, input_path) -> openparse.schemas.ParsedDocument:
        return self.parser.parse(input_path)

    