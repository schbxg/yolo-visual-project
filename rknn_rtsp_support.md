# Can Rockchip (RK) use the standard YOLO `model` functions?

The short answer is: **No, not for hardware acceleration.**

While you *can* install the `ultralytics` library on a Rockchip board and run `model.track()`, it will run entirely on the **CPU**, which is extremely slow (often 1-2 FPS). To use the **RK NPU** hardware, you must use the RKNN API.

## 1. Why the standard `model.track()` doesn't work on RK NPU
The `model.track()` function is built on **PyTorch**.
- **PyTorch** knows how to talk to NVIDIA GPUs (via CUDA).
- **PyTorch** does NOT know how to talk to Rockchip NPUs directly.
- The Rockchip NPU requires a specific binary format called **`.rknn`**, while `model.track()` expects `.pt` or `.engine` files.

## 2. The RK Hardware Pipeline
To get real-time RTSP performance on a board like the RK3588, you have to replace the standard YOLO steps with Rockchip-specific ones:

| Step | Standard YOLO Way | Optimized RK Way |
| :--- | :--- | :--- |
| **Decoding** | OpenCV (CPU/FFMPEG) | **Rockchip MPP** (Hardware Decoder) |
| **Data Flow** | CPU Memory | **Zero-Copy DMA-BUF** |
| **Inference** | PyTorch (CPU) | **RKNN Runtime** (NPU) |
| **Tracking** | ByteTrack (Python) | ByteTrack (C++ or Optimized Python) |

## 3. How to run RTSP on RK Platforms properly
If you want to use the NPU for an RTSP stream, you should follow this workflow instead of using `model.track()`:

1.  **Export the model**: Convert your YOLO model to ONNX, then to `.rknn` using `rknn-toolkit2`.
2.  **Use RKNN-Toolkit-Lite2**: On your RK board, use this library to load the `.rknn` model.
3.  **The Code Structure**:
    ```python
    # This is how RKNN inference looks (NOT model.track)
    from rknnlite.api import RKNNLite
    
    rknn = RKNNLite()
    rknn.load_rknn('yolo_model.rknn')
    rknn.init_runtime()
    
    # You must capture the RTSP frame manually with MPP or OpenCV
    img = capture_frame("rtsp://...")
    
    # Run inference on NPU
    outputs = rknn.inference(inputs=[img])
    
    # Then you must manually run ByteTrack on the outputs
    # (You cannot use the built-in tracking in model.track)
    ```

## 4. Are there any shortcuts?
There are community-maintained projects that wrap the RKNN API into a more "YOLO-like" interface, but they are not official Ultralytics products. 

**Recommendation**: If you are deploying on RK3588, look for the **`rknn-multi-threaded`** or **`rknn_model_zoo`** repositories on GitHub. They provide specialized C++ and Python examples specifically for running RTSP streams on the NPU as efficiently as possible.
