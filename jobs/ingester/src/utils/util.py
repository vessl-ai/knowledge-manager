import base64

import urllib3
import yaml
import logging

class Logger:
    def __init__(self, name='VESSLAPIClient', level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

def decode_and_parse_yaml(encoded_str):
    # Decode the base64 encoded string
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')

    # Parse the YAML content
    parsed_yaml = yaml.safe_load(decoded_str)
    return parsed_yaml

def parse_chroma_url(connection_string):
    # expected format : chroma://user:password@host:port
    connection_string = connection_string.replace("chroma://", "")
    auth, host_port = connection_string.split("@")
    parsed_host = urllib3.util.parse_url(host_port)

    return {
        "auth": auth,
        "host": f"""{parsed_host.scheme}://{parsed_host.host}""",
        "port": parsed_host.port,
    }