#!/bin/bash

export CHROMA_SERVER_AUTHN_CREDENTIALS_FILE="server.htpasswd"
export CHROMA_SERVER_AUTHN_PROVIDER="chromadb.auth.basic_authn.BasicAuthenticationServerProvider"

chroma run --path ./db-data