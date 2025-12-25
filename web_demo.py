import gradio as gr
from ultralytics import YOLO
import cv2
import PIL.Image as Image
import numpy as np

# Load the model
model_path = 'yolo-project/models/yolov8n.pt'
model = YOLO(model_path)

def predict_image(img, conf_threshold, iou_threshold):
    # Run inference
    results = model.predict(
        source=img,
        conf=conf_threshold,
        iou=iou_threshold,
        show_labels=True,
        show_conf=True,
    )
    
    # Plot results on the image
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        return im

# Create the Gradio interface
demo = gr.Interface(
    fn=predict_image,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence Threshold"),
        gr.Slider(minimum=0, maximum=1, value=0.45, label="IoU Threshold"),
    ],
    outputs=gr.Image(type="pil", label="Result"),
    title="🌟 YOLOv8 Object Detection Interactive Demo",
    description="Upload an image to see YOLOv8 in action! Adjust the thresholds to see how detection changes.",
    examples=[["bus.jpg", 0.25, 0.45]]
)

if __name__ == "__main__":
    demo.launch(share=False)
