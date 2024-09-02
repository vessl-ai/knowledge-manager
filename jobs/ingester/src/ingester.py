from parser import get_parser

from api_client import get_vessl_api_client
from chunking import get_chunking_function
from config import IngesterConfig
from embedding_model import get_embedding_function
from vectordb import get_vector_db


class IngestRunner():

    def __init__(self, config: IngesterConfig) -> None:
        self.api_client = get_vessl_api_client()
        self.chunking_function = get_chunking_function(config.ingest_options)
        self.parser = get_parser(config.ingest_options)
        self.embedding_function = get_embedding_function(config.embedding_model)
        self.vector_db = get_vector_db(config.vector_db)

    def run(self):
        # Todo; implement
        self.notify_start()

        try:
            documents = self.load_documents()

            jobs = []
            for document in documents:
                job = self.spawn_document_process_job(document)
                jobs.append(job)

            for job in jobs:
                try:
                    job.run()
                    job.notify_success()
                except Exception as e:
                    job.notify_error()

            print("All jobs completed")

            self.notify_end()
        except:
            self.notify_error()

    def load_documents(self):
        # load from filesystem and validate with vessl api
        pass

    def notify_start(self):
        pass

    def notify_end(self):
        pass

    def notify_error(self):
        pass

    def spawn_document_process_job(self):
        return IngestDocumentJob();


class IngestDocumentJob():
    def __init__(self) -> None:
        pass

    def _load_document(self):
        pass

    def _parse_document(self):
        pass

    def _chunk_document(self):

        pass

    def _embed_document(self):
        pass

    def _push_vectordb(self):
        pass

    def run(self):
        self._load_document()
        self._parse_document()
        self._chunk_document()
        self._embed_document()
        self._push_vectordb()
    
    def notify_success(self):
        # notify api server of its progress
        pass

    def notify_error(self):
        pass