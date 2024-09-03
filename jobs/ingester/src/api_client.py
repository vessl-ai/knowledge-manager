


def get_vessl_api_client():
    return VESSLAPIClient()

class VESSLAPIClient:
    def __init__(self):
        pass

    def notify_start_processing(self, knowledgeID: str, jobID: str) -> None:
        # dummy
        print('Notify start received')


    def notify_processing_complete(self, jobID: str) -> None:
        print('Notify procesing received')


    def notify_processing_failed(self, jobID: str, error: str) -> None:
        print('Notify failed received')

    def get_input_config(self):
        return (
            """
kind: v1/ingestor
embedding_model: ## Can be retrieved by querying the knowledge
  kind: v1/~~
  type: openai # openai | chroma | huggingface | ?
  model_name: "text-embedding-3-small"
  api_key: "API_KEY_HERE"
  model_endpoint: "" #"https://huggingface.co/bert-base-uncased/resolve/main/pytorch_model.bin" #optional
vectordb:
  kind: v1/~~
  type: "chroma"
  connection_string: "chroma://localhost:8000" ## 강제로 항상 localhost일 예정
  collection_name: "knowledge-name-2"
knowledge:
  name: "knowledge-name"
  id: 18182837191 # DB Id
  organization_name: "organization-name"
ingest_options:
  parser:
    type: "openparse" # openparse | dify | ?
  chunking:
    method: "character_splitting" # character_splitting | fixed-size | ?
    fixed_size:
      chunk_size: 1000
    character_splitting:
      separator: "\n"
      chunk_size: 1000
      chunk_overlap: 100
documents:
  - id: 100000001
    filename: "한화생명 간편가입 H플러스 보장보험 무배당.pdf"
            """
        )