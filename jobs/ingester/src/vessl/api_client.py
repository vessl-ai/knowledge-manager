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
        for i in range(5):
            response = self._get(f'organizations/{self.config.organization_name}/llm/knowledge/{self.config.knowledge_name}/ingestion/job/{self.config.knowledge_ingestion_job_number}')

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