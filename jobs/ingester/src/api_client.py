


def get_vessl_api_client():
    return VESSLAPIClient()

class VESSLAPIClient:
    def __init__(self):
        pass

    def notify_start_processing(self, knowledgeID: str, jobID: str) -> None:
        # dummy
        print('Notify start received')


    def notify_processing_complete(self, jobID: str) -> None:
        """
        Notify the API that the processing of a job has completed.
        """
        url = f"{API_URL}/jobs/{jobID}/complete"
        response = requests.post(url)
        response.raise_for_status()


    def notify_processing_failed(self, jobID: str, error: str) -> None:
        """
        Notify the API that the processing of a job has failed.
        """
        url = f"{API_URL}/jobs/{jobID}/fail"
        response = requests.post(url, json={"error": error})
        response.raise_for_status()


