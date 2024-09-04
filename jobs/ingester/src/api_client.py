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
        response = self._get('hello-job-status')
        yaml = decode_and_parse_yaml(response.get('input_yaml', None))
        return yaml