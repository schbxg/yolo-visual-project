# Enabling NVIDIA GPU Acceleration for YOLO

If you have an NVIDIA GPU, you can speed up your pose detection by 10x to 50x. Here is how to fix your environment.

## 1. Why is it currently using CPU?
By default, some Python environments install the **CPU-only** version of PyTorch. You can check this by running:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```
If it says `False`, you need to reinstall the CUDA version.

---

## 2. Step-by-Step Installation

### Step A: Uninstall old version
First, remove the current CPU version:
```bash
pip uninstall torch torchvision torchaudio -y
```

### Step B: Install CUDA Version
Visit [pytorch.org](https://pytorch.org/) to get the latest command. For most Windows users with recent NVIDIA GPUs, this command works:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```
> [!NOTE]
> Change `cu124` to `cu121` if you have an older GPU or older drivers.

---

## 3. How to use it in your code?

Once installed, you don't need to change much. You can force YOLO to use the GPU by adding `.to('cuda')` or using the `device` argument:

### Method A: Global Device (Recommended)
```python
from ultralytics import YOLO
import torch

# Check if GPU is ready
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

model = YOLO("yolo11n-pose.pt").to(device)
```

### Method B: Inline Argument
```python
results = model.predict(source=frame, device='cuda')
```

---

## 4. Expected Performance
| Hardware | Avg. Time per Frame |
| :--- | :--- |
| **CPU (i7 or similar)** | 100ms - 250ms |
| **NVIDIA GPU (RTX 3060+)** | 5ms - 15ms |

With a GPU, your live stream will be much smoother and feel like a real-time mirror!
