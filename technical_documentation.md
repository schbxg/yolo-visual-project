# YOLOv11 Pose Detection Technical Documentation

## 1. Overview
This project implements a robust pose estimation system using the **YOLOv11** model. It provides two primary interfaces:
- **Web Interface**: A Gradio-based interactive demo for high-quality single-frame analysis.
- **Real-time Live Stream**: An OpenCV-based script for low-latency, real-time pose estimation with dynamic threshold controls.

---

## 2. System Architecture

### 2.1 Model Specification
- **Model**: `yolo11n-pose.pt` (Nano version for high efficiency).
- **Task**: Pose Estimation (Keypoint Detection).
- **Output**: 17 human joints (keypoints) and their respective confidence scores, along with person bounding boxes.

### 2.2 Core Components

#### A. Web Demo (`pose_demo.py`)
- **Backend**: Gradio Blocks.
- **Imaging**: PIL (Python Imaging Library).
- **Control**: Support for Confidence and IoU threshold adjustment via UI sliders.
- **Workflow**: 
  1. Capture picture/upload.
  2. Send to YOLO model.
  3. Plot results using Ultralytics `Annotator`.
  4. Display back to user.

#### B. Live Detection (`live_pose.py`)
- **Backend**: OpenCV (cv2).
- **Imaging**: NumPy Arrays (BGR format).
- **Real-time Control**: OpenCV Trackbars for live parameter tuning.
- **Optimization**: Switched from `track()` to `predict()` to minimize external dependencies (`lap` library) while maintaining high FPS.

---

## 3. Data Formats & Processing

### 3.1 Input Format
The system accepts raw pixel data from the webcam via OpenCV:
- **Color Space**: BGR (Blue-Green-Red).
- **Structure**: NumPy `ndarray` of shape `(Height, Width, 3)`.
- **Pre-processing**: YOLO automatically resizes inputs to a standard size (default `640x640`) using letterboxing to maintain aspect ratio before inference.

### 3.2 Detection Output
For each frame, the model returns a `Results` object containing:
- **Boxes**: `(x1, y1, x2, y2)` coordinates of detected people.
- **Keypoints**: `(x, y)` coordinates for 17 standard COCO points (eyes, ears, nose, shoulders, elbows, wrists, hips, knees, ankles).
- **Confidence**: Probability scores for both the person box and each individual keypoint.

### 3.3 Visualization Pipeline
1. **Plotting**: The `results[0].plot()` method is used for rendering.
2. **BGR/RGB Handling**: 
   - `pose_demo.py` converts BGR to RGB for Gradio display.
   - `live_pose.py` uses direct BGR rendering for maximum OpenCV performance.

---

## 4. Implementation Details

### 4.1 Interface Comparison

| Feature | Web Demo (`pose_demo`) | Live Stream (`live_pose`) |
| :--- | :--- | :--- |
| **FPS** | Low (Capture & Process) | High (Streaming) |
| **Library** | Gradio | OpenCV |
| **Output Type** | Static Processed Image | Real-time Video Window |
| **Use Case** | Detailed analysis, screenshots | Interactive real-time testing |

### 4.2 Error Handling
- **Missing Models**: Automatically checks local path and downloads from Ultralytics server if unavailable.
- **Empty Frames**: Robust check for `img is None` to prevent pipeline crashes.
- **No Detections**: Returns the original raw frame if the model finds 0 people, ensuring a continuous video stream.

---

## 5. Directory Structure
- `yolo-project/`: Root directory.
  - `models/`: Contains the `.pt` binary weights.
  - `scripts/`: Supplemental utility scripts.
  - `pose_demo.py`: Main Gradio entry point.
  - `live_pose.py`: Main OpenCV live entry point.
