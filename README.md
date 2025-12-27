# 🌟 YOLO 可视化开发与训练项目

本项目提供了一个完整的 YOLOv8/v10 开发环境，支持交互式 Web 演示、命令行批量推理以及自动化模型训练。

## 📂 项目结构

```text
yolo-project/
├── data/
│   ├── dataset/         # [核心] 存放您的训练图片和标注文件
│   └── dataset.yaml     # 数据集配置文件
├── models/              # 存放权重文件 (*.pt)
├── output/              # [新] 存放导出的数据 (如姿态关键点 JSON)
├── live_pose.py         # [新] 实时姿态检测 + 关键点保存 (按 'S' 保存)
├── live_track.py        # [新] 实时对象追踪 (ByteTrack)
├── pose_demo.py         # 姿态检测 Web 界面
├── web_demo.py          # 基础对象检测 Web 界面
└── README.md            # 本说明文档
```

## 🚀 快速开始

### 1. 启动交互式 Web 演示 (推荐)
在浏览器中直接上传图片并检测：
```bash
python yolo-project/web_demo.py
```
*启动后访问: [http://127.0.0.1:7860](http://127.0.0.1:7860)*

### 2. 实时姿态检测与数据捕获
运行摄像头实时姿态估计，并支持导出数据：
```bash
python live_pose.py
```
- **关键点保存**: 在窗口活跃时按 **'S'** 键，将当前帧的 17 个关键点保存至 `output/keypoints/`。

### 3. 实时对象追踪 (ByteTrack)
运行高效的多目标追踪（支持瓶子、人等 80 类目标）：
```bash
python live_track.py
```
- **自定义配置**: 可通过 `my_bytetrack.yaml` 调优追踪参数。

## 📚 技术文档与指南
- [姿态检测技术文档](technical_documentation.md)
- [RTSP 流处理深度指南](rtsp_processing_guide.md)
- [硬件对比: NVIDIA vs Rockchip](nvidia_vs_rk_rtsp_comparison.md)
- [Rockchip NPU 与 RKNN 兼容性说明](rknn_rtsp_support.md)

## 🎓 训练您自己的模型

### 步骤 1： 准备数据
按照以下结构将文件放入 `yolo-project/data/dataset/`：
- `images/train/`: 训练图片
- `labels/train/`: 对应的 YOLO 格式 `.txt` 标签

### 步骤 2： 执行训练
```bash
# 本地训练
python yolo-project/scripts/train.py --data yolo-project/data/dataset.yaml --epochs 100

# 或者使用 Docker (镜像内部自动映射)
docker run --rm -it -v $(pwd)/yolo-project:/workspace ubuntu:22.04 python3 scripts/train.py
```

## 🔧 推理参数说明
在 Web 界面或脚本中，您可以实时调整以下参数：
- **Confidence (置信度)**: 调高可减少误报，调低可减少漏检。
- **IoU (重叠度)**: 控制 NMS 算法对重合框的过滤程度。

## 📊 训练结果查看
训练完成后，请前往根目录下的 `runs/detect/train/` 文件夹查看：
- `weights/best.pt`: 性能最好的模型文件。
- `results.png`: 损失函数和精度曲线图。
- `confusion_matrix.png`: 类别识别准确度矩阵。
