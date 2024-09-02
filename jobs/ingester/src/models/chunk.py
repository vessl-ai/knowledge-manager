from models.document import Document


class Chunk:
    def __init__(self, chunk_id, chunk_size, chunk_data, document: Document):
        self.chunk_id = chunk_id
        self.chunk_size = chunk_size
        self.chunk_data = chunk_data
        self.document = document

    def __str__(self):
        return f"Chunk {self.chunk_id} with size {self.chunk_size} and data {self.chunk_data}"