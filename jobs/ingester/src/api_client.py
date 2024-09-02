


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


