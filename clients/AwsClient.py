import boto3
import threading

class AwsClient:

    @staticmethod
    def instance():
        return awsClient

    def __init__(self) -> None:
        self._instance_lock = threading.Lock()
        self._clients = {}

    def get_client(self, service_name):
        if service_name not in self._clients:
            with self._instance_lock:
                if service_name not in self._clients:
                    self._clients[service_name] = boto3.client(service_name)
        return self._clients[service_name]

awsClient = AwsClient()