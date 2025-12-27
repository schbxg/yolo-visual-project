# 🌟 YOLO 可视化开发与训练项目

本项目提供了一个完整的 YOLOv8/v10 开发环境，支持交互式 Web 演示、命令行批量推理以及自动化模型训练。

## 📂 项目结构

```text
yolo-project/
├── data/
│   ├── dataset/         # [核心] 存放您的训练图片和标注文件
│   └── dataset.yaml     # 数据集配置文件
├── models/              # 存放权重文件 (*.pt)
├── output/              # 存放导出的数据 (如姿态关键点 JSON)
├── live_pose.py         # [增强] 实时姿态检测 + 跌倒报警 + MinIO 上传
├── live_track.py        # 实时对象追踪 (ByteTrack)
├── minio_utils.py       # [新] MinIO 对象存储集成工具
├── minio.exe            # [新] MinIO Windows 本地服务器 (已加入 .gitignore)
├── pose_demo.py         # 姿态检测 Web 界面
├── web_demo.py          # 基础对象检测 Web 界面
└── README.md            # 本说明文档
```

## 🚀 🚀 新增亮点功能

### 1. 跌倒检测 (Fall Detection)
`live_pose.py` 现在集成了实时跌倒检测逻辑。当检测到人员跌倒（基于长宽比和关节垂直距离）时，系统会：
- 在实时界面弹出 **"FALL DETECTED!"** 红色警告。
- 自动触发截图并保存至本地。
- 如果开启了 MinIO，则自动将报警截图上传至云端。

### 2. MinIO 对象存储集成
支持将所有检测结果（图片、JSON 数据）实时备份到 S3 兼容的 MinIO 服务器。

---

## 🚀 快速开始

### 1. 启动交互式 Web 演示 (推荐)
在浏览器中直接上传图片并检测：
```bash
python yolo-project/web_demo.py
```
*启动后访问: [http://127.0.0.1:7860](http://127.0.0.1:7860)*

### 2. 实时姿态检测与 MinIO 联动
运行摄像头实时姿态估计，支持数据保存与远程上传：
```bash
# 1. 启动 MinIO 服务器 (本地 Windows)
.\minio.exe server C:\minio_data --console-address ":9001"

# 2. 启动姿态检测
python live_pose.py
```
- **控制说明**:
    - **MinIO 开关**: 在 GUI 界面将 "MinIO" 滑块拨至 **1** 开启上传。
    - **手动保存**: 按 **'S'** 键同步保存图片和关键点数据。
    - **跌倒报警**: 自动触发，无需手动操作。

### 3. 实时对象追踪 (ByteTrack)
运行高效的多目标追踪（支持瓶子、人等 80 类目标）：
```bash
python live_track.py
```

## 📚 技术文档与指南
- [姿态检测技术文档](technical_documentation.md)
- [MinIO 集成与部署手册](walkthrough.md)
- [RTSP 流处理深度指南](rtsp_processing_guide.md)
- [硬件对比: NVIDIA vs Rockchip](nvidia_vs_rk_rtsp_comparison.md)

## 🎓 训练您自己的模型

### 步骤 1： 准备数据
按照以下结构将文件放入 `yolo-project/data/dataset/`：
- `images/train/`: 训练图片
- `labels/train/`: 对应的 YOLO 格式 `.txt` 标签

### 步骤 2： 执行训练
```bash
python yolo-project/scripts/train.py --data yolo-project/data/dataset.yaml --epochs 100
```

## 📊 训练结果查看
训练完成后，请前往根目录下的 `runs/detect/train/` 文件夹查看 `weights/best.pt`。
