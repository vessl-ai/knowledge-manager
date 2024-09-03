#!/bin/bash

CHROMA_SERVER_AUTHN_USERNAME=${CHROMA_SERVER_AUTHN_USERNAME:-"$1"}
CHROMA_SERVER_AUTHN_PASSWORD=${CHROMA_SERVER_AUTHN_PASSWORD:-"$2"}

export CHROMA_SERVER_AUTHN_CREDENTIALS_FILE="server.htpasswd"

htpasswd -Bbn $CHROMA_SERVER_AUTHN_USERNAME $CHROMA_SERVER_AUTHN_PASSWORD > $CHROMA_SERVER_AUTHN_CREDENTIALS_FILE