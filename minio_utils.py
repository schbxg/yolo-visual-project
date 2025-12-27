from minio import Minio
import os
import logging

class MinioStorage:
    def __init__(self, endpoint="127.0.0.1:9000", access_key="minioadmin", secret_key="minioadmin", secure=False):
        """
        Initialize MinIO client. 
        Default credentials are 'minioadmin' for both user and password in standard Docker setups.
        """
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.bucket_name = "yolo-detections"
        self._ensure_bucket()

    def _ensure_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Created MinIO bucket: {self.bucket_name}")
        except Exception as e:
            print(f"Error connecting to MinIO: {e}")

    def upload_file(self, file_path, object_name=None):
        """Uploads a file to the MinIO bucket."""
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        try:
            self.client.fput_object(self.bucket_name, object_name, file_path)
            return True
        except Exception as e:
            print(f"Failed to upload {file_path} to MinIO: {e}")
            return False

    def upload_json(self, json_path):
        return self.upload_file(json_path)

    def upload_image(self, image_path):
        return self.upload_file(image_path)
