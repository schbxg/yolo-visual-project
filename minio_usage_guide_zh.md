# MinIO 使用指南

本文档介绍了如何在 YOLO 项目中配置和使用 MinIO 对象存储，用于备份检测图像和数据。

## 1. 安装与部署

### Windows 原生运行 (推荐)
1.  **下载**: 将 [minio.exe](https://dl.min.io/server/minio/release/windows-amd64/minio.exe) 下载到项目根目录。
2.  **启动服务器**: 在 PowerShell 中运行：
    ```powershell
    mkdir C:\minio_data
    .\minio.exe server C:\minio_data --console-address ":9001"
    ```

### Docker 部署
如果您更喜欢使用容器：
```powershell
docker run -d -p 9000:9000 -p 9001:9001 `
  --name minio `
  -e "MINIO_ROOT_USER=minioadmin" `
  -e "MINIO_ROOT_PASSWORD=minioadmin" `
  quay.io/minio/minio server /data --console-address ":9001"
```

---

## 2. 访问 Web 控制台

- **链接**: [http://localhost:9001](http://localhost:9001)
- **用户名**: `minioadmin` (默认)
- **密码**: `minioadmin` (默认)

您可以在控制台中管理 Bucket 并远程浏览已上传的跌倒报警截图与关键点 JSON 文件。

---

## 3. Python 代码集成

### 配置参数
连接参数在 `minio_utils.py` 中管理：
```python
# 默认配置
endpoint = "127.0.0.1:9000"
access_key = "minioadmin"
secret_key = "minioadmin"
```
如果您的 MinIO 服务器在其他机器上，请修改这些值。

### 在 `live_pose.py` 中使用
1.  **运行脚本**: `python live_pose.py`
2.  **开启上传**: 在 GUI 界面将 **"MinIO"** 滑块拨动到 **1**。
3.  **自动报警**: 当系统识别到跌倒时，会自动抓拍并将图片发送到 `yolo-detections` 存储桶。
4.  **手动保存**: 按 **'S'** 键可手动将当前帧和关键点同步至 MinIO。

---

## 4. 验证上传
- 保存或报警后，查看终端输出：`SUCCESS: Uploaded to MinIO`。
- 刷新 MinIO Web 控制台 -> Buckets -> `yolo-detections` 即可看到新上传的文件。
