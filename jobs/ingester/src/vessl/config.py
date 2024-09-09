import os
import threading
from dotenv import dotenv_values

token_once = threading.Lock()
access_token_file = "/opt/vessl/access_token/token_file"
initial_access_token_file = "/opt/vessl/initial_config/access_token"

class Config:
    def __init__(self):
        self.env = {
            **dotenv_values(".env"),
            **dotenv_values(".env.local"),
            **os.environ,
        }
        self.vessl_api_url = self.env.get("VESSL_API_URL", "https://api.vessl.ai")
        self.organization_name = self.env.get("VESSL_ORGANIZATION_NAME", "")
        self.knowledge_name = self.env.get("VESSL_KNOWLEDGE_NAME", "")
        self.knowledge_ingestion_job_number = self.env.get("VESSL_KNOWLEDGE_INGESTION_JOB_NUMBER", 1)
        self.access_token = self.access_token_getter()

    def get(self, key, default=None):
        return self.env.get(key, default)

    def access_token_getter():
        def get_token():
            with token_once:
                if not os.path.exists(access_token_file):
                    try:
                        with open(initial_access_token_file, 'r') as f:
                            token_bytes = f.read()
                    except Exception as e:
                        raise RuntimeError(f"initialAccessToken read error: {e}")

                    try:
                        os.makedirs("/opt/vessl", exist_ok=True)
                    except Exception as e:
                        raise RuntimeError(e)

                    try:
                        with open(access_token_file, 'w') as f:
                            f.write(token_bytes)
                    except Exception as e:
                        raise RuntimeError(e)

            try:
                with open(access_token_file, 'r') as f:
                    data = f.read()
                return data.strip()
            except Exception as e:
                print(f"WARN: access token read failed: {e}")
                return ""

        return get_token