"""
Test script for MinIO HTTP REST API access.
Run this with: python test_minio_http.py
"""
from minio_utils import MinioStorage
import requests

def main():
    print("=" * 60)
    print("MinIO HTTP REST API Test")
    print("=" * 60)
    
    # Initialize storage
    storage = MinioStorage()
    print(f"\n✓ Connected to MinIO bucket: {storage.bucket_name}")
    
    # List all objects with URLs
    print("\n--- Listing all objects with pre-signed URLs ---")
    objects = storage.list_objects_with_urls()
    
    if not objects:
        print("No objects found in bucket. Upload some files first using live_pose.py")
        return
    
    print(f"Found {len(objects)} object(s):\n")
    
    for i, obj in enumerate(objects, 1):
        print(f"{i}. {obj['name']}")
        print(f"   Size: {obj['size']} bytes")
        print(f"   Modified: {obj['last_modified']}")
        print(f"   Pre-signed URL: {obj['url'][:80]}...")
        print()
        
        # Test HTTP access for the first object
        if i == 1:
            print("   Testing HTTP access...")
            try:
                response = requests.get(obj['url'], timeout=5)
                if response.status_code == 200:
                    print(f"   ✓ HTTP GET successful! Content size: {len(response.content)} bytes")
                else:
                    print(f"   ✗ HTTP GET failed with status: {response.status_code}")
            except Exception as e:
                print(f"   ✗ HTTP request error: {e}")
            print()
    
    # Show example usage
    if objects:
        example_obj = objects[0]['name']
        print("-" * 60)
        print("Example Usage:")
        print("-" * 60)
        print(f'\n# Get pre-signed URL (valid for 1 hour by default):')
        print(f'url = storage.get_presigned_url("{example_obj}")')
        print(f'\n# Get URL valid for 24 hours:')
        print(f'url = storage.get_presigned_url("{example_obj}", expires_hours=24)')
        print(f'\n# Get direct URL (requires public bucket policy):')
        print(f'url = storage.get_direct_url("{example_obj}")')
        print(f'# Direct URL: {storage.get_direct_url(example_obj)}')

if __name__ == "__main__":
    main()
