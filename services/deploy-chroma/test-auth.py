#!/usr/bin/env python

import chromadb
from chromadb.config import Settings

client = chromadb.HttpClient(
  settings=Settings(chroma_client_auth_provider="chromadb.auth.basic_authn.BasicAuthClientProvider",chroma_client_auth_credentials="admin:admin"))
client.heartbeat()  # this should work with or without authentication - it is a public endpoint
client.get_version()  # this should work with or without authentication - it is a public endpoint
col = client.get_or_create_collection("helloworld")
print(col)
client.list_collections() 