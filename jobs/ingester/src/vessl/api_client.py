import os
import time
import requests
from dotenv import dotenv_values

from utils.util import decode_and_parse_yaml, Logger
from vessl.config import Config

env = {
    **dotenv_values(".env"),
    **dotenv_values(".env.local"),
    **os.environ,
}

def get_vessl_api_client():
    return VESSLAPIClient()

class VESSLAPIClient:
    def __init__(self):
        self.base_url = 'https://api.vessl.ai' if env.get("VESSL_API_URL") is None else env.get("VESSL_API_URL")
        self.config = Config()
        self.logger = Logger()
        pass

    def _get(self, endpoint, params=None):
        try:
            access_token = self.config.access_token()
            headers = {
                "Authorization": f"token {access_token}",
            }

            self.logger.info(f" access_token: {access_token}")

            response = requests.get(f"{self.base_url}/api/v1/{endpoint}", params=params, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"GET request failed: {e}")
            return None

    def _post(self, endpoint, data=None):
        try:
            access_token = self.config.access_token()
            headers = {
                "Authorization": f"token {access_token}",
            }
            response = requests.post(f"{self.base_url}/api/v1/{endpoint}", json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"POST request failed: {e}")
            return None

    def _patch(self, endpoint, data=None):
        try:
            access_token = self.config.access_token()
            headers = {
                "Authorization": f"token {access_token}",
            }
            response = requests.patch(f"{self.base_url}/api/v1/{endpoint}", json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"PATCH request failed: {e}")
            return None

    def notify(self, message: str, status: str):
        response = self._patch(f'llm/knowledge/{self.config.knowledge_name}/ingestion/job/{self.config.knowledge_ingestion_job_number}/status', {
            'message': message,
            'status': status
        })

        return response

    def get_input_config(self):

        # get api key by prompt
        api_key = input("Enter your openai api key: ")

        connection_string = input("Enter your vectordb connection string  (e.g. chroma://user:password@http://localhost:8000)")

        return (
            f"""
kind: v1/ingestor
embedding_model: ## Can be retrieved by querying the knowledge
  kind: v1/~~
  type: openai # openai | chroma | huggingface | ?
  model_name: "text-embedding-3-large"
  model_endpoint: "" 
  api_key: "{api_key}"
vectordb:
  kind: v1/~~
  type: "chroma"
  connection_string: "{connection_string}" ## 강제로 항상 localhost일 예정
  collection_name: "test-seokju"
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