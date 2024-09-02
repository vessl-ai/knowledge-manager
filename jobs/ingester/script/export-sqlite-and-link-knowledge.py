

DB_SOURCE_PATH = "GET_BY_ENV"
ARTIFACT_NAME = "generated"
KNOWLEDGE_ID = "GET_BY_ENV"

## /chroma-data에 있는 sqlite3 파일을 가져와서, artifact로 업로드
vessl.artifact.get_persistant_artifact_locator(...)
vessl.push_artifact(...)


## knowledge에 artifact를 연결한다.
vessl.llm_knowledge.set_knowledge_database_artifact(...)