# How YOLO Resizes Images: The "Letterbox" Technique

YOLO models (like YOLOv11) usually require a fixed input size, typically **640x640**. However, most cameras or RTSP streams are **1920x1080** (16:9). 

YOLO does NOT simply stretch the image, as that would distort shapes (making people look fat or skinny) and hurt detection accuracy. Instead, it uses a technique called **Letterboxing**.

## 1. The 3-Step Process

Imagine you have a **1280x720** original image and want to fit it into **640x640**.

### Step A: Scale while keeping Aspect Ratio
The model calculates the scaling factor for both width and height and chooses the **smaller** one.
- 640 / 1280 = 0.5
- 640 / 720 = 0.88
- **Winning factor**: 0.5
- **Resulting image**: 640 x 360 (Perfectly proportional, but not a square yet).

### Step B: Center and Pad
To make it a 640x640 square, the model adds padding (usually gray pixels, color `(114, 114, 114)`).
- **Target Height**: 640
- **Current Height**: 360
- **Gap**: 280 pixels
- **Padding**: 140 pixels at the top and 140 pixels at the bottom.

### Step C: Normalization
The pixel values are then divided by 255.0 to bring them into the `[0, 1]` range for the neural network.

---

## 2. Why not just Stretch/Resize?

| Method | Visual Result | Impact on AI |
| :--- | :--- | :--- |
| **Stretch** | Distorted (Wide or Tall) | Poor accuracy; features like height/width ratios are ruined. |
| **Crop** | Missing edges | Might lose objects near the boundaries of the frame. |
| **Letterbox** | Original info is safe | **Highest Accuracy**; preserve the geometry of the objects. |

---

## 3. How do we get original Coordinates?

When the model detects a nose at `(320, 200)` in the **640x640** processed image, it uses a reverse formula to give you the coordinates in your **1920x1080** original image:

1.  **Subtract Padding**: Remove the 140px gray borders.
2.  **Multiply by Inverse Scale**: Divide the coordinate by the 0.5 scaling factor.

**Ultralytics YOLO does this math for you automatically** in the `results[0].boxes` or `results[0].keypoints` objects. The values you see in your JSON files are already mapped back to your original source pixels.

---

## 4. Pro Tip: Rectangular Inference
In modern YOLO, if you are processing a batch of similar 16:9 images, the model can use "Rectangular Inference" to reduce the gray padding and speed up processing by as much as 30%. It simply processes a 640x384 "Letterbox" instead of a full 640x640 square.
