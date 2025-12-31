from minio import Minio
from datetime import timedelta
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
        self.endpoint = endpoint
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

    def get_presigned_url(self, object_name, expires_hours=1):
        """
        Get a pre-signed URL for HTTP access to an object.
        This URL can be used in browsers, <img> tags, or any HTTP client.
        
        Args:
            object_name: The object name in MinIO (e.g., "fall_20251231_140000.jpg")
            expires_hours: How long the URL is valid (default: 1 hour, max: 7 days)
        
        Returns:
            Pre-signed URL string or None if failed
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket_name, 
                object_name, 
                expires=timedelta(hours=expires_hours)
            )
            return url
        except Exception as e:
            print(f"Failed to generate presigned URL: {e}")
            return None

    def get_direct_url(self, object_name):
        """
        Get direct URL (only works if bucket has public read policy).
        Format: http://127.0.0.1:9000/yolo-detections/object_name
        
        Note: For this to work, you need to set the bucket policy to public.
        You can do this in MinIO Console or via: mc anonymous set download myminio/bucket
        """
        protocol = "https" if "https" in self.endpoint else "http"
        return f"{protocol}://{self.endpoint}/{self.bucket_name}/{object_name}"

    def list_objects_with_urls(self, prefix="", expires_hours=1):
        """
        List all objects in the bucket with their pre-signed URLs.
        
        Args:
            prefix: Optional prefix to filter objects (e.g., "fall_alerts/")
            expires_hours: URL validity duration
        
        Returns:
            List of dicts with 'name', 'size', 'last_modified', and 'url' keys
        """
        try:
            objects = self.client.list_objects(self.bucket_name, prefix=prefix)
            result = []
            for obj in objects:
                url = self.get_presigned_url(obj.object_name, expires_hours)
                result.append({
                    'name': obj.object_name,
                    'size': obj.size,
                    'last_modified': obj.last_modified,
                    'url': url
                })
            return result
        except Exception as e:
            print(f"Failed to list objects: {e}")
            return []
