import boto3
import threading

class AwsClient:
    _instance_lock = threading.Lock()
    _clients = {}

    @classmethod
    def get_client(cls, service_name):
        if service_name not in cls._clients:
            with cls._instance_lock:
                if service_name not in cls._clients:
                    cls._clients[service_name] = boto3.client(service_name)
        return cls._clients[service_name]