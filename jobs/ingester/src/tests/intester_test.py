import chromadb

from config import get_config, VectorDBConfig
from ingester import IngestRunner


def test_ingester():
    config = get_config()
    runner = IngestRunner(config)

    runner.run()

    chroma_client = chromadb.HttpClient(host="localhost", port=8000)

    vectordb_config = VectorDBConfig(config.get_config()["vectordb"])
    collection = chroma_client.get_or_create_collection(vectordb_config.collection_name, embedding_function=runner.embedding_function)

    query_result = collection.query(query_texts=["병으로 보험금 청구가 되어 보험금 지급이 거절되었으나, 진단 이후 제9차 개정 한국표준질병·사인분 류가 적용되고 그 기준에서는 보장하는 질병에 해당된다고 하더라도 보험금을 지급하지 않습니다. "], n_results=10)
    print(query_result)


test_ingester()