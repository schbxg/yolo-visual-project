# YOLOv11 Pose Detection Technical Documentation

## 1. Overview
This project implements a robust pose estimation system using the **YOLOv11** model. It provides two primary interfaces:
- **Web Interface**: A Gradio-based interactive demo for high-quality single-frame analysis.
- **Real-time Live Stream**: An OpenCV-based script for low-latency, real-time pose estimation.
- **Data Capture**: Integrated "Press S to Save" functionality to export pose keypoints to JSON.
- **Object Tracking**: Integrated ByteTrack for persistent ID tracking of people, **bottles**, and other objects.

---

## 2. System Architecture

### 2.1 Model Specification
- **Model**: `yolo11n-pose.pt` (for pose) and `yolo11n.pt` (for object tracking).
- **Task**: Pose Estimation & Object Detection/Tracking.
- **Output**: 17 keypoints (pose) or bounding boxes with unique IDs (tracking).

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

- **Live Detection (`live_pose.py`)**: 
    - Real-time Trackbars for Confidence/IoU.
    - **Data Capture**: Saves **three files** per capture: JSON (keypoints), `_raw.jpg` (original frame), and `_result.jpg` (annotated frame with skeleton).
- **Optimization**: Switched from `track()` to `predict()` to minimize external dependencies.

#### C. Object Tracking (`live_track.py`)
- **Algorithm**: ByteTrack.
- **Feature**: Assigns unique IDs to detected objects (e.g., bottles, people), maintaining them across frames.
- **Model**: `yolo11n.pt` (General detection).
- **Requirement**: Requires `lapx` or `lap` package.

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
  - `live_track.py`: ByteTrack integration entry point.
  - `my_bytetrack.yaml`: Custom tracking configuration and tuning guide.
  - `keypoints_concepts.md`: Explanation of pose estimation landmarks and standards.
  - `rtsp_processing_guide.md`: Detailed guide on handling RTSP streams.
  - `nvidia_vs_rk_rtsp_comparison.md`: Comparison of hardware acceleration on AI platforms.
  - `rknn_rtsp_support.md`: Technical explanation of RKNN and standard YOLO compatibility.

---

## 6. Advanced Tracking Tuning
If the tracker performance is not optimal, you can modify `my_bytetrack.yaml`. 

### Tuning Scenarios:
- **ID Flickering**: Decrease `track_low_thresh`.
- **Loss of ID during hiding**: Increase `track_buffer`.
- **IDs jumping between objects**: Decrease `match_thresh`.
- **Seeing False/Ghost IDs**: Increase `new_track_thresh`.
