import os

import requests
from dotenv import dotenv_values

from utils.util import decode_and_parse_yaml

env = {
    **dotenv_values(".env"),
    **dotenv_values(".env.local"),
    **os.environ,
}

def get_vessl_api_client():
    return VESSLAPIClient()

class VESSLAPIClient:
    def __init__(self):
        self.base_url = 'https://api-vssl-10567.dev2.vssl.ai' if env.get("VESSL_API_URL") is None else env.get("VESSL_API_URL")
        pass

    def _get(self, endpoint, params=None, headers=None):
        try:
            response = requests.get(f"{self.base_url}/api/v1/{endpoint}", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GET request failed: {e}")
            return None

    def notify_start_processing(self, knowledgeID: str, jobID: str) -> None:
        # dummy
        print('Notify start received')


    def notify_processing_complete(self, jobID: str) -> None:
        print('Notify procesing received')


    def notify_processing_failed(self, jobID: str, error: str) -> None:
        print('Notify failed received')

    def get_input_config(self):
        for i in range(5):
            response = self._get(f'/organizations/{self.config.organization_name}/llm/knowledge/{self.config.knowledge_name}/ingestion/job/{self.config.knowledge_ingestion_job_number}')

            if 400 <= response.status_code < 500:
                reason = response.reason.decode("utf-8")
                self.logger.error(
                    f"{response.status_code} Client Error: {reason} for url: {response.url}"
                )
            elif 500 <= response.status_code < 600:
                reason = response.reason.decode("utf-8")
                self.logger.error(f"{response.status_code} Server Error: {reason} for url: {response.url}")
            else:
                return decode_and_parse_yaml(response.json().get('input_yaml', None))

            self.logger.info(f"Retrying in 5 seconds")
            time.sleep(5)