# MinIO RESTful API 访问指南 / MinIO RESTful API Guide

本文档介绍如何通过 HTTP RESTful API 访问 MinIO 存储中的文件。

---

## 🌐 访问方式概览

| 方式 | 适用场景 | 是否需要认证 |
|------|----------|--------------|
| **Pre-signed URL** | 临时分享、网页嵌入 | ❌ URL 自带签名 |
| **Direct URL** | 公开访问（需设置策略） | ❌ 无需认证 |
| **S3 REST API** | 程序化访问 | ✅ 需要 Access Key |

---

## 1️⃣ Pre-signed URL（推荐）

Pre-signed URL 是一个带有临时签名的链接，无需额外认证即可通过 HTTP 访问文件。

### Python 代码示例

```python
from minio_utils import MinioStorage

storage = MinioStorage()

# 获取 1 小时有效的链接
url = storage.get_presigned_url("keypoints_20251231_120000_001_result.jpg")
print(url)
# 输出: http://127.0.0.1:9000/yolo-detections/keypoints_xxx.jpg?X-Amz-Algorithm=...

# 获取 24 小时有效的链接
url_24h = storage.get_presigned_url("image.jpg", expires_hours=24)
```

### 在网页中使用

```html
<!-- 直接作为图片 src -->
<img src="http://127.0.0.1:9000/yolo-detections/image.jpg?X-Amz-Algorithm=..." />

<!-- 或用 JavaScript fetch -->
<script>
  fetch(presignedUrl)
    .then(response => response.blob())
    .then(blob => {
      const imgUrl = URL.createObjectURL(blob);
      document.getElementById('myImg').src = imgUrl;
    });
</script>
```

### 使用 curl 测试

```bash
# 获取文件
curl "http://127.0.0.1:9000/yolo-detections/image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&..."

# 下载到本地
curl -o downloaded.jpg "YOUR_PRESIGNED_URL"
```

---

## 2️⃣ 批量获取文件列表与 URL

使用 `list_objects_with_urls()` 一次性获取所有文件及其 URL：

```python
from minio_utils import MinioStorage

storage = MinioStorage()
objects = storage.list_objects_with_urls(expires_hours=2)

for obj in objects:
    print(f"文件: {obj['name']}")
    print(f"大小: {obj['size']} bytes")
    print(f"URL:  {obj['url']}")
    print("---")
```

### 输出 JSON 格式（用于 Web API）

```python
import json

objects = storage.list_objects_with_urls()
api_response = json.dumps(objects, default=str, indent=2)
print(api_response)
```

---

## 3️⃣ 直接 URL 访问（需配置公开策略）

如果希望使用固定 URL（无签名参数），需要将 Bucket 设为公开：

### 步骤 1：设置公开策略

```bash
# 使用 MinIO Client (mc) 工具
mc alias set myminio http://127.0.0.1:9000 minioadmin minioadmin
mc anonymous set download myminio/yolo-detections
```

或在 MinIO Console (http://127.0.0.1:9001) 中设置 Bucket Policy 为 `public`。

### 步骤 2：直接访问

```python
url = storage.get_direct_url("image.jpg")
# 输出: http://127.0.0.1:9000/yolo-detections/image.jpg
```

```bash
# 浏览器或 curl 直接访问
curl http://127.0.0.1:9000/yolo-detections/image.jpg
```

---

## 4️⃣ 完整 S3 REST API（高级）

MinIO 兼容 AWS S3 API，可使用标准 S3 签名认证：

### 列出 Bucket 内容

```bash
# 需要计算 AWS Signature V4 签名，或使用 awscli
aws --endpoint-url http://127.0.0.1:9000 s3 ls s3://yolo-detections/
```

### Python requests 示例（需签名库）

```python
import requests
from requests_aws4auth import AWS4Auth

auth = AWS4Auth('minioadmin', 'minioadmin', 'us-east-1', 's3')
response = requests.get(
    'http://127.0.0.1:9000/yolo-detections/',
    auth=auth
)
print(response.text)
```

> 💡 对于简单用途，推荐使用 Pre-signed URL，无需复杂的签名计算。

---

## 📊 快速测试

运行项目自带的测试脚本：

```bash
python test_minio_http.py
```

运行图片查看器（自动打开浏览器）：

```bash
python view_minio_images.py
```

---

## 🔗 相关文件

| 文件 | 说明 |
|------|------|
| [minio_utils.py](minio_utils.py) | MinIO 工具类（含 URL 生成方法） |
| [test_minio_http.py](test_minio_http.py) | HTTP 访问测试脚本 |
| [view_minio_images.py](view_minio_images.py) | 浏览器图片查看器 |
