import os
from typing import List

from models.chunk import Chunk
from parser import get_parser

from vessl.api_client import get_vessl_api_client
from chunking import get_chunking_function
from config import IngesterConfig, DocumentConfig
from embedding_model import get_embedding_function
from vectordb import get_vector_db


class IngestRunner():

    def __init__(self, config: IngesterConfig) -> None:
        self.documents = config.documents
        self.api_client = get_vessl_api_client()
        self.chunking_function = get_chunking_function(config.ingest_options)
        self.parser = get_parser(config.ingest_options)
        self.embedding_function = get_embedding_function(config.embedding_model)
        self.vector_db = get_vector_db(config.vector_db, self.embedding_function)

    def run(self):
        self.notify_start()

        try:


            jobs = []
            for document_config in self.documents:
                job = self.spawn_document_process_job(document_config)
                jobs.append(job)

            for job in jobs:
                try:
                    job.run()
                    job.notify_success()

                except Exception as e:
                    job.notify_error(e)

            print("All jobs completed")

            self.notify_end()
        except:
            self.notify_error()

    def load_document(self, document: DocumentConfig):
        return os.path.join(os.path.curdir, f"source-documents/{document.filename}")

    def notify_start(self):
        self.api_client.notify(f"{self.api_client.config.organization_name}/{self.api_client.config.knowledge_name}/{self.api_client.config.knowledge_ingestion_job_number} Ingestion Job started", "in_progress")

    def notify_end(self):
        self.api_client.notify(f"{self.api_client.config.organization_name}/{self.api_client.config.knowledge_name}/{self.api_client.config.knowledge_ingestion_job_number} Ingestion Job completed", "completed")

    def notify_error(self):
        self.api_client.notify(
            f"{self.api_client.config.organization_name}/{self.api_client.config.knowledge_name}/{self.api_client.config.knowledge_ingestion_job_number} Ingestion Job failed",
            "failed")

    def spawn_document_process_job(self, document_config):
        return IngestDocumentJob(self, document_config)


class IngestDocumentJob():
    def __init__(self, runner: IngestRunner, document_config: DocumentConfig) -> None:
        self.runner = runner
        self.document_config = document_config
        self.document_path = os.path.join(os.path.curdir, f"source-documents/{document_config.filename}")

    def _parse_document(self):
        print(f"Parsing {self.document_path} ..")
        output = []
        for node in self.runner.parser.parse(self.document_path).nodes:
            output.append(node.text)
        return output

    def _chunk_document(self, parsed: List[str]) -> List[Chunk]:
        output = self.runner.chunking_function.chunk(parsed, self.document_config.id)
        return output

    def _push_vectordb(self, chunked: List[Chunk]):
        self.runner.vector_db.put_many(chunked)

    def run(self):
        parsed = self._parse_document()
        chunked = self._chunk_document(parsed)
        self._push_vectordb(chunked) # embed and push to vectordb

    def notify_success(self):
        print(f"{self.document_config.filename} Document processed successfully")

    def notify_error(self, error):
        print(f"An error occurred: {error}")