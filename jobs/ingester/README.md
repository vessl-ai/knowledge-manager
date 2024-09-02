# Ingester job

## Overview

API Server

- Build config.yaml
- Mount documents as import to /source-documents
- Mount /chroma-data as export to artifacts

Job

- Initialize Chroma Vector DB as local instance
- Read config.yaml to config.py
- Load embedding model info
- Load document info
- Init vectordb connection (currently only use local)
- Embedd into vectordb
- Export sqlite to /chroma-data

## 할일

1. 일단 chroma가 어딘가 떠있다고 가정하고, src 하위만 작업해서 정상 동작 확인하기 (수요일까지 confidency level 5~7 사이)
2. 그 다음에 import - process - export가 굳이 필요한가를 확인해보자
   -- 사실 Network layer에 있는 DB에 바로 붙어서 사용해도 되는데 이건 나중에 생각해보자
