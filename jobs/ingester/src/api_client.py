


def get_vessl_api_client():
    return VESSLAPIClient()

class VESSLAPIClient:
    def __init__(self):
        pass

    def notify_start_processing(self, knowledgeID: str, jobID: str) -> None:
        # dummy
        print('Notify start received')


    def notify_processing_complete(self, jobID: str) -> None:
        print('Notify procesing received')


    def notify_processing_failed(self, jobID: str, error: str) -> None:
        print('Notify failed received')

    def get_input_config(self, jobID: str) -> str:
        ## mock return
        return '''kind: v1/ingestor
embedding_model: ## Can be retrieved by querying the knowledge
  kind: v1/~~
  type: openai # openai | chroma | huggingface | ?
  model_name: "text-embedding-3-small"
  api_key: "API_KEY_HERE"
  model_endpoint: "" #"https://huggingface.co/bert-base-uncased/resolve/main/pytorch_model.bin" #optional
vectordb:
  kind: v1/~~
  type: "chroma"
  connection_string: "chroma://localhost:8000" ## 강제로 항상 localhost일 예정
  collection_name: "knowledge-name"
knowledge:
  name: "knowledge-name"
  id: 18182837191 # DB Id
  organization_name: "organization-name"
ingest_options:
  parser:
    type: "openparse" # openparse | dify | ?
  chunking:
    method: "character_splitting" # character_splitting | fixed-size | ?
    fixed_size:
      chunk_size: 1000
    character_splitting:
      separator: "\n"
      chunk_size: 1000
      chunk_overlap: 100
documents:
  - id: 100000001
    filename: "한화생명 간편가입 H플러스 보장보험 무배당.pdf"
# xxx(sungbin) : langgraph-runner에서 사용하는 yaml 컨벤션을 어느정도 따라가는건 어떤가요?
# kind: workflowv1/Workflow
# variables:
#   SOME_PERSON:
#     text: GLEN
# nodes:
#   knowledgeSearch:
#     kind: workflowv1/VectorSearch
#     knowledges:
#       - organization: glentest
#         knowledge: glen-brain
#     request:
#       input: "{{ inputs['query'] }}"
#     outputs:
#       result:
#         expr: |-
#           def main(results, **kwargs):
#               return results
#   llmQuery:
#     kind: workflowv1/LLMQuery
#     model:
#       organization: vesls-ai
#       model: llama3-in-seoulland-zoo
#       modelPreset: super-duper-unacceptable-creative
#     request:
#       messages:
#         - role: system
#           content: |-
#             DOCUMENT:
#             {{ outputs['knowledgeSearch']['result']['documents'][0]['content'] }}
#         - role: system
#           content: |-
#             DOCUMENT:
#             {{ outputs['knowledgeSearch']['result']['documents'][1]['content'] }}
#         - role: system
#           content: |-
#             INSTRUCTIONS:
#             Answer the users QUESTION using the DOCUMENTs provided.
#             Keep your answer ground in the facts of the DOCUMENT
#             If the DOCUMENT doesn't contain the facts to the answer the QUESTION, say "I don't know".
# edges:
#   __start__:
#     - next_node: knowledgeSearch
#   knowledgeSearch:
#     - next_node: llmQuery
#   llmQuery:
#     - next_node: __end__
'''

