

from typing import List
from config import IngestOptionsConfig
from langchain_text_splitters import CharacterTextSplitter


def get_chunking_function(config: IngestOptionsConfig):
    if config.chunking.method == "character_splitting":
        return CharacterSplittingChunkingFunction(config)
    else:
        return BaseChunkingFunction()


class BaseChunkingFunction():
    def __init__(self):
        pass

    def chunk(self, input):
        pass


class CharacterSplittingChunkingFunction(BaseChunkingFunction):
    def __init__(self, config: IngestOptionsConfig):
        self.splitter = CharacterTextSplitter(
            separator = config.chunking.character_splitting.separator,
            chunk_size = config.chunking.character_splitting.chunk_size,
            chunk_overlap = config.chunking.character_splitting.chunk_overlap,
            is_separator_regex = True,
        )

    def chunk(self, parsed: List[str]):
        splitted_texts = self.splitter.create_documents(parsed)
        return [i.page_content for i in splitted_texts]