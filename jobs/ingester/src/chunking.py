

from typing import List
from config import IngestOptionsConfig
from langchain_text_splitters import CharacterTextSplitter

from models.chunk import Chunk


def get_chunking_function(config: IngestOptionsConfig):
    if config.chunking.method == "character_splitting":
        return CharacterSplittingChunkingFunction(config)
    else:
        return BaseChunkingFunction()


class BaseChunkingFunction():
    def __init__(self):
        pass

    def chunk(self, input: List[str], document_id: str):
        pass


class CharacterSplittingChunkingFunction(BaseChunkingFunction):
    def __init__(self, config: IngestOptionsConfig):
        self.splitter = CharacterTextSplitter(
            separator = config.chunking.character_splitting.separator,
            chunk_size = config.chunking.character_splitting.chunk_size,
            chunk_overlap = config.chunking.character_splitting.chunk_overlap,
            is_separator_regex = True,
        )

    def chunk(self, parsed: List[str], document_id: str) -> List[Chunk]:
        splitted_texts = self.splitter.create_documents(parsed)

        return [Chunk(
            chunk_id=f"{document_id}-{i}",
            chunk_size=len(splitted_text.page_content),
            chunk_data=splitted_text.page_content,
            document_id=document_id
        ) for i, splitted_text in enumerate(splitted_texts)]