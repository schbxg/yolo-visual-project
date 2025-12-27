# MinIO Usage Guide

This document explains how to set up and use MinIO object storage with the YOLO project.

## 1. Installation & Deployment

### Native Windows (Recommended)
1.  **Download**: [minio.exe](https://dl.min.io/server/minio/release/windows-amd64/minio.exe) to your project root.
2.  **Start Server**:
    ```powershell
    mkdir C:\minio_data
    .\minio.exe server C:\minio_data --console-address ":9001"
    ```

### Docker
If you prefer containers:
```powershell
docker run -d -p 9000:9000 -p 9001:9001 `
  --name minio `
  -e "MINIO_ROOT_USER=minioadmin" `
  -e "MINIO_ROOT_PASSWORD=minioadmin" `
  quay.io/minio/minio server /data --console-address ":9001"
```

---

## 2. Web Console Access

- **URL**: [http://localhost:9001](http://localhost:9001)
- **Username**: `minioadmin` (Default)
- **Password**: `minioadmin` (Default)

Inside the console, you can manage buckets and view uploaded detection images/JSON files.

---

## 3. Python Integration

### Configuration
The connection parameters are managed in `minio_utils.py`:
```python
# Default values in minio_utils.py
endpoint = "127.0.0.1:9000"
access_key = "minioadmin"
secret_key = "minioadmin"
```
If your MinIO server is on a different machine, update these values.

### Using in `live_pose.py`
1.  **Start the script**: `python live_pose.py`
2.  **Enable Upload**: Slide the **"MinIO"** trackbar to **1**.
3.  **Automatic Alerts**: When a fall is detected, the image is automatically sent to the `yolo-detections` bucket.
4.  **Manual Save**: Press **'S'** to manually sync the current frame and keypoints to MinIO.

---

## 4. Verification
- After a save or alert, check your terminal for: `SUCCESS: Uploaded to MinIO`.
- Refresh the MinIO Web Console -> Buckets -> `yolo-detections` to see your files.
