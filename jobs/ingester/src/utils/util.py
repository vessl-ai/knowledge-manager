import base64

import urllib3
import yaml

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